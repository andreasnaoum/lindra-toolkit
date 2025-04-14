# Lindra Evaluation Framework

A comprehensive framework for evaluating and analyzing Lindra, an Empathetic Conversational Agent for Pain Self-Management and Well-Being. This repository contains tools for simulating conversations with different user personas, classifying conversation content, and analyzing therapeutic effectiveness.

## Overview

The Lindra Evaluation Framework employs a dual-LLM approach to test and analyze AI assistant interactions related to pain management. It uses:

1. **Simulated Personas**: Testing with diverse user profiles representing different pain conditions and psychological needs
2. **Conversation Generation**: Claude-powered simulation of user-assistant interactions
3. **Emotion Classification**: Analysis of user emotional states and expressions
4. **Response Classification**: Validation of appropriate assistant interventions
5. **Performance Analysis**: Systematic evaluation across system versions

## Repository Structure

```
lindra-evaluation-framework/
├── personas/                # Simulated user personas for testing
├── classifiers/             # Emotion and response classifiers
├── simulation/              # Conversation simulation scripts
├── analysis/                # Data processing and analysis tools
├── results/                 # Test results and visualizations
└── docs/                    # Documentation and methodology
```

## Evaluation Components

### Dual-LLM Testing Approach

- **Claude**: Powers the conversation simulation system, generating realistic user interactions based on persona profiles and previous conversation context
- **ChatGPT**: Implements classification models for evaluating conversations, detecting emotional states, and validating therapeutic responses

### Persona-Based Testing

The framework includes 12+ personas representing different:
- Pain conditions (arthritis, back pain, fibromyalgia, etc.)
- Psychological profiles (catastrophizing, avoidance, etc.)
- Communication styles (expressive, analytical, minimal, etc.)
- Therapeutic needs (cognitive restructuring, behavioral activation, etc.)

## Analysis Components

### Conversation Analysis (Hume)

The Hume integration provides:
- Emotional expression detection in user messages
- Conversation event tracking and analysis
- Transcript generation with emotional annotation
- Export of conversations to CSV and single-line JSON formats

### Classifier Analysis (ChatGPT)

The classifier system evaluates:
- User needs and emotional states (pain catastrophizing, fear of movement, etc.)
- Assistant therapeutic techniques (cognitive restructuring, behavioral activation, etc.)
- Appropriate recognition and response matching

## Getting Started

### Prerequisites

```
python >= 3.8
anthropic
openai
hume-python
pandas
numpy
matplotlib
```

### Installation

```bash
git clone https://github.com/yourusername/lindra-evaluation-framework.git
cd lindra-evaluation-framework
pip install -r requirements.txt
```

### Configuration

Add your API keys to a `.env` file:

```
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
HUME_API_KEY=your_hume_key
```

### Running a Test

```bash
# Run a simulation with all personas
python simulation/run_simulations.py

# Run a specific test case
python simulation/run_simulations.py --persona=maya

# Analyze conversation results
python analysis/analyze_conversations.py --input=results/conversations.jsonl

# Generate summary report
python analysis/generate_report.py --input=results/analysis.json --output=results/report.pdf
```

## Technical Validation

The framework provides technical validation through:
1. Testing across multiple system versions
2. Paired classifier evaluation (input pattern → appropriate response)
3. Quantitative performance metrics (pass/fail rates by capability area)
4. Conversation transcript analysis with emotional tracking

## License

MIT

## Citation

If you use this framework in your research, please cite:

```
@software{lindra_evaluation_framework,
  author = {Your Name},
  title = {Lindra Evaluation Framework},
  year = {2023},
  url = {https://github.com/yourusername/lindra-evaluation-framework}
}
```

## Acknowledgments

This framework builds on concepts from cognitive behavioral therapy for chronic pain and leverages multiple AI systems for testing and analysis.
