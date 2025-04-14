from assistant import ASSISTANT_PROMPT
from personas import *
from user import USER_PROMPT_TEMPLATE

import json
import random
import argparse
import os
import requests
import time
import sys
import csv
import os
from dotenv import load_dotenv
import anthropic

# Load environment variables from .env file
load_dotenv()

# Retrieve API key securely
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
NUM_MESSAGES = 6
OUTPUT_FILE = "simulated_conversations.jsonl"
OUTPUT_FOLDER = "personas_conversations"

# Create output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)


def retry_with_backoff(func):
    def wrapper(*args, **kwargs):
        retries = 3
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except (anthropic.RateLimitError, anthropic.APIError) as e:
                if attempt == retries - 1:
                    raise
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry attempt {attempt + 1}. Waiting {wait_time} seconds.")
                time.sleep(wait_time)

    return wrapper


@retry_with_backoff
def get_simulated_user_message(persona, conversation_history, message_index):
    """Generate a message from the simulated user using Claude API."""

    # Create prompt with conversation context
    prompt = USER_PROMPT_TEMPLATE.format(**persona)

    # Add conversation history to provide context
    if conversation_history:
        prompt += "\n\nHere's the conversation so far:\n"
        for message in conversation_history:
            if message["role"] == "assistant":
                prompt += f"Lindra: {message['content']}\n"
            else:
                # Strip the emotion expressions when showing the conversation history
                user_content = message["content"]
                if "(" in user_content and user_content.endswith(")"):
                    user_content = user_content[:user_content.rfind("(")].strip()
                prompt += f"You: {user_content}\n"

    # Add instruction for the next message if it's the first one
    if message_index == 0:
        prompt += "\nThis is your first message to Lindra. Introduce yourself briefly and mention your pain condition."
    else:
        prompt += "\nRespond to Lindra's last message."

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            max_tokens=1000,
            temperature=1,
            messages=[
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        )
        user_message = message.content[0].text.strip()

        # Check if the message already has emotion expressions
        if not (user_message.endswith(")") and "(" in user_message):
            # If not, add default emotions based on the persona's psychological profile
            if "catastrophizing" in persona["psychological_profile"].lower():
                user_message += " (Anxiety 0.8, Fear 0.7, Pain 0.9)"
            elif "depression" in persona["psychological_profile"].lower():
                user_message += " (Sadness 0.8, Pain 0.7, Tiredness 0.6)"
            elif "frustrated" in persona["psychological_profile"].lower():
                user_message += " (Frustration 0.8, Anger 0.7, Pain 0.6)"
            else:
                user_message += " (Pain 0.7, Anxiety 0.6, Determination 0.5)"

        return user_message
    except Exception as e:
        print(f"Error generating user message: {e}")
        # Fallback to a simple message if API fails
        return f"Problem"


@retry_with_backoff
def get_assistant_response(conversation_history, lindra_prompt=""):
    """Get a response from Lindra using Claude API."""

    # Format messages for the API call
    messages = []
    for message in conversation_history:
        messages.append({
            "role": message["role"],
            "content": [{"type": "text", "text": message["content"]}]
        })

    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-latest",
            system=lindra_prompt,
            max_tokens=1600,
            messages=messages
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error getting assistant response: {e}")
        return "Error getting response"


def simulate_conversation(persona, num_messages=10, lindra_prompt=""):
    """Simulate a conversation between Lindra and a user with the given persona."""
    conversation = []

    # First user message
    user_message = get_simulated_user_message(persona, conversation, 0)
    conversation.append({"role": "user", "content": user_message})

    # Simulate the conversation for the specified number of messages
    for i in range(num_messages):
        # Get assistant response
        assistant_response = get_assistant_response(conversation, ASSISTANT_PROMPT)
        conversation.append({"role": "assistant", "content": assistant_response})

        # Get next user message
        if i < num_messages - 1:  # Only get next user message if not the last iteration
            user_message = get_simulated_user_message(persona, conversation, i + 1)
            conversation.append({"role": "user", "content": user_message})

        # Add a small delay to avoid rate limiting
        time.sleep(1)

    return conversation


def save_conversation_to_csv(persona, conversation, folder):
    """Save a conversation to a CSV file."""
    filename = os.path.join(folder, f"{persona['name']}_{persona['specific_focus'].replace(' ', '_')}.csv")

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['turn', 'role', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, message in enumerate(conversation):
            writer.writerow({
                'turn': i + 1,
                'role': message['role'],
                'content': message['content']
            })

    return filename


def save_conversation_to_json(persona, conversation, folder):
    """Save a conversation to a single-line JSON file."""
    filename = os.path.join(folder, f"{persona['name']}_{persona['specific_focus'].replace(' ', '_')}.json")

    # Create a dictionary with persona info and conversation
    data = {
        "persona": persona,
        "conversation": conversation
    }

    # Write to file as a single line
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return filename


def save_all_conversations_to_jsonl(all_conversations, filename):
    """Save all conversations to a JSONL file, each conversation as a single JSON line."""
    with open(filename, 'w', encoding='utf-8') as f:
        for persona_name, data in all_conversations.items():
            # Convert each conversation to a single JSON line
            f.write(json.dumps(data) + '\n')


def main():
    all_conversations = {}

    # Simulate conversations for each selected persona
    for i, persona in enumerate(personas):
        print(
            f"Simulating conversation {i + 1}/{len(personas)} with {persona['name']} ({persona['test_category']}: {persona['specific_focus']})...")

        conversation = simulate_conversation(persona, NUM_MESSAGES, ASSISTANT_PROMPT)

        # Save individual conversation to CSV
        csv_filename = save_conversation_to_csv(persona, conversation, OUTPUT_FOLDER)
        print(f"Saved CSV to {csv_filename}")

        # Save individual conversation to JSON (single line)
        json_filename = save_conversation_to_json(persona, conversation, OUTPUT_FOLDER)
        print(f"Saved JSON to {json_filename}")

        # Add to all conversations dictionary
        all_conversations[persona['name']] = {
            "persona": persona,
            "conversation": conversation
        }

        print(f"Completed conversation with {persona['name']}")

    # Save all conversations to JSONL file (one JSON object per line)
    all_conversations_file = os.path.join(OUTPUT_FOLDER, "all_conversations.jsonl")
    save_all_conversations_to_jsonl(all_conversations, all_conversations_file)
    print(f"All conversations saved to {all_conversations_file}")


if __name__ == "__main__":
    main()
