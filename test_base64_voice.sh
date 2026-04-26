#!/bin/bash

# Test base64 voice without streaming (WAV format to avoid ffmpeg issue)

VOICE_FILE="${1:-/home/owner/Documents/projects/Ronin/ronin/resources/voices_friends/Trener99.wav}"
OUTPUT_FILE="${2:-trener_test.wav}"

echo "🎤 Encoding voice file: $VOICE_FILE"
base64 -w 0 "$VOICE_FILE" > /tmp/voice_base64.txt

echo "📝 Creating request payload..."
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
    "stream": False,
    "response_format": "wav"
}

with open('/tmp/test_request.json', 'w') as f:
    json.dump(request_data, f)
PYTHON_EOF

echo "🚀 Sending request (WAV format, no streaming)..."
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d @/tmp/test_request.json \
  --output "$OUTPUT_FILE" \
  -w "\nHTTP Status: %{http_code}\n"

if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    echo ""
    echo "✅ Audio saved to: $OUTPUT_FILE"
    ls -lh "$OUTPUT_FILE"
    file "$OUTPUT_FILE"
    rm -f /tmp/test_request.json /tmp/voice_base64.txt
else
    echo ""
    echo "❌ Request failed"
    cat "$OUTPUT_FILE"
    rm -f /tmp/test_request.json /tmp/voice_base64.txt
    exit 1
fi
