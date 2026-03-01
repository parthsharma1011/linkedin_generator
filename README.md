# LinkedIn Post Generator - Multi-Agent System

Professional LinkedIn post generator using CrewAI with research, writing, and validation agents.

## Features

- **Research Agent**: Uses Tavily API to find recent data and trends
- **Writer Agent**: Crafts engaging posts following LinkedIn best practices  
- **Validator Agent**: Ensures accuracy, authenticity, and quality

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. API keys are already configured in `.env`

3. Run the generator:
   ```bash
   python linkedin_generator.py
   ```

## Usage

The script will prompt you for:
- **Topic**: What you want to write about
- **Tone**: professional, casual, thought-leader
- **Post Type**: story, hot-take, announcement, lesson-learned

## Output

- Complete LinkedIn post ready to copy/paste
- Validation score and suggestions
- Word count and research source count

The system automatically researches your topic, writes an engaging post, and validates it for quality before presenting the final result.