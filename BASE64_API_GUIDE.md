# Base64 Audio Support for IndexTTS2 API

## Overview

The IndexTTS2 API now supports **base64 encoded audio** for both voice and emotion reference audio. This allows you to send audio data directly in the API request without needing to upload files to the server.

## Benefits

- ✅ **No file uploads required** - Send audio data directly in JSON
- ✅ **Stateless operation** - No need to manage files on the server
- ✅ **Dynamic voices** - Use different voices without pre-uploading
- ✅ **Secure** - Audio data doesn't persist on the server
- ✅ **Flexible** - Mix file-based and base64 references

## Usage

### Option 1: Voice Reference from File (Original Method)

```json
{
  "model": "IndexTTS2",
  "input": "Hello, this is a test.",
  "voice": "alex",
  "response_format": "mp3"
}
```

The API looks for `characters/alex.wav` on the server.

### Option 2: Voice Reference from Base64 (New Method)

```json
{
  "model": "IndexTTS2",
  "input": "Hello, this is a test.",
  "voice": "placeholder",
  "voice_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
  "response_format": "mp3"
}
```

The API decodes the base64 audio data and uses it as the voice reference.

## API Parameters

### New Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `voice_base64` | string | Base64 encoded audio data for voice reference (alternative to `voice` filename) |
| `emotion_voice_base64` | string | Base64 encoded audio data for emotion reference (alternative to `emotion_voice` filename) |

### Priority

- If `voice_base64` is provided, it takes priority over the `voice` filename
- If `emotion_voice_base64` is provided, it takes priority over the `emotion_voice` filename

## Examples

### Example 1: Basic Base64 Voice Reference

**Python:**

```python
import requests
import base64

# Read and encode audio file
with open('my_voice.wav', 'rb') as f:
    voice_data = base64.b64encode(f.read()).decode('utf-8')

# Make API request
response = requests.post(
    'http://localhost:8000/v1/audio/speech',
    headers={
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'IndexTTS2',
        'input': 'Hello from base64 voice!',
        'voice': 'base64_voice',
        'voice_base64': voice_data,
        'response_format': 'mp3'
    }
)

with open('output.mp3', 'wb') as f:
    f.write(response.content)
```

**JavaScript:**

```javascript
// Read file and convert to base64
const fs = require('fs');
const voiceData = fs.readFileSync('my_voice.wav').toString('base64');

// Make API request
fetch('http://localhost:8000/v1/audio/speech', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer test_token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'IndexTTS2',
    input: 'Hello from base64 voice!',
    voice: 'base64_voice',
    voice_base64: voiceData,
    response_format: 'mp3'
  })
})
.then(res => res.blob())
.then(blob => {
  // Save or play the audio
});
```

**curl:**

```bash
# First, encode the audio file
VOICE_BASE64=$(base64 -w 0 my_voice.wav)

# Make the API request
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"IndexTTS2\",
    \"input\": \"Hello from base64 voice!\",
    \"voice\": \"base64_voice\",
    \"voice_base64\": \"$VOICE_BASE64\",
    \"response_format\": \"mp3\"
  }" \
  --output output.mp3
```

### Example 2: Base64 Voice + Emotion Reference

```python
import requests
import base64

# Encode voice and emotion files
with open('my_voice.wav', 'rb') as f:
    voice_data = base64.b64encode(f.read()).decode('utf-8')

with open('happy_emotion.wav', 'rb') as f:
    emotion_data = base64.b64encode(f.read()).decode('utf-8')

# Make API request with both
response = requests.post(
    'http://localhost:8000/v1/audio/speech',
    headers={
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'IndexTTS2',
        'input': 'I am so excited about this!',
        'voice': 'base64_voice',
        'voice_base64': voice_data,
        'emotion_voice_base64': emotion_data,
        'emotion_weight': 0.8,
        'response_format': 'mp3'
    }
)
```

### Example 3: Mix File and Base64

You can mix file-based and base64 references:

```python
# Use file for voice, base64 for emotion
response = requests.post(
    'http://localhost:8000/v1/audio/speech',
    headers={
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'IndexTTS2',
        'input': 'Mixed reference example',
        'voice': 'alex',  # Uses characters/alex.wav
        'emotion_voice_base64': emotion_data,  # Uses base64
        'emotion_weight': 0.7,
        'response_format': 'mp3'
    }
)
```

## Using the Python Client

A dedicated client example is provided:

```bash
python api_client_base64_example.py \
  --text "Hello from base64!" \
  --voice-file examples/voice_01.wav \
  --output test.mp3
```

**With emotion:**

```bash
python api_client_base64_example.py \
  --text "I'm so happy!" \
  --voice-file examples/voice_01.wav \
  --emotion-file examples/emo_happy.wav \
  --emotion-weight 0.8 \
  --output happy.mp3
```

## Data URI Format Support

The API also supports Data URI format (commonly used in web browsers):

```json
{
  "voice_base64": "data:audio/wav;base64,UklGRiQAAABXQVZFZm10IB..."
}
```

The API automatically strips the `data:audio/wav;base64,` prefix.

## Audio Format Requirements

- **Recommended format**: WAV (uncompressed)
- **Sample rate**: Any (will be processed by the model)
- **Channels**: Mono or Stereo
- **Duration**: 5-10 seconds recommended for best results

## Size Considerations

Base64 encoding increases data size by ~33%. For example:
- 1 MB audio file → ~1.33 MB base64 string
- 5 MB audio file → ~6.65 MB base64 string

**Recommendations:**
- For frequently used voices, use the file-based method
- For dynamic/one-time voices, use base64
- Consider compressing audio before encoding (but keep quality high)

## Complete Request Example

```json
{
  "model": "IndexTTS2",
  "input": "This is a complete example with all features.",
  "voice": "placeholder",
  "voice_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEA...",
  "emotion_voice_base64": "UklGRjQBAABXQVZFZm10IBAAAAABAAEA...",
  "emotion_weight": 0.7,
  "response_format": "mp3",
  "sample_rate": 24000,
  "speed": 1.0,
  "gain": 0.0,
  "temperature": 0.8,
  "top_p": 0.8,
  "do_sample": true
}
```

## Error Handling

### Invalid Base64 Data

```json
{
  "detail": "Invalid base64 audio data: Incorrect padding"
}
```

**Solution:** Ensure the base64 string is properly encoded.

### Corrupted Audio Data

```json
{
  "detail": "Failed to process audio file"
}
```

**Solution:** Verify the audio file is valid before encoding.

## Performance Notes

- Base64 decoding is fast and adds minimal overhead
- Temporary files are automatically cleaned up after generation
- No persistent storage of base64 audio data
- Memory usage is proportional to audio file size

## Security Considerations

1. **Size limits**: Consider implementing request size limits in production
2. **Validation**: The API validates base64 format but not audio content
3. **Rate limiting**: Recommended for production deployments
4. **Cleanup**: Temporary files are automatically removed

## Browser Integration Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>IndexTTS2 Base64 Demo</title>
</head>
<body>
    <input type="file" id="voiceFile" accept="audio/*">
    <textarea id="text" placeholder="Enter text..."></textarea>
    <button onclick="generateSpeech()">Generate</button>
    <audio id="output" controls></audio>

    <script>
    async function generateSpeech() {
        const file = document.getElementById('voiceFile').files[0];
        const text = document.getElementById('text').value;
        
        // Convert file to base64
        const reader = new FileReader();
        reader.onload = async function(e) {
            const base64 = e.target.result.split(',')[1];
            
            // Call API
            const response = await fetch('http://localhost:8000/v1/audio/speech', {
                method: 'POST',
                headers: {
                    'Authorization': 'Bearer test_token',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    model: 'IndexTTS2',
                    input: text,
                    voice: 'browser_voice',
                    voice_base64: base64,
                    response_format: 'mp3'
                })
            });
            
            // Play result
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            document.getElementById('output').src = url;
        };
        reader.readAsDataURL(file);
    }
    </script>
</body>
</html>
```

## Comparison: File vs Base64

| Feature | File-based | Base64 |
|---------|-----------|--------|
| Setup | Requires file upload | No setup needed |
| Request size | Small | Large (~33% overhead) |
| Reusability | High (cached on server) | Low (sent each time) |
| Dynamic voices | Requires upload first | Immediate |
| Server storage | Required | Not required |
| Best for | Frequent use, production | One-time use, testing |

## Best Practices

1. **Use files for production voices**: Upload commonly used voices to `characters/`
2. **Use base64 for dynamic content**: User-uploaded voices, testing, demos
3. **Validate before encoding**: Check audio quality before base64 encoding
4. **Handle errors gracefully**: Implement proper error handling for invalid data
5. **Consider caching**: Cache base64 strings client-side if reusing
6. **Monitor payload size**: Be aware of request size limits

## Troubleshooting

### "Voice file not found" despite sending base64

**Issue:** The `voice` parameter is still required even when using `voice_base64`.

**Solution:** Set `voice` to any placeholder value (e.g., "base64_voice").

### Large request timeout

**Issue:** Request times out with large audio files.

**Solution:** 
- Reduce audio file size
- Increase server timeout settings
- Use file-based method for large files

### Memory errors

**Issue:** Server runs out of memory.

**Solution:**
- Limit audio file size
- Use file-based method for large files
- Increase server memory allocation

## Additional Resources

- **API Documentation**: See `API_README.md`
- **Quick Start**: See `API_QUICKSTART.md`
- **Python Client**: `api_client_base64_example.py`
- **Standard Client**: `api_client_example.py`
