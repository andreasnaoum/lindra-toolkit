#!/usr/bin/env python3
"""
Lindra Toolkit - Main Module

This script serves as the main entry point for the Lindra Toolkit, integrating all components
for generating and analyzing conversations with the Lindra AI assistant.

Usage:
    1. Generate and analyze new conversations:
       python main.py --generate

    2. Analyze existing conversations:
       python main.py --analyze path/to/conversations.jsonl

    3. Customize conversation length:
       python main.py --generate --messages 8

    4. Use a different classifier set:
       python main.py --generate --classifier-set v1

Example workflow:
    1. First, set up your environment variables in a .env file:
       ANTHROPIC_API_KEY=your_api_key
       OPENAI_API_KEY=your_api_key
       HUME_API_KEY=your_api_key

    2. Generate conversations with all personas:
       python main.py --generate

    3. Analyze the results in the conversations_output directory:
       - Review the JSON files for detailed results
       - Open the CSV files for tabular data
       - Check the PNG files for visualizations
"""

import os
import asyncio
import json
import argparse
import time
import csv
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any
from datetime import datetime
import seaborn as sns

# Import LLM-Test modules
from LLMTest.llmtestframework import simulate_conversation, save_conversation_to_json, save_all_conversations_to_jsonl, \
    save_conversation_to_csv
from LLMTest.personas import personas
from LLMTest.assistant import ASSISTANT_PROMPT

# Import Classifier modules
import Classifiers.emoclassifiers.io_utils as io_utils
import Classifiers.emoclassifiers.classification as classification
import Classifiers.emoclassifiers.aggregation as aggregation

# Load environment variables
load_dotenv()

# Global settings
OUTPUT_FOLDER = "conversations_output"  # Directory where all output files will be saved
NUM_MESSAGES = 6  # Default number of messages in each conversation
CLASSIFIER_SET = "v1"  # Default classifier set version


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output directory: {OUTPUT_FOLDER}")


async def analyze_conversation(conversation: List[Dict], model_wrapper, classifiers, aggregator):
    """
    Analyze a conversation using the classifiers

    Args:
        conversation: List of conversation messages in the format [{"role": "user", "content": "..."}, ...]
        model_wrapper: Instance of ModelWrapper that manages API calls
        classifiers: Dictionary of classifier instances
        aggregator: Aggregator instance to combine results

    Returns:
        Dictionary of classifier results for the conversation
    """
    results = {}
    for classifier_name, classifier in classifiers.items():
        raw_result = await classifier.classify_conversation(conversation)
        result = aggregator.aggregate(raw_result)
        results[classifier_name] = result
    return results


async def run_classifier_analysis(conversations_data: Dict[str, Any], conversation_source="generated"):
    """
    Run classifier analysis on a set of conversations

    This function:
    1. Initializes the classifier models
    2. Analyzes each conversation with appropriate classifiers
    3. Saves the results to a JSON file

    Args:
        conversations_data: Dictionary of conversations with persona information
        conversation_source: Source of conversations - "generated" or "hume"
                            - "generated": Only use target classifiers in personas
                            - "hume": Use all available classifiers

    Returns:
        Dictionary of analysis results by persona
    """
    print(f"Running classifier analysis for {conversation_source} conversations...")

    # Initialize model wrapper and load classifiers
    model_wrapper = classification.ModelWrapper(
        model="gpt-4o-mini-2024-07-18",  # Using GPT-4o mini for classification
        max_concurrent=4  # Limit concurrent API calls
    )

    # Load the classifier definitions from the specified set
    all_classifiers = classification.load_classifiers(
        classifier_set=CLASSIFIER_SET,
        model_wrapper=model_wrapper,
    )

    # Use the "any" aggregator (returns True if any chunk is classified as Yes)
    aggregator = aggregation.AGGREGATOR_DICT["any"]

    # Process each conversation
    analysis_results = {}
    for persona_name, data in conversations_data.items():
        conversation = data["conversation"]
        persona = data["persona"]
        print(f"Analyzing conversation with {persona_name}...")

        # Determine which classifiers to use based on the conversation source
        if conversation_source == "generated":
            # For generated conversations, only use target classifiers if defined
            if "target_classifiers" in persona and persona["target_classifiers"]:
                classifier_names = persona["target_classifiers"]
                classifiers_to_use = {name: all_classifiers[name] for name in classifier_names
                                      if name in all_classifiers}
            else:
                # If no target classifiers defined, use all classifiers
                classifiers_to_use = all_classifiers
        else:
            # For Hume conversations, use all available classifiers
            classifiers_to_use = all_classifiers

        # Run analysis with selected classifiers
        results = {}
        for classifier_name, classifier in classifiers_to_use.items():
            raw_result = await classifier.classify_conversation(conversation)
            result = aggregator.aggregate(raw_result)
            results[classifier_name] = result

        # Check if persona has target classifiers defined
        target_validation = evaluate_target_classifiers(persona, results)

        analysis_results[persona_name] = {
            "persona": persona,
            "classification_results": results,
            "target_validation": target_validation,
            "conversation_source": conversation_source
        }

        print(analysis_results)

    # Save results with timestamp to avoid overwriting
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(OUTPUT_FOLDER, f"classification_results_{conversation_source}_{timestamp}.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2)

    print(f"Classification results saved to {results_file}")
    return analysis_results


async def run_classifier_analysis_with_rate_limits(conversations_data: Dict[str, Any], conversation_source="generated"):
    """
    Run classifier analysis on a set of conversations with robust rate limiting

    This function:
    1. Initializes the classifier models with rate limiting
    2. Analyzes each conversation with appropriate classifiers
    3. Implements proper rate limit handling and retries
    4. Saves the results to a JSON file

    Args:
        conversations_data: Dictionary of conversations with persona information
        conversation_source: Source of conversations - "generated" or "hume"
                            - "generated": Only use target classifiers in personas
                            - "hume": Use all available classifiers

    Returns:
        Dictionary of analysis results by conversation ID
    """
    import time
    import random
    import asyncio
    from datetime import datetime
    import os
    import json

    print(f"Running classifier analysis for {conversation_source} conversations with rate limiting...")

    # Create a RateLimitManager
    class RateLimitManager:
        def __init__(self, max_retries=8, base_delay=1.0, max_delay=60.0):
            self.max_retries = max_retries
            self.base_delay = base_delay
            self.max_delay = max_delay
            self.last_request_time = 0
            self.request_count = 0

        async def execute(self, func, *args, **kwargs):
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    # Check if this is a rate limit error
                    is_rate_limit = False
                    retry_after = None

                    # Check for OpenAI rate limit error
                    error_name = e.__class__.__name__
                    if error_name == "RateLimitError" or "rate_limit" in str(e).lower():
                        is_rate_limit = True

                        # Try to extract retry time
                        import re
                        match = re.search(r"try again in (\d+)ms", str(e).lower())
                        if match:
                            retry_after = int(match.group(1)) / 1000.0  # Convert ms to seconds

                    # If not a rate limit error, re-raise
                    if not is_rate_limit:
                        raise

                    # If max retries reached, raise
                    if retries >= self.max_retries:
                        print(f"Max retries ({self.max_retries}) exceeded. Rate limit error: {e}")
                        raise

                    # Calculate backoff time
                    if retry_after is not None:
                        backoff = retry_after + random.uniform(0.1, 1.0)  # Add jitter
                    else:
                        # Exponential backoff with jitter
                        backoff = min(self.max_delay, self.base_delay * (2 ** retries))
                        backoff += random.uniform(0, backoff / 2)  # Add jitter

                    retries += 1
                    print(
                        f"Rate limit hit. Retrying in {backoff:.2f} seconds... (Attempt {retries}/{self.max_retries})")
                    await asyncio.sleep(backoff)

    # Initialize model wrapper and load classifiers
    model_wrapper = classification.ModelWrapper(
        model="gpt-4o-mini-2024-07-18",  # Using GPT-4o mini for classification
        max_concurrent=5  # Reduced from 4 to be more conservative
    )

    # model="gpt-4.1-mini",
    # model = "gpt-4o-mini-2024-07-18",  # Using GPT-4o mini for classification

    # Create a rate limiter
    rate_limiter = RateLimitManager()

    # Add rate limiting to the model wrapper
    original_classify = model_wrapper.classify_conversation_chunk

    async def rate_limited_classify(*args, **kwargs):
        return await rate_limiter.execute(original_classify, *args, **kwargs)

    # Patch the method with our rate-limited version
    model_wrapper.classify_conversation_chunk = rate_limited_classify

    # Load the classifier definitions from the specified set
    all_classifiers = classification.load_classifiers(
        classifier_set=CLASSIFIER_SET,
        model_wrapper=model_wrapper,
    )

    # Use the "any" aggregator (returns True if any chunk is classified as Yes)
    aggregator = aggregation.AGGREGATOR_DICT["any"]

    # Process each conversation with rate limiting
    analysis_results = {}
    processed_count = 0
    total_count = len(conversations_data)
    start_time = time.time()

    for conv_id, data in conversations_data.items():
        conversation = data["conversation"]
        persona = data["persona"]

        # Calculate progress and ETA
        processed_count += 1
        elapsed_time = time.time() - start_time
        avg_time_per_item = elapsed_time / processed_count if processed_count > 0 else 0
        remaining_items = total_count - processed_count
        eta_seconds = avg_time_per_item * remaining_items

        # Format ETA as minutes and seconds
        eta_minutes = int(eta_seconds // 60)
        eta_seconds_remainder = int(eta_seconds % 60)

        print(
            f"Analyzing conversation {processed_count}/{total_count} with ID '{conv_id}'... (ETA: {eta_minutes}m {eta_seconds_remainder}s)")

        # Determine which classifiers to use based on the conversation source
        if conversation_source == "generated":
            # For generated conversations, only use target classifiers if defined
            if "target_classifiers" in persona and persona["target_classifiers"]:
                classifier_names = persona["target_classifiers"]
                classifiers_to_use = {name: all_classifiers[name] for name in classifier_names
                                      if name in all_classifiers}
            else:
                # If no target classifiers defined, use all classifiers
                classifiers_to_use = all_classifiers
        else:
            # For Hume conversations, use all available classifiers
            classifiers_to_use = all_classifiers

        print(all_classifiers)

        # Run analysis with selected classifiers, with rate limiting
        results = {}

        # Process classifiers with rate limiting
        classifier_tasks = []

        # Create a semaphore to limit concurrent classifier tasks
        # This adds an additional limit to prevent rate limit issues
        sem = asyncio.Semaphore(2)  # Allow at most 2 concurrent classifier tasks

        for classifier_name, classifier in classifiers_to_use.items():
            # Add a rate-limited wrapper for classify_conversation
            async def process_classifier(name, cls):
                async with sem:  # Acquire semaphore to limit concurrency
                    try:
                        # Add small random delay between classifier calls to avoid burst requests
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                        raw_result = await cls.classify_conversation(conversation)
                        result = aggregator.aggregate(raw_result)
                        return name, result
                    except Exception as e:
                        print(f"Error processing classifier {name}: {e}")
                        return name, None

            # Add task to the list
            classifier_tasks.append(process_classifier(classifier_name, classifier))

        # Wait for all classifiers to complete
        classifier_results = await asyncio.gather(*classifier_tasks)

        # Process results
        for name, result in classifier_results:
            if result is not None:
                results[name] = result

        # Check if persona has target classifiers defined
        target_validation = evaluate_target_classifiers(persona, results)

        # Store results
        analysis_results[conv_id] = {
            "persona": persona,
            "classification_results": results,
            "target_validation": target_validation,
            "conversation_source": conversation_source
        }

        if "chat_id" in data:
            analysis_results[conv_id]["chat_id"] = data["chat_id"]

        print(analysis_results)

        # Save intermediate results after every 5 conversations
        if processed_count % 5 == 0 or processed_count == total_count:
            # Save intermediate results with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            intermediate_file = os.path.join(OUTPUT_FOLDER,
                                             f"intermediate_results_{conversation_source}_{timestamp}.json")
            with open(intermediate_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=2)
            print(f"Saved intermediate results after {processed_count}/{total_count} conversations")

    # Save final results with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(OUTPUT_FOLDER, f"classification_results_{conversation_source}_{timestamp}.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2)

    print(f"Classification results saved to {results_file}")

    # Calculate and display statistics
    total_time = time.time() - start_time
    avg_time_per_conversation = total_time / total_count if total_count > 0 else 0
    print(f"Analysis completed in {total_time:.2f} seconds")
    print(f"Average time per conversation: {avg_time_per_conversation:.2f} seconds")

    return analysis_results

def evaluate_target_classifiers(persona, classifier_results):
    """
    Evaluate if a conversation meets all target classifiers for a persona

    Args:
        persona: The persona dictionary with target classifiers
        classifier_results: The results of classifier analysis

    Returns:
        Dictionary with validation status and details
    """
    # Check if persona has target classifiers defined
    if "target_classifiers" not in persona:
        return {
            "status": "SKIP",
            "message": "No target classifiers defined for this persona",
            "details": {}
        }

    target_classifiers = persona["target_classifiers"]
    validation_results = {}
    all_passed = True

    for classifier_name in target_classifiers:
        # Check if the classifier exists in results
        if classifier_name not in classifier_results:
            validation_results[classifier_name] = {
                "status": "ERROR",
                "message": f"Classifier '{classifier_name}' not found in results"
            }
            all_passed = False
            continue

        # Check if the classifier was detected
        detected = classifier_results[classifier_name]
        validation_results[classifier_name] = {
            "status": "PASS" if detected else "FAIL",
            "detected": detected
        }

        if not detected:
            all_passed = False

    return {
        "status": "PASS" if all_passed else "FAIL",
        "details": validation_results
    }


def convert_json_to_csv(json_file_path, output_folder=None):
    """
    Convert a conversation from JSON format to CSV format

    This function:
    1. Loads a conversation from a JSON file
    2. Extracts only the conversation part (without persona details)
    3. Saves it as a CSV file with the same name

    Args:
        json_file_path: Path to the JSON file containing the conversation
        output_folder: Optional folder to save the CSV file (defaults to same folder as JSON)

    Returns:
        Path to the generated CSV file
    """
    # Determine output path
    if output_folder is None:
        output_folder = os.path.dirname(json_file_path)

    ensure_output_dir()

    # Load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if "conversation" not in data:
        print(f"Error: {json_file_path} does not contain a conversation field")
        return None

    # Extract conversation
    conversation = data["conversation"]

    # Determine output filename
    base_name = os.path.basename(json_file_path)
    csv_filename = os.path.splitext(base_name)[0] + ".csv"
    csv_path = os.path.join(output_folder, csv_filename)

    # Write to CSV
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['turn', 'role', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, message in enumerate(conversation):
            writer.writerow({
                'turn': i + 1,
                'role': message['role'],
                'content': message['content']
            })

    print(f"Converted {json_file_path} to {csv_path}")
    return csv_path


def generate_conversations(conversations_per_persona=3):
    """
    Generate conversations between Lindra and all defined personas

    This function:
    1. Creates multiple simulated conversations for each persona in the personas list
    2. Saves individual conversations as JSON files
    3. Saves individual conversations as CSV files
    4. Creates a combined JSONL file with all conversations

    Args:
        conversations_per_persona: Number of conversations to generate for each persona

    Usage:
        # Generate conversations with default settings (3 per persona)
        conversations = generate_conversations()

        # Generate 5 conversations per persona
        conversations = generate_conversations(5)

        # Access a specific conversation
        ethan_conversation = conversations["Ethan_1"]["conversation"]

    Returns:
        Dictionary containing all generated conversations
    """
    print(f"Generating {conversations_per_persona} conversations per persona...")
    ensure_output_dir()

    all_conversations = {}

    # Simulate conversations for each persona
    for i, persona in enumerate(personas):
        print(
            f"Processing persona {i + 1}/{len(personas)}: {persona['name']} ({persona['test_category']}: {persona['specific_focus']})...")

        # Generate multiple conversations for each persona
        for conv_num in range(1, conversations_per_persona + 1):
            print(f"  Generating conversation {conv_num}/{conversations_per_persona}...")

            # Generate conversation
            conversation = simulate_conversation(persona, NUM_MESSAGES, ASSISTANT_PROMPT)

            # Create unique identifier for this persona-conversation
            persona_conv_id = f"{persona['name']}_{conv_num}"

            # Create filename base with unique identifier
            filename_base = f"{persona['name']}_{persona['specific_focus'].replace(' ', '_')}_{conv_num}"

            # Save individual conversation to JSON
            json_filename = os.path.join(OUTPUT_FOLDER, f"{filename_base}.json")
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "persona": persona,
                    "conversation": conversation,
                    "conversation_number": conv_num
                }, f)
            print(f"    Saved to {json_filename}")

            # Save individual conversation to CSV
            csv_filename = os.path.join(OUTPUT_FOLDER, f"{filename_base}.csv")
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['turn', 'role', 'content']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for j, message in enumerate(conversation):
                    writer.writerow({
                        'turn': j + 1,
                        'role': message['role'],
                        'content': message['content']
                    })
            print(f"    Saved to CSV: {csv_filename}")

            # Add to all conversations dictionary
            all_conversations[persona_conv_id] = {
                "persona": persona,
                "conversation": conversation,
                "conversation_number": conv_num
            }

            # Add a small delay between conversations
            time.sleep(1)

    # Save all conversations to JSONL file
    all_conversations_file = os.path.join(OUTPUT_FOLDER,
                                          f"all_conversations_{conversations_per_persona}_per_persona.jsonl")
    save_all_conversations_to_jsonl(all_conversations, all_conversations_file)
    print(f"All conversations saved to {all_conversations_file}")

    return all_conversations


# Modifications for visualize_results_hume function

def visualize_results_hume(analysis_results):
    """
    Generate visualizations of the analysis results for Hume conversations

    This function:
    1. Processes the classification results into a format suitable for visualization
    2. Creates a CSV file with the results
    3. Generates visualizations of the results including:
       - Individual conversation results by classifier
       - Aggregated results across multiple conversations

    This version is designed for Hume conversations with ID-based structure rather than personas,
    and does not include validation status visualization.

    Args:
        analysis_results: Dictionary of analysis results from run_classifier_analysis
    """
    print("Generating visualizations for Hume conversations...")

    # Extract data for visualization
    conversation_ids = []
    chat_ids = []
    results = {}

    for conv_id, data in analysis_results.items():
        # Add to visualization data
        conversation_ids.append(conv_id)

        # Get chat_id from persona data or use conv_id as fallback
        chat_id = data.get("chat_id", conv_id)
        if "persona" in data and isinstance(data["persona"], dict):
            if "chat_id" in data["persona"]:
                chat_id = data["persona"]["chat_id"]
        chat_ids.append(chat_id)

        # Extract classifier results
        for classifier, result in data["classification_results"].items():
            if classifier not in results:
                results[classifier] = []
            # Convert boolean or dictionary results to a numeric value for visualization
            if isinstance(result, bool):
                results[classifier].append(1 if result else 0)
            elif isinstance(result, dict):
                # For raw aggregator, calculate percentage of True values
                true_count = sum(1 for v in result.values() if v)
                total = len(result)
                results[classifier].append(true_count / total if total > 0 else 0)

    # Create a DataFrame for easier visualization
    df_data = {
        "ConversationID": conversation_ids,
        "ChatID": chat_ids
    }
    for classifier, values in results.items():
        df_data[classifier] = values

    df = pd.DataFrame(df_data)

    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(OUTPUT_FOLDER, f"hume_analysis_results_{timestamp}.csv")
    df.to_csv(csv_file, index=False)
    print(f"Analysis results saved to {csv_file}")

    # Generate classifier results visualization for individual conversations
    plt.figure(figsize=(15, 10))

    # Set up the bar plot
    x = np.arange(len(conversation_ids))
    bar_width = 0.8 / len(results)

    for i, (classifier, values) in enumerate(results.items()):
        plt.bar(x + i * bar_width, values, width=bar_width, label=classifier, alpha=0.7)

    plt.xlabel("Conversation ID")
    plt.ylabel("Classification Result")
    plt.title("Classification Results by Conversation and Classifier")
    plt.xticks(x + bar_width * (len(results) - 1) / 2, conversation_ids, rotation=90, ha="right")
    plt.legend()
    plt.tight_layout()

    # Save plot
    plot_file = os.path.join(OUTPUT_FOLDER, f"hume_classification_plot_{timestamp}.png")
    plt.savefig(plot_file)
    print(f"Visualization saved to {plot_file}")

    # Calculate summary statistics for each classifier
    summary_stats = {}
    for classifier, values in results.items():
        summary_stats[classifier] = {
            "mean": np.mean(values),
            "positive_rate": np.mean([1 if v > 0.5 else 0 for v in values]),
            "count": len(values),
            "positive_count": sum(1 for v in values if v > 0.5)
        }

    # Generate summary bar chart for each classifier
    plt.figure(figsize=(12, 6))

    classifiers = list(summary_stats.keys())
    positive_rates = [summary_stats[c]["positive_rate"] for c in classifiers]

    bars = plt.bar(classifiers, positive_rates, alpha=0.7)

    # Color bars according to positive rate
    for i, bar in enumerate(bars):
        rate = positive_rates[i]
        color = plt.cm.RdYlGn(rate)  # Red to Yellow to Green color map
        bar.set_color(color)

    plt.xlabel("Classifiers")
    plt.ylabel("Positive Detection Rate")
    plt.title("Classifier Detection Rates Across All Conversations")
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, 1.1)  # Set y-axis from 0 to 1.1 to show full bars
    plt.tight_layout()

    # Save summary plot
    summary_plot_file = os.path.join(OUTPUT_FOLDER, f"hume_detection_rates_{timestamp}.png")
    plt.savefig(summary_plot_file)
    print(f"Summary visualization saved to {summary_plot_file}")

    # Save detailed summary statistics to a JSON file
    summary_file = os.path.join(OUTPUT_FOLDER, f"hume_summary_stats_{timestamp}.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_stats, f, indent=2)
    print(f"Summary statistics saved to {summary_file}")

    # Create a summary CSV with one row per classifier
    summary_df = pd.DataFrame({
        "Classifier": classifiers,
        "Mean": [summary_stats[c]["mean"] for c in classifiers],
        "Positive_Rate": positive_rates,
        "Total_Conversations": [summary_stats[c]["count"] for c in classifiers],
        "Positive_Count": [summary_stats[c]["positive_count"] for c in classifiers]
    })

    summary_csv = os.path.join(OUTPUT_FOLDER, f"hume_classifier_summary_{timestamp}.csv")
    summary_df.to_csv(summary_csv, index=False)
    print(f"Classifier summary saved to {summary_csv}")

    # Create a chat ID summary CSV
    chat_summary_df = pd.DataFrame({
        "ConversationID": conversation_ids,
        "ChatID": chat_ids
    })

    # Add classifier results
    for classifier, values in results.items():
        chat_summary_df[classifier] = values

    chat_summary_csv = os.path.join(OUTPUT_FOLDER, f"hume_chat_id_summary_{timestamp}.csv")
    chat_summary_df.to_csv(chat_summary_csv, index=False)
    print(f"Chat ID summary saved to {chat_summary_csv}")

    # Generate a heatmap visualization if there are multiple classifiers
    if len(classifiers) > 1:
        plt.figure(figsize=(14, 8))

        # Create a correlation matrix of classifiers
        corr_matrix = np.zeros((len(classifiers), len(classifiers)))
        for i, c1 in enumerate(classifiers):
            for j, c2 in enumerate(classifiers):
                # Calculate correlation coefficient between classifier results
                corr = np.corrcoef(results[c1], results[c2])[0, 1]
                corr_matrix[i, j] = corr

        # Plot the heatmap
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
                    xticklabels=classifiers, yticklabels=classifiers)
        plt.title("Correlation Between Classifiers")
        plt.tight_layout()

        # Save heatmap
        heatmap_file = os.path.join(OUTPUT_FOLDER, f"hume_classifier_correlation_{timestamp}.png")
        plt.savefig(heatmap_file)
        print(f"Classifier correlation heatmap saved to {heatmap_file}")

    # Return a summary of results for terminal output
    return {
        "total_conversations": len(conversation_ids),
        "classifiers": classifiers,
        "classifier_stats": summary_stats
    }

# def visualize_results_hume(analysis_results):
#     """
#     Generate visualizations of the analysis results for Hume conversations
#
#     This function:
#     1. Processes the classification results into a format suitable for visualization
#     2. Creates a CSV file with the results
#     3. Generates visualizations of the results including:
#        - Individual conversation results by classifier
#        - Aggregated results across multiple conversations
#
#     This version is designed for Hume conversations with ID-based structure rather than personas,
#     and does not include validation status visualization.
#
#     Args:
#         analysis_results: Dictionary of analysis results from run_classifier_analysis
#     """
#     print("Generating visualizations for Hume conversations...")
#
#     # Extract data for visualization
#     conversation_ids = []
#     results = {}
#
#     for conv_id, data in analysis_results.items():
#         # Add to visualization data
#         conversation_ids.append(conv_id)
#
#         # Extract classifier results
#         for classifier, result in data["classification_results"].items():
#             if classifier not in results:
#                 results[classifier] = []
#             # Convert boolean or dictionary results to a numeric value for visualization
#             if isinstance(result, bool):
#                 results[classifier].append(1 if result else 0)
#             elif isinstance(result, dict):
#                 # For raw aggregator, calculate percentage of True values
#                 true_count = sum(1 for v in result.values() if v)
#                 total = len(result)
#                 results[classifier].append(true_count / total if total > 0 else 0)
#
#     # Create a DataFrame for easier visualization
#     df_data = {"ConversationID": conversation_ids}
#     for classifier, values in results.items():
#         df_data[classifier] = values
#
#     df = pd.DataFrame(df_data)
#
#     # Save to CSV
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     csv_file = os.path.join(OUTPUT_FOLDER, f"hume_analysis_results_{timestamp}.csv")
#     df.to_csv(csv_file, index=False)
#     print(f"Analysis results saved to {csv_file}")
#
#     # Generate classifier results visualization for individual conversations
#     plt.figure(figsize=(15, 10))
#
#     # Set up the bar plot
#     x = np.arange(len(conversation_ids))
#     bar_width = 0.8 / len(results)
#
#     for i, (classifier, values) in enumerate(results.items()):
#         plt.bar(x + i * bar_width, values, width=bar_width, label=classifier, alpha=0.7)
#
#     plt.xlabel("Conversation ID")
#     plt.ylabel("Classification Result")
#     plt.title("Classification Results by Conversation and Classifier")
#     plt.xticks(x + bar_width * (len(results) - 1) / 2, conversation_ids, rotation=90, ha="right")
#     plt.legend()
#     plt.tight_layout()
#
#     # Save plot
#     plot_file = os.path.join(OUTPUT_FOLDER, f"hume_classification_plot_{timestamp}.png")
#     plt.savefig(plot_file)
#     print(f"Visualization saved to {plot_file}")
#
#     # Calculate summary statistics for each classifier
#     summary_stats = {}
#     for classifier, values in results.items():
#         summary_stats[classifier] = {
#             "mean": np.mean(values),
#             "positive_rate": np.mean([1 if v > 0.5 else 0 for v in values]),
#             "count": len(values),
#             "positive_count": sum(1 for v in values if v > 0.5)
#         }
#
#     # Generate summary bar chart for each classifier
#     plt.figure(figsize=(12, 6))
#
#     classifiers = list(summary_stats.keys())
#     positive_rates = [summary_stats[c]["positive_rate"] for c in classifiers]
#
#     bars = plt.bar(classifiers, positive_rates, alpha=0.7)
#
#     # Color bars according to positive rate
#     for i, bar in enumerate(bars):
#         rate = positive_rates[i]
#         color = plt.cm.RdYlGn(rate)  # Red to Yellow to Green color map
#         bar.set_color(color)
#
#     plt.xlabel("Classifiers")
#     plt.ylabel("Positive Detection Rate")
#     plt.title("Classifier Detection Rates Across All Conversations")
#     plt.xticks(rotation=45, ha="right")
#     plt.ylim(0, 1.1)  # Set y-axis from 0 to 1.1 to show full bars
#     plt.tight_layout()
#
#     # Save summary plot
#     summary_plot_file = os.path.join(OUTPUT_FOLDER, f"hume_detection_rates_{timestamp}.png")
#     plt.savefig(summary_plot_file)
#     print(f"Summary visualization saved to {summary_plot_file}")
#
#     # Save detailed summary statistics to a JSON file
#     summary_file = os.path.join(OUTPUT_FOLDER, f"hume_summary_stats_{timestamp}.json")
#     with open(summary_file, 'w', encoding='utf-8') as f:
#         json.dump(summary_stats, f, indent=2)
#     print(f"Summary statistics saved to {summary_file}")
#
#     # Create a summary CSV with one row per classifier
#     summary_df = pd.DataFrame({
#         "Classifier": classifiers,
#         "Mean": [summary_stats[c]["mean"] for c in classifiers],
#         "Positive_Rate": positive_rates,
#         "Total_Conversations": [summary_stats[c]["count"] for c in classifiers],
#         "Positive_Count": [summary_stats[c]["positive_count"] for c in classifiers]
#     })
#
#     summary_csv = os.path.join(OUTPUT_FOLDER, f"hume_classifier_summary_{timestamp}.csv")
#     summary_df.to_csv(summary_csv, index=False)
#     print(f"Classifier summary saved to {summary_csv}")
#
#     # Generate a heatmap visualization if there are multiple classifiers
#     if len(classifiers) > 1:
#         plt.figure(figsize=(14, 8))
#
#         # Create a correlation matrix of classifiers
#         corr_matrix = np.zeros((len(classifiers), len(classifiers)))
#         for i, c1 in enumerate(classifiers):
#             for j, c2 in enumerate(classifiers):
#                 # Calculate correlation coefficient between classifier results
#                 corr = np.corrcoef(results[c1], results[c2])[0, 1]
#                 corr_matrix[i, j] = corr
#
#         # Plot the heatmap
#         sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1,
#                     xticklabels=classifiers, yticklabels=classifiers)
#         plt.title("Correlation Between Classifiers")
#         plt.tight_layout()
#
#         # Save heatmap
#         heatmap_file = os.path.join(OUTPUT_FOLDER, f"hume_classifier_correlation_{timestamp}.png")
#         plt.savefig(heatmap_file)
#         print(f"Classifier correlation heatmap saved to {heatmap_file}")
#
#     # Return a summary of results for terminal output
#     return {
#         "total_conversations": len(conversation_ids),
#         "classifiers": classifiers,
#         "classifier_stats": summary_stats
#     }

def visualize_results(analysis_results):
    """
    Generate visualizations of the analysis results

    This function:
    1. Processes the classification results into a format suitable for visualization
    2. Creates a CSV file with the results
    3. Generates multiple visualizations of the results including:
       - Individual conversation results
       - Aggregated results across multiple conversations
       - Summary statistics

    Args:
        analysis_results: Dictionary of analysis results from run_classifier_analysis
    """
    print("Generating visualizations...")

    # Extract data for visualization
    personas = []
    categories = []
    results = {}
    validation_status = []
    conversation_numbers = []

    for persona_conv_id, data in analysis_results.items():
        # Extract persona name and conversation number
        if "_" in persona_conv_id and persona_conv_id.split("_")[-1].isdigit():
            parts = persona_conv_id.split("_")
            persona_name = "_".join(parts[:-1])
            conv_num = int(parts[-1])
        else:
            persona_name = persona_conv_id
            conv_num = 1  # Default for old format

        # Add to visualization data
        personas.append(persona_name)
        categories.append(data["persona"]["test_category"])
        conversation_numbers.append(conv_num)

        # Add validation status if available
        if "target_validation" in data and "status" in data["target_validation"]:
            validation_status.append(data["target_validation"]["status"])
        else:
            validation_status.append("N/A")

        for classifier, result in data["classification_results"].items():
            if classifier not in results:
                results[classifier] = []
            # Convert boolean or dictionary results to a numeric value for visualization
            if isinstance(result, bool):
                results[classifier].append(1 if result else 0)
            elif isinstance(result, dict):
                # For raw aggregator, calculate percentage of True values
                true_count = sum(1 for v in result.values() if v)
                total = len(result)
                results[classifier].append(true_count / total if total > 0 else 0)

    # Create a DataFrame for easier visualization
    df = pd.DataFrame({
        "Persona": personas,
        "ConversationNumber": conversation_numbers,
        "Category": categories,
        "ValidationStatus": validation_status,
        **results
    })

    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = os.path.join(OUTPUT_FOLDER, f"analysis_results_{timestamp}.csv")
    df.to_csv(csv_file, index=False)
    print(f"Analysis results saved to {csv_file}")

    # Aggregate results across multiple conversations per persona
    if len(set(zip(personas, conversation_numbers))) > len(set(personas)):
        print("Detected multiple conversations per persona. Generating aggregated visualizations...")

        # Create an aggregated DataFrame
        agg_df = pd.DataFrame()

        # Group by persona and aggregate results
        for persona_name in set(personas):
            persona_df = df[df["Persona"] == persona_name]

            # Create a row for the aggregated results
            agg_row = {
                "Persona": persona_name,
                "Category": persona_df["Category"].iloc[0],  # All should be the same
                "ConversationCount": len(persona_df),
                "ValidationPass": (persona_df["ValidationStatus"] == "PASS").mean(),
            }

            # Aggregate classifier results
            for classifier in results.keys():
                if classifier in persona_df.columns:
                    agg_row[f"{classifier}_rate"] = persona_df[classifier].mean()

            # Add to aggregated DataFrame
            agg_df = pd.concat([agg_df, pd.DataFrame([agg_row])], ignore_index=True)

        # Save aggregated results
        agg_csv_file = os.path.join(OUTPUT_FOLDER, f"aggregated_results_{timestamp}.csv")
        agg_df.to_csv(agg_csv_file, index=False)
        print(f"Aggregated results saved to {agg_csv_file}")

        # Generate aggregated visualization
        plt.figure(figsize=(12, 8))

        # For each classifier, create a bar showing detection rate
        bar_width = 0.8 / len(results)
        x = np.arange(len(agg_df))

        for i, classifier in enumerate(results.keys()):
            rate_col = f"{classifier}_rate"
            if rate_col in agg_df.columns:
                plt.bar(x + i * bar_width, agg_df[rate_col],
                        width=bar_width, label=classifier, alpha=0.7)

        plt.xlabel("Personas")
        plt.ylabel("Detection Rate")
        plt.title("Aggregated Classifier Detection Rates by Persona")
        plt.xticks(x + bar_width * (len(results) - 1) / 2, agg_df["Persona"], rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()

        # Save aggregated plot
        agg_plot_file = os.path.join(OUTPUT_FOLDER, f"aggregated_classifier_rates_{timestamp}.png")
        plt.savefig(agg_plot_file)
        print(f"Aggregated classifier rates visualization saved to {agg_plot_file}")

        # Generate validation pass rate visualization
        plt.figure(figsize=(12, 6))
        bars = plt.bar(agg_df["Persona"], agg_df["ValidationPass"], alpha=0.7)

        # Color bars according to pass rate
        for i, bar in enumerate(bars):
            pass_rate = agg_df["ValidationPass"].iloc[i]
            color = plt.cm.RdYlGn(pass_rate)  # Red to Yellow to Green color map
            bar.set_color(color)

        plt.xlabel("Personas")
        plt.ylabel("Validation Pass Rate")
        plt.title("Target Classifier Validation Pass Rate by Persona")
        plt.xticks(rotation=45, ha="right")
        plt.ylim(0, 1.1)  # Set y-axis from 0 to 1.1 to show full bars
        plt.tight_layout()

        # Save validation rate plot
        val_rate_plot_file = os.path.join(OUTPUT_FOLDER, f"validation_pass_rate_{timestamp}.png")
        plt.savefig(val_rate_plot_file)
        print(f"Validation pass rate visualization saved to {val_rate_plot_file}")

    # Generate classifier results visualization for individual conversations
    plt.figure(figsize=(15, 10))

    # Create unique labels that include conversation numbers
    labels = [f"{p}_{c}" for p, c in zip(personas, conversation_numbers)]

    for classifier in results.keys():
        plt.bar(labels, results[classifier], alpha=0.7, label=classifier)

    plt.xlabel("Persona_ConversationNumber")
    plt.ylabel("Classification Result")
    plt.title("Classification Results by Persona and Classifier")
    plt.xticks(rotation=90, ha="right")
    plt.legend()
    plt.tight_layout()

    # Save plot
    plot_file = os.path.join(OUTPUT_FOLDER, f"classification_plot_{timestamp}.png")
    plt.savefig(plot_file)
    print(f"Visualization saved to {plot_file}")

    # Generate validation status visualization
    plt.figure(figsize=(15, 6))
    status_colors = {"PASS": "green", "FAIL": "red", "SKIP": "gray", "N/A": "lightgray"}
    status_values = [1 if s == "PASS" else 0 for s in validation_status]

    bars = plt.bar(labels, status_values, alpha=0.7)

    # Color bars according to validation status
    for i, status in enumerate(validation_status):
        bars[i].set_color(status_colors.get(status, "blue"))

    plt.xlabel("Persona_ConversationNumber")
    plt.ylabel("Validation Status")
    plt.title("Target Classifier Validation Status by Persona and Conversation")
    plt.xticks(rotation=90, ha="right")
    plt.yticks([0, 1], ["FAIL", "PASS"])
    plt.tight_layout()

    # Save validation plot
    validation_plot_file = os.path.join(OUTPUT_FOLDER, f"validation_plot_{timestamp}.png")
    plt.savefig(validation_plot_file)
    print(f"Validation status visualization saved to {validation_plot_file}")

    # Create summary statistics
    pass_count = validation_status.count("PASS")
    fail_count = validation_status.count("FAIL")
    skip_count = validation_status.count("SKIP") + validation_status.count("N/A")

    # Generate summary visualization
    plt.figure(figsize=(8, 6))
    plt.pie([pass_count, fail_count, skip_count],
            labels=["PASS", "FAIL", "SKIP/N/A"],
            colors=["green", "red", "gray"],
            autopct='%1.1f%%')
    plt.title("Overall Target Classifier Validation Results")

    # Save summary plot
    summary_plot_file = os.path.join(OUTPUT_FOLDER, f"summary_plot_{timestamp}.png")
    plt.savefig(summary_plot_file)
    print(f"Summary visualization saved to {summary_plot_file}")

    # Return a summary of results for terminal output
    return {
        "total_conversations": len(personas),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "skip_count": skip_count,
        "pass_rate": pass_count / (pass_count + fail_count) if (pass_count + fail_count) > 0 else 0
    }


# Modifications for analyze_existing_conversations function

async def analyze_existing_conversations(file_path, conversation_source="hume"):
    """
    Analyze existing conversations from a file

    This function:
    1. Loads conversations from a JSON or JSONL file
    2. Runs the classifier analysis on the loaded conversations
    3. Generates visualizations of the results

    Args:
        file_path: Path to the file containing conversations to analyze
        conversation_source: Source of conversations - "generated" or "hume"
    """
    print(f"Analyzing existing conversations from {file_path} as {conversation_source} conversations...")

    # Load conversations
    conversations_data = {}
    if file_path.endswith('.jsonl'):
        raw_data = io_utils.load_jsonl(file_path)
        # Process each item in the JSONL file
        for i, item in enumerate(raw_data):
            # Generate a default unique ID for this conversation
            conversation_id = f"conversation_{i + 1}"

            if conversation_source == "hume":
                # For Hume mode, extract just the conversation without requiring persona
                if isinstance(item, list):
                    # Direct list of messages
                    conversations_data[conversation_id] = {
                        "conversation": item
                    }
                elif isinstance(item, dict):
                    # Check for chat ID in the new format
                    if "chat" in item and "chat_id" in item["chat"]:
                        conversation_id = str(item["chat"]["chat_id"])

                    # Try to find conversation data in different possible fields
                    if "conversation" in item:
                        conversations_data[conversation_id] = {
                            "conversation": item["conversation"]
                        }
                    elif "messages" in item:
                        conversations_data[conversation_id] = {
                            "conversation": item["messages"]
                        }
                    # If it has both ID and conversation, use the provided ID
                    if "id" in item and ("conversation" in item or "messages" in item):
                        conversation_id = str(item["id"])
                        conversations_data[conversation_id] = {
                            "conversation": item.get("conversation", item.get("messages", []))
                        }
            else:
                # For generated mode, still extract persona and conversation
                if "persona" in item and "conversation" in item:
                    # If there's an ID field, use it; otherwise use the index
                    if "id" in item:
                        conversation_id = str(item["id"])
                    # Check for chat ID in the new format
                    elif "chat" in item and "chat_id" in item["chat"]:
                        conversation_id = str(item["chat"]["chat_id"])
                    conversations_data[conversation_id] = item

    elif file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if conversation_source == "hume":
                # For Hume conversations in a single JSON file
                conversation_id = "conversation_1"

                # Check for chat ID in the new format
                if isinstance(data, dict) and "chat" in data and "chat_id" in data["chat"]:
                    conversation_id = str(data["chat"]["chat_id"])

                if isinstance(data, list):
                    # If it's just an array of conversation messages
                    conversations_data[conversation_id] = {
                        "conversation": data
                    }
                elif isinstance(data, dict):
                    # Try to find the conversation data in different fields
                    if "conversation" in data:
                        conversations_data[conversation_id] = {
                            "conversation": data["conversation"]
                        }
                    elif "messages" in data:
                        conversations_data[conversation_id] = {
                            "conversation": data["messages"]
                        }

                    # If there's an ID field, use it
                    if "id" in data:
                        conversation_id = str(data["id"])
                        # Update the entry with the correct ID
                        if conversation_id in conversations_data:
                            temp = conversations_data[conversation_id]
                            del conversations_data[conversation_id]
                            conversations_data[str(data["id"])] = temp
            else:
                # For generated conversations, check for persona and conversation
                if isinstance(data, dict) and "persona" in data and "conversation" in data:
                    # If there's an ID field, use it; otherwise use a default ID
                    conversation_id = str(data.get("id", "conversation_1"))
                    # Check for chat ID in the new format
                    if "chat" in data and "chat_id" in data["chat"]:
                        conversation_id = str(data["chat"]["chat_id"])
                    conversations_data[conversation_id] = data

    if not conversations_data:
        print("No valid conversations found in the provided file.")
        print("For Hume conversations, the file should contain either:")
        print("  1. A JSON array of message objects with 'role' and 'content' fields")
        print("  2. A JSON object with a 'conversation' or 'messages' field that contains the array")
        print("  3. A JSONL file where each line is one of the above formats")
        return

    # When in Hume mode, add dummy persona if needed for compatibility with run_classifier_analysis
    if conversation_source == "hume":
        for id, data in conversations_data.items():
            if "persona" not in data:
                data["persona"] = {"name": id, "target_classifiers": []}

            # Also store the chat_id in the data for later use
            if "chat_id" not in data:
                data["chat_id"] = id

    # Run analysis with the specified conversation source
    analysis_results = await run_classifier_analysis_with_rate_limits(conversations_data, conversation_source)

    print(analysis_results)

    # Visualize results
    visualize_results_hume(analysis_results)

# async def analyze_existing_conversations(file_path, conversation_source="hume"):
#     """
#     Analyze existing conversations from a file
#
#     This function:
#     1. Loads conversations from a JSON or JSONL file
#     2. Runs the classifier analysis on the loaded conversations
#     3. Generates visualizations of the results
#
#     Args:
#         file_path: Path to the file containing conversations to analyze
#         conversation_source: Source of conversations - "generated" or "hume"
#     """
#     print(f"Analyzing existing conversations from {file_path} as {conversation_source} conversations...")
#
#     # Load conversations
#     conversations_data = {}
#     if file_path.endswith('.jsonl'):
#         raw_data = io_utils.load_jsonl(file_path)
#         # Process each item in the JSONL file
#         for i, item in enumerate(raw_data):
#             # Generate a unique ID for this conversation
#             conversation_id = f"conversation_{i + 1}"
#
#             if conversation_source == "hume":
#                 # For Hume mode, extract just the conversation without requiring persona
#                 if isinstance(item, list):
#                     # Direct list of messages
#                     conversations_data[conversation_id] = {
#                         "conversation": item
#                     }
#                 elif isinstance(item, dict):
#                     # Try to find conversation data in different possible fields
#                     if "conversation" in item:
#                         conversations_data[conversation_id] = {
#                             "conversation": item["conversation"]
#                         }
#                     elif "messages" in item:
#                         conversations_data[conversation_id] = {
#                             "conversation": item["messages"]
#                         }
#                     # If it has both ID and conversation, use the provided ID
#                     if "id" in item and ("conversation" in item or "messages" in item):
#                         conversation_id = str(item["id"])
#                         conversations_data[conversation_id] = {
#                             "conversation": item.get("conversation", item.get("messages", []))
#                         }
#             else:
#                 # For generated mode, still extract persona and conversation
#                 if "persona" in item and "conversation" in item:
#                     # If there's an ID field, use it; otherwise use the index
#                     if "id" in item:
#                         conversation_id = str(item["id"])
#                     conversations_data[conversation_id] = item
#
#     elif file_path.endswith('.json'):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#
#             if conversation_source == "hume":
#                 # For Hume conversations in a single JSON file
#                 conversation_id = "conversation_1"
#
#                 if isinstance(data, list):
#                     # If it's just an array of conversation messages
#                     conversations_data[conversation_id] = {
#                         "conversation": data
#                     }
#                 elif isinstance(data, dict):
#                     # Try to find the conversation data in different fields
#                     if "conversation" in data:
#                         conversations_data[conversation_id] = {
#                             "conversation": data["conversation"]
#                         }
#                     elif "messages" in data:
#                         conversations_data[conversation_id] = {
#                             "conversation": data["messages"]
#                         }
#
#                     # If there's an ID field, use it
#                     if "id" in data:
#                         conversation_id = str(data["id"])
#                         # Update the entry with the correct ID
#                         if conversation_id in conversations_data:
#                             temp = conversations_data[conversation_id]
#                             del conversations_data[conversation_id]
#                             conversations_data[str(data["id"])] = temp
#             else:
#                 # For generated conversations, check for persona and conversation
#                 if isinstance(data, dict) and "persona" in data and "conversation" in data:
#                     # If there's an ID field, use it; otherwise use a default ID
#                     conversation_id = str(data.get("id", "conversation_1"))
#                     conversations_data[conversation_id] = data
#
#     if not conversations_data:
#         print("No valid conversations found in the provided file.")
#         print("For Hume conversations, the file should contain either:")
#         print("  1. A JSON array of message objects with 'role' and 'content' fields")
#         print("  2. A JSON object with a 'conversation' or 'messages' field that contains the array")
#         print("  3. A JSONL file where each line is one of the above formats")
#         return
#
#     # When in Hume mode, add dummy persona if needed for compatibility with run_classifier_analysis
#     if conversation_source == "hume":
#         for id, data in conversations_data.items():
#             if "persona" not in data:
#                 data["persona"] = {"name": id, "target_classifiers": []}
#
#     # Run analysis with the specified conversation source
#     analysis_results = await run_classifier_analysis_with_rate_limits(conversations_data, conversation_source)
#
#     print(analysis_results)
#
#     # Visualize results
#     visualize_results_hume(analysis_results)

# async def analyze_existing_conversations(file_path, conversation_source="hume"):
#     """
#     Analyze existing conversations from a file
#
#     This function:
#     1. Loads conversations from a JSON or JSONL file
#     2. Runs the classifier analysis on the loaded conversations
#     3. Generates visualizations of the results
#
#     Args:
#         file_path: Path to the file containing conversations to analyze
#         conversation_source: Source of conversations - "generated" or "hume"
#     """
#     print(f"Analyzing existing conversations from {file_path} as {conversation_source} conversations...")
#
#     # Load conversations
#     conversations_data = {}
#     if file_path.endswith('.jsonl'):
#         raw_data = io_utils.load_jsonl(file_path)
#         for item in raw_data:
#             if "persona" in item and "conversation" in item:
#                 persona_name = item["persona"]["name"]
#                 conversations_data[persona_name] = item
#     elif file_path.endswith('.json'):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             data = json.load(f)
#             if isinstance(data, dict) and "persona" in data and "conversation" in data:
#                 persona_name = data["persona"]["name"]
#                 conversations_data[persona_name] = data
#
#     if not conversations_data:
#         print("No valid conversations found in the provided file.")
#         return
#
#     # Run analysis with the specified conversation source
#     analysis_results = await run_classifier_analysis(conversations_data, conversation_source)
#
#     # Visualize results
#     visualize_results(analysis_results)


def generate_latex_pseudocode():
    """
    Generate LaTeX pseudocode for the target classifier validation process

    Returns:
        LaTeX code for including in a thesis
    """
    latex_code = r"""
\begin{algorithm}
\caption{Enhanced LLM Testing Framework with Multiple Conversations per Persona}
\begin{algorithmic}[1]
\Require Personas $P$, each with target classifiers $T_p$
\Require Number of conversations per persona $N$
\Ensure Evaluation reports with PASS/FAIL status

\For{each persona $p \in P$}
    \State results\_per\_persona $\gets \emptyset$

    \For{$i = 1$ to $N$} \Comment{Generate $N$ conversations per persona}
        \State conversation $\gets$ SimulateConversation($p$, NUM\_MESSAGES)
        \State results $\gets \emptyset$

        \For{each classifier $c \in T_p$}
            \State chunker $\gets$ GetChunkerType($c$) \Comment{user\_message or assistant\_message}
            \State relevant\_messages $\gets$ FilterMessagesByRole(conversation, chunker)
            \State classifier\_prompt $\gets$ GetClassifierPrompt($c$)
            \State detected $\gets$ False

            \For{each message $m \in$ relevant\_messages}
                \State detection $\gets$ EvaluateWithLLM(classifier\_prompt, $m$)
                \If{detection is True}
                    \State detected $\gets$ True
                    \State \textbf{break}
                \EndIf
            \EndFor

            \State results[c] $\gets$ detected
        \EndFor

        \State Save(conversation, $p$, $i$) \Comment{Save as separate file with index}
        \State results\_per\_persona[$i$] $\gets$ results
    \EndFor

    \State aggregated\_results $\gets \emptyset$
    \For{each classifier $c \in T_p$}
        \State detection\_count $\gets$ Count(results\_per\_persona, $c$, True)
        \State detection\_rate $\gets$ detection\_count / $N$
        \If{detection\_rate $\geq$ threshold} \Comment{e.g., threshold = 0.5}
            \State aggregated\_results[$c$] $\gets$ True
        \Else
            \State aggregated\_results[$c$] $\gets$ False
        \EndIf
    \EndFor

    \If{$\forall c \in T_p : $ aggregated\_results[$c$] = True}
        \State status $\gets$ "PASS"
    \Else
        \State status $\gets$ "FAIL"
    \EndIf

    \State SaveResults($p$, aggregated\_results, status)
\EndFor

\State GenerateVisualizations(all\_results)
\end{algorithmic}
\end{algorithm}
"""
    return latex_code


async def main():
    """
    Main entry point for the Lindra Toolkit

    Command-line arguments:
        --generate: Generate new conversations with personas
        --analyze PATH: Analyze existing conversations at the specified path
        --messages NUM: Number of messages in each conversation (default: 6)
        --classifier-set SET: Classifier set version to use (default: v1)
        --convert-to-csv PATH: Convert a JSON conversation file to CSV format
        --output-folder PATH: Folder where to save the converted CSV file (optional)
        --latex-pseudocode: Generate LaTeX pseudocode for the thesis
        --conversation-source TYPE: Specify the source of conversations (generated or hume)
        --conversations-per-persona NUM: Number of conversations to generate for each persona (default: 3)

    Examples:
        # Generate new conversations (3 per persona by default)
        python main.py --generate

        # Generate 5 conversations per persona
        python main.py --generate --conversations-per-persona 5

        # Analyze existing conversations using all classifiers (Hume mode)
        python main.py --analyze all_conversations_test.jsonl --conversation-source hume

        python main.py --analyze split_conversations/conversations_part_1.jsonl --conversation-source hume

        # Analyze existing conversations using only target classifiers (Generated mode)
        python main.py --analyze conversations_output/all_conversations.jsonl --conversation-source generated

        # Generate longer conversations
        python main.py --generate --messages 10

        # Convert a JSON conversation to CSV
        python main.py --convert-to-csv conversations_output/Maya_Cognitive_restructuring.json

        # Generate LaTeX pseudocode for thesis
        python main.py --latex-pseudocode
    """
    # Declare globals at the beginning of the function before using them
    global NUM_MESSAGES, CLASSIFIER_SET

    parser = argparse.ArgumentParser(description="Lindra Toolkit: Generate and analyze conversations")
    parser.add_argument("--generate", action="store_true", help="Generate new conversations")
    parser.add_argument("--analyze", type=str, help="Path to existing conversations to analyze")
    parser.add_argument("--messages", type=int, default=NUM_MESSAGES, help="Number of messages in each conversation")
    parser.add_argument("--classifier-set", type=str, default=CLASSIFIER_SET, help="Classifier set version")
    parser.add_argument("--convert-to-csv", type=str, help="Path to JSON conversation file to convert to CSV")
    parser.add_argument("--output-folder", type=str, help="Folder to save the converted CSV file")
    parser.add_argument("--latex-pseudocode", action="store_true", help="Generate LaTeX pseudocode for thesis")
    parser.add_argument("--conversation-source", type=str, default="generated",
                        choices=["generated", "hume"],
                        help="Source of conversations - determines classifier usage")
    parser.add_argument("--conversations-per-persona", type=int, default=3,
                        help="Number of conversations to generate for each persona")

    args = parser.parse_args()

    # Update global settings
    NUM_MESSAGES = args.messages
    CLASSIFIER_SET = args.classifier_set
    CONVERSATION_SOURCE = args.conversation_source
    CONVERSATIONS_PER_PERSONA = args.conversations_per_persona

    ensure_output_dir()

    if args.latex_pseudocode:
        # Generate LaTeX pseudocode
        latex_code = generate_latex_pseudocode()
        latex_file = os.path.join(OUTPUT_FOLDER, "target_classifier_validation_pseudocode.tex")
        with open(latex_file, 'w', encoding='utf-8') as f:
            f.write(latex_code)
        print(f"LaTeX pseudocode saved to {latex_file}")
    elif args.generate:
        # Generate new conversations with the specified number per persona
        conversations = generate_conversations(CONVERSATIONS_PER_PERSONA)
        # Analyze the generated conversations (using target classifiers)
        analysis_results = await run_classifier_analysis(conversations, "generated")
        # Visualize results
        visualization_summary = visualize_results(analysis_results)

        # Display summary
        print("\nSummary of Analysis Results:")
        print(f"  Total conversations analyzed: {visualization_summary['total_conversations']}")
        print(f"  PASS: {visualization_summary['pass_count']} ({visualization_summary['pass_rate']:.1%})")
        print(f"  FAIL: {visualization_summary['fail_count']}")
        print(f"  SKIP/N/A: {visualization_summary['skip_count']}")
    elif args.analyze:
        # Analyze existing conversations with the specified source type
        await analyze_existing_conversations(args.analyze, CONVERSATION_SOURCE)
    elif args.convert_to_csv:
        # Convert JSON conversation to CSV
        convert_json_to_csv(args.convert_to_csv, args.output_folder)
    else:
        print("Please specify one of the following options:")
        print("  --generate: To create new conversations")
        print("  --analyze PATH: To analyze existing conversations")
        print("  --convert-to-csv PATH: To convert a JSON conversation to CSV format")
        print("  --latex-pseudocode: To generate LaTeX pseudocode for thesis")
        print("\nAdditional options:")
        print("  --conversation-source [generated|hume]: Specify the source of conversations")
        print("    - generated: Use only target classifiers defined in personas")
        print("    - hume: Use all available classifiers")
        print("  --conversations-per-persona NUM: Number of conversations to generate for each persona (default: 3)")


if __name__ == "__main__":
    asyncio.run(main())
