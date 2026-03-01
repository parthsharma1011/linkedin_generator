# LinkedIn Post Generator - Multi-Agent System

Professional LinkedIn post generator with Gradio UI using CrewAI multi-agent system.

## Features

- 🎨 **Gradio Web UI** - Simple interface for generating posts
- 🔍 **Research Agent** - Uses Tavily API to find recent data and trends
- ✍️ **Writer Agent** - Crafts engaging posts following LinkedIn best practices  
- ✅ **Validator Agent** - Ensures accuracy, authenticity, and quality

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file:
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

3. Run locally:
   ```bash
   python gradio_app.py
   ```

4. Open browser: http://localhost:7860

## Usage

The UI allows you to:
- **Topic**: What you want to write about
- **Tone**: professional, casual, thought-leader
- **Post Type**: story, hot-take, announcement, lesson-learned, thought-leader

## Deploy to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## Output

- Complete LinkedIn post ready to copy/paste
- Validation score and suggestions
- Word count and research source count