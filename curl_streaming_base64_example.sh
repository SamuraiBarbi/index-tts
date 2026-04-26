#!/bin/bash

# Example: Streaming API with Base64 Reference Audio

echo "Encoding reference audio to base64..."
VOICE_BASE64=$(base64 -w 0 examples/SamuraiBarbi.wav)

echo "Sending streaming request with base64 voice..."
echo ""

curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"IndexTTS2\",
    \"input\": \"First sentence here. Second sentence follows. Third sentence complete.\",
    \"voice\": \"base64_voice\",
    \"voice_base64\": \"$VOICE_BASE64\",
    \"stream\": true,
    \"response_format\": \"mp3\"
  }" \
  --no-buffer \
  --output streaming_base64_output.bin

echo ""
echo "✅ Streaming response saved to streaming_base64_output.bin"
echo ""
echo "Note: The output contains metadata lines (JSON) followed by audio chunks."
echo "To extract just the audio, you'll need to parse the metadata and combine chunks."
