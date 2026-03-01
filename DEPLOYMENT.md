# Deployment Setup Guide

## Step 1: Setup Render

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
   - `PORT`: 5000

7. Click "Create Web Service"

## Step 2: Get Deploy Hook (Optional - for auto-deploy)

1. In Render dashboard → Your service → Settings
2. Scroll to "Deploy Hook"
3. Copy the URL
4. Go to GitHub repo → Settings → Secrets → Actions
5. Add secret: `RENDER_DEPLOY_HOOK` with the URL

## Step 3: Deploy

Render will auto-deploy on every push to main branch.

Or manually trigger from Render dashboard → Manual Deploy

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check
- `POST /generate` - Generate LinkedIn post
  ```json
  {
    "topic": "AI in healthcare",
    "tone": "professional",
    "post_type": "thought-leader"
  }
  ```

## Test Locally

```bash
docker build -t linkedin-generator .
docker run -p 5000:5000 --env-file .env linkedin-generator
```

Visit: http://localhost:5000
