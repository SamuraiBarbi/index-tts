#!/bin/bash

# Streaming API with Base64 - Using file to avoid argument length limit

VOICE_FILE="${1:-/home/owner/Documents/projects/Ronin/ronin/resources/voices_friends/Trener99.wav}"
OUTPUT_FILE="${2:-playful_streaming.bin}"

echo "🎤 Encoding voice file: $VOICE_FILE"

# Encode to base64 and save to temp file to avoid shell escaping issues
base64 -w 0 "$VOICE_FILE" > /tmp/voice_base64.txt

echo "📝 Creating request payload..."

# Use Python to create proper JSON with base64 data
python3 << 'PYTHON_EOF'
import json

with open('/tmp/voice_base64.txt', 'r') as f:
    voice_base64 = f.read().strip()

request_data = {
    "model": "IndexTTS2",
    "input": "ok, but i eat ass on the first date, so?",
    "voice": "base64_voice",
    "voice_base64": voice_base64,
    "emotion_text": "playful, joking, friendly",
    "emotion_weight": 0.8,
    "stream": True,
    "response_format": "mp3"
}

with open('/tmp/streaming_request.json', 'w') as f:
    json.dump(request_data, f)
PYTHON_EOF

echo "🚀 Sending streaming request..."
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d @/tmp/streaming_request.json \
  --no-buffer \
  --output "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Streaming response saved to: $OUTPUT_FILE"
    ls -lh "$OUTPUT_FILE"
    
    # Clean up
    rm -f /tmp/streaming_request.json /tmp/voice_base64.txt
else
    echo ""
    echo "❌ Request failed"
    rm -f /tmp/streaming_request.json /tmp/voice_base64.txt
    exit 1
fi
