#!/bin/bash

echo "🧪 Testing IndexTTS2 API"
echo "========================"
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
curl -s http://localhost:8889/health | jq .
echo ""

# Test 2: Simple Speech Generation
echo "Test 2: Generating speech..."
curl -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "IndexTTS2",
    "input": "Hello world",
    "voice": "alex",
    "response_format": "mp3"
  }' \
  --output test_simple.mp3 \
  -w "\nHTTP Status: %{http_code}\n"

if [ -f "test_simple.mp3" ] && [ -s "test_simple.mp3" ]; then
    echo "✅ Speech generated successfully!"
    ls -lh test_simple.mp3
    echo ""
    echo "Play with: mpg123 test_simple.mp3"
else
    echo "❌ Speech generation failed"
fi
