#!/bin/bash

echo "Starting LinkedIn Generator Gradio App..."
echo "=========================================="

if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    exit 1
fi

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Gradio app on http://localhost:7860"
echo "Press Ctrl+C to stop"
echo ""

python gradio_app.py
