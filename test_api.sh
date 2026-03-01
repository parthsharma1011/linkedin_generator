#!/bin/bash

BASE_URL="http://localhost:8000"

echo "Testing LinkedIn Generator API"
echo "==============================="
echo ""

# Test 1: Health check
echo "1. Testing /health endpoint..."
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""

# Test 2: Home endpoint
echo "2. Testing / endpoint..."
curl -s "$BASE_URL/" | python3 -m json.tool
echo ""

# Test 3: Generate post
echo "3. Testing /generate endpoint..."
curl -s -X POST "$BASE_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI in software development",
    "tone": "professional",
    "post_type": "thought-leader"
  }' | python3 -m json.tool

echo ""
echo "Tests completed!"
