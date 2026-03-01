# Deployment Setup Guide

## Quick Start - Run Locally

```bash
cd /Users/parthsharma/Desktop/linkedin_generator
./run_gradio.sh
```

Open browser: http://localhost:7860

## Deploy to Render

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select repository: `parthsharma1011/linkedin_generator`
5. Configure:
   - **Name**: `linkedin-generator`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Instance Type**: Free

6. Add Environment Variables:
   - `GOOGLE_API_KEY`: Your Google API key
   - `TAVILY_API_KEY`: Your Tavily API key
   - `PORT`: 7860

7. Click "Create Web Service"

## Features

- 📝 Simple UI to enter topic, tone, and post type
- 🤖 AI-powered research and writing
- ✅ Automatic validation and suggestions
- 📊 Word count and quality score

## Test Locally with Docker

```bash
docker build -t linkedin-generator .
docker run -p 7860:7860 --env-file .env linkedin-generator
```

Visit: http://localhost:7860
