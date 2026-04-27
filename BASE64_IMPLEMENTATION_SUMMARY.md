# Base64 Audio Support - Implementation Summary

## ✅ Implementation Complete

The IndexTTS2 API now supports **base64 encoded audio** for both voice and emotion reference audio.

## 🎯 What Was Added

### 1. API Model Updates (`app/models.py`)
- Added `voice_base64` parameter - Base64 encoded voice reference audio
- Added `emotion_voice_base64` parameter - Base64 encoded emotion reference audio
- Both parameters are optional and work alongside existing file-based parameters

### 2. Service Layer Updates (`app/services/tts_service.py`)
- Updated `generate_speech()` method to accept base64 parameters
- Added logic to decode base64 audio and save to temporary files
- Automatic cleanup of temporary files after generation
- Priority: base64 takes precedence over file-based references

### 3. Utility Functions (`app/utils/audio_utils.py`)
- Added `decode_base64_audio()` function
- Handles Data URI format (e.g., `data:audio/wav;base64,`)
- Proper error handling for invalid base64 data
- Creates temporary WAV files for processing

### 4. Route Updates (`app/routes/speech.py`)
- Updated endpoint to pass base64 parameters to service layer
- No breaking changes to existing functionality

### 5. Documentation
- **BASE64_API_GUIDE.md** - Complete guide with examples
- **api_client_base64_example.py** - Python client for base64 usage
- Updated **API_README.md** with base64 information

## 📝 Usage Examples

### Basic Usage

```python
import requests
import base64

# Encode audio file
with open('my_voice.wav', 'rb') as f:
    voice_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make API request
response = requests.post(
    'http://localhost:8889/v1/audio/speech',
    headers={
        'Authorization': 'Bearer test_token',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'IndexTTS2',
        'input': 'Hello from base64!',
        'voice': 'base64_voice',
        'voice_base64': voice_base64,
        'response_format': 'mp3'
    }
)
```

### With Emotion Control

```python
# Encode both voice and emotion
with open('voice.wav', 'rb') as f:
    voice_b64 = base64.b64encode(f.read()).decode('utf-8')

with open('emotion.wav', 'rb') as f:
    emotion_b64 = base64.b64encode(f.read()).decode('utf-8')

# Request with both
response = requests.post(url, json={
    'input': 'I am so excited!',
    'voice': 'placeholder',
    'voice_base64': voice_b64,
    'emotion_voice_base64': emotion_b64,
    'emotion_weight': 0.8,
    'response_format': 'mp3'
})
```

### Using the Client

```bash
python api_client_base64_example.py \
  --text "Hello from base64!" \
  --voice-file examples/voice_01.wav \
  --output test.mp3
```

## 🔧 Technical Details

### How It Works

1. **Client** encodes audio file to base64 string
2. **API** receives base64 in JSON request
3. **Service** decodes base64 to temporary WAV file
4. **IndexTTS2** processes the temporary file
5. **Cleanup** removes temporary files automatically

### File Flow

```
Base64 String
    ↓
decode_base64_audio()
    ↓
Temporary WAV file (/tmp/tmpXXXXXX.wav)
    ↓
IndexTTS2.infer()
    ↓
Generated Audio
    ↓
Cleanup (temp file deleted)
```

### Priority Logic

- If `voice_base64` is provided → use base64 (ignore `voice` filename)
- If `voice_base64` is null → use `voice` filename from `characters/`
- Same logic applies for `emotion_voice_base64` vs `emotion_voice`

## 🎨 Features

✅ **Flexible Input** - Support both file-based and base64 methods
✅ **Data URI Support** - Handles `data:audio/wav;base64,` prefix
✅ **Automatic Cleanup** - Temporary files removed after use
✅ **Error Handling** - Validates base64 format and provides clear errors
✅ **No Breaking Changes** - Fully backward compatible
✅ **Mix and Match** - Can use file for voice, base64 for emotion (or vice versa)

## 📊 Comparison

| Method | File-based | Base64 |
|--------|-----------|--------|
| **Setup** | Upload files to server | No setup |
| **Request Size** | Small | Large (+33%) |
| **Server Storage** | Required | Not required |
| **Best For** | Production, frequent use | Testing, dynamic voices |
| **Reusability** | High (cached) | Low (sent each time) |

## 🔐 Security & Performance

### Security
- Base64 data is validated before decoding
- Temporary files use secure temp directory
- Files are automatically cleaned up
- No persistent storage of base64 data

### Performance
- Base64 decoding is fast (minimal overhead)
- Temporary file I/O is efficient
- Memory usage proportional to audio size
- Cleanup happens in background tasks

## 📚 Documentation Files

1. **BASE64_API_GUIDE.md** - Complete guide
   - Usage examples (Python, JavaScript, curl)
   - Browser integration
   - Error handling
   - Best practices

2. **api_client_base64_example.py** - Working client
   - Command-line interface
   - File encoding
   - API integration

3. **API_README.md** - Updated main docs
   - Added base64 to features
   - Updated parameters table
   - Added advanced features section

## 🧪 Testing

### Test with Python Client

```bash
# Basic test
python api_client_base64_example.py \
  --text "Testing base64 support" \
  --voice-file examples/voice_01.wav \
  --output test.mp3

# With emotion
python api_client_base64_example.py \
  --text "Happy test!" \
  --voice-file examples/voice_01.wav \
  --emotion-file examples/emo_happy.wav \
  --emotion-weight 0.8 \
  --output happy.mp3
```

### Test with curl

```bash
# Encode file
VOICE_B64=$(base64 -w 0 examples/voice_01.wav)

# Make request
curl -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d "{
    \"input\": \"Hello from curl!\",
    \"voice\": \"base64\",
    \"voice_base64\": \"$VOICE_B64\",
    \"response_format\": \"mp3\"
  }" \
  --output test.mp3
```

## 💡 Use Cases

### 1. Web Applications
Users upload audio files in browser → Convert to base64 → Send to API

### 2. Dynamic Voice Generation
Generate voices on-the-fly without managing server files

### 3. Testing & Development
Quick testing with different voices without file uploads

### 4. Microservices
Stateless API calls without shared file storage

### 5. Mobile Apps
Send audio data directly from mobile devices

## ⚠️ Considerations

### Request Size
- Base64 increases size by ~33%
- 1 MB audio → ~1.33 MB base64
- Consider request size limits in production

### Best Practices
1. Use file-based for production/frequent voices
2. Use base64 for dynamic/one-time voices
3. Validate audio quality before encoding
4. Implement request size limits
5. Consider caching base64 strings client-side

## 🔄 Backward Compatibility

✅ **100% Backward Compatible**
- All existing API calls work unchanged
- File-based method still fully supported
- No breaking changes to any endpoints
- Optional parameters only

## 📈 Future Enhancements

Potential improvements:
- [ ] Support for other audio formats (MP3, OGG input)
- [ ] Automatic format detection
- [ ] Audio validation before processing
- [ ] Caching of base64 decoded files
- [ ] Compression support
- [ ] Batch base64 processing

## ✨ Summary

The base64 audio support feature:
- ✅ Fully implemented and tested
- ✅ Well documented with examples
- ✅ Backward compatible
- ✅ Production ready
- ✅ Supports both voice and emotion references
- ✅ Automatic cleanup and error handling

Users can now choose between:
1. **File-based** - Upload files to `characters/` directory
2. **Base64** - Send audio data directly in API requests
3. **Mixed** - Use both methods in the same request

This provides maximum flexibility for different use cases and deployment scenarios.
