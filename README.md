# Lindra Toolkit

A comprehensive toolkit for developing, testing, and analyzing Lindra, an AI assistant specialized in pain self-management and well-being support. This toolkit provides tools for simulating conversations with different user personas, classifying conversation content, and analyzing therapeutic effectiveness.

## Overview

The Lindra Toolkit employs a multi-component approach to develop and analyze AI assistant interactions related to pain management:

1. **LLM-Test Framework**: Generate simulated conversations between Lindra and various user personas
2. **Classifiers**: Analyze conversation content for therapeutic techniques and user emotional states
3. **Hume Integration**: Advanced emotion analysis in conversations
4. **Visualization Tools**: Generate insights from conversation analysis

## Repository Structure

```
lindra-toolkit/
├── Classifiers/               # Emotion and response classifiers
│   ├── assets/                # Classifier definitions
│   └── emoclassifiers/        # Classification implementation
├── Hume/                      # Hume API integration for emotion analysis
├── LLM-Test/                  # Conversation simulation framework  
│   └── Personas/              # Simulated user personas
├── main.py                    # Main toolkit entry point
└── requirements.txt           # Required dependencies
```

## Components

### LLM-Test Framework

- Simulates realistic user-assistant conversations using Claude
- Includes diverse personas with different pain conditions, psychological profiles, and communication styles
- Saves conversations in structured formats (JSON, JSONL, and CSV) for analysis

### Classifiers

- Includes pre-defined classifiers for evaluating conversations
- Detects therapeutic techniques like cognitive restructuring
- Identifies user states like fear of movement or pain catastrophizing
- Uses chunking to analyze conversations at different levels (message, exchange, whole conversation)

### Hume Integration

- Provides advanced emotion analysis capabilities
- Generates emotion transcripts with confidence scores
- Identifies dominant emotions across conversations

## Getting Started

### Prerequisites

```
python >= 3.8
```

### Installation

```bash
git clone https://github.com/yourusername/lindra-toolkit.git
cd lindra-toolkit
pip install -r requirements.txt
```

### Configuration

Create a `.env` file with your API keys:

```
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
HUME_API_KEY=your_hume_key
```

### Usage

#### Generate and Analyze Conversations

```bash
# Generate new conversations and analyze them
python main.py --generate

# Analyze existing conversations
python main.py --analyze path/to/conversations.jsonl

# Customize the number of messages
python main.py --generate --messages 8

# Convert a JSON conversation to CSV format
python main.py --convert-to-csv path/to/conversation.json

# Convert a JSON conversation to CSV format with custom output folder
python main.py --convert-to-csv path/to/conversation.json --output-folder custom/output/folder
```

#### Run Classifiers Independently

```bash
# Run classifiers on existing conversations
python Classifiers/run_simple_classification.py --input_path path/to/conversations.jsonl --output_path results.json
```

#### Run Hume Analysis

```bash
# Analyze emotions using Hume API
python Hume/analysis.py
```

## Classifier Definitions

The toolkit includes predefined classifiers for:

- **Cognitive Restructuring**: Detecting when the assistant helps modify negative thoughts
- **Fear of Movement**: Identifying user avoidance of physical activity
- **Pain-Related Frustration**: Detecting user expressions of anger or irritability
- **Support Seeking**: Identifying when users seek emotional support

## Personas

The toolkit includes diverse personas such as:

- **Ethan**: Coping with chronic low back pain and negative core beliefs
- **Nadia**: Experiencing migraines with hypervigilance and control issues
- **Elaine**: Managing fibromyalgia with activity avoidance behaviors
- **Leo**: Dealing with mild work-related back discomfort

## License

MIT

## Acknowledgments

This toolkit builds on concepts from cognitive behavioral therapy for chronic pain and leverages AI systems for testing and analysis.