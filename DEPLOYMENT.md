# Deployment Setup Guide

## Step 1: Create GitHub Personal Access Token

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name: `linkedin-generator-deploy`
4. Select scopes: `repo` (all), `workflow`
5. Generate and copy the token

## Step 2: Initialize Git and Push to GitHub

```bash
cd /Users/parthsharma/Desktop/linkedin_generator
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/linkedin-generator.git
git push -u origin main
```

## Step 3: Create Docker Hub Account & Token

1. Sign up at https://hub.docker.com
2. Go to Account Settings → Security → New Access Token
3. Name: `github-actions`
4. Copy the token

## Step 4: Set GitHub Secrets

Go to your GitHub repo → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token
- `RENDER_DEPLOY_HOOK`: (Get this from Render in next step)

## Step 5: Setup Render

1. Sign up at https://render.com
2. New → Web Service
3. Select "Deploy an existing image from a registry"
4. Image URL: `docker.io/YOUR_DOCKER_USERNAME/linkedin-generator:latest`
5. Name: `linkedin-generator`
6. Add Environment Variables:
   - `GOOGLE_API_KEY`: Your Google API key
   - `TAVILY_API_KEY`: Your Tavily API key
   - `PORT`: 5000
7. Create Web Service
8. Go to Settings → Deploy Hook → Copy the URL
9. Add this URL as `RENDER_DEPLOY_HOOK` secret in GitHub

## Step 6: Deploy

Push any change to main branch:
```bash
git add .
git commit -m "Trigger deployment"
git push
```

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
