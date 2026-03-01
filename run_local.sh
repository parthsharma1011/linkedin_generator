#!/bin/bash

echo "Starting LinkedIn Generator API locally..."
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please create .env file with:"
    echo "  GOOGLE_API_KEY=your_key"
    echo "  TAVILY_API_KEY=your_key"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run Flask app
echo ""
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

PORT=8000 python app.py
