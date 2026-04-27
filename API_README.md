# IndexTTS2 REST API Service

A FastAPI-based REST API implementation for IndexTTS2 text-to-speech synthesis with emotion control.

## Features

- ✅ RESTful API with OpenAPI documentation
- ✅ Voice cloning from reference audio
- ✅ **Base64 encoded audio support** - Send audio data directly in requests
- ✅ **Progressive sentence-by-sentence streaming** - Real-time audio generation
- ✅ Emotion control via reference audio, vectors, or text descriptions
- ✅ Multiple output formats (MP3, WAV, OGG)
- ✅ Streaming and non-streaming responses
- ✅ Token-based authentication
- ✅ CORS support
- ✅ Advanced generation parameters

## Prerequisites

- Python 3.10 or higher
- CUDA-compatible GPU (recommended) or CPU
- FFmpeg installed on your system
- IndexTTS2 model files in `checkpoints/` directory

## Installation

The API service uses the same dependencies as the main IndexTTS2 project. Additional dependencies needed:

```bash
pip install fastapi uvicorn python-multipart
```

Or add to your environment:

```bash
uv sync --all-extras
```

## Setting Up Voice References

You have two options for providing voice references:

### Option 1: File-based (Recommended for Production)

Set up voice reference files on the server:

1. Create a `characters` directory in the project root:
```bash
mkdir -p characters
```

2. Add WAV files containing voice samples to this directory:
   - Files should be in WAV format
   - Clear voice samples (5-10 seconds recommended)
   - Named according to your preferred voice identifier (e.g., `alex.wav`, `female1.wav`)

Example structure:
```
characters/
├── alex.wav
├── female1.wav
├── narrator.wav
└── emotion_happy.wav
```

### Option 2: Base64 Encoded Audio (New!)

Send audio data directly in API requests without uploading files:

- No server-side file management required
- Perfect for dynamic voices and testing
- See **[BASE64_API_GUIDE.md](BASE64_API_GUIDE.md)** for detailed documentation

```python
import base64

with open('my_voice.wav', 'rb') as f:
    voice_base64 = base64.b64encode(f.read()).decode('utf-8')

# Use in API request
payload = {
    "voice": "placeholder",
    "voice_base64": voice_base64,
    ...
}
```

## Running the API Server

### Basic Usage

```bash
python api_run.py
```

The server will start on `http://0.0.0.0:8000` by default.

### Advanced Options

```bash
python api_run.py \
  --host 127.0.0.1 \
  --port 9000 \
  --log-level debug \
  --reload
```

Available options:
- `--host`: Host to bind to (default: `0.0.0.0`)
- `--port`: Port to bind to (default: `8000`)
- `--reload`: Enable auto-reload for development
- `--log-level`: Set logging level (default: `info`)
- `--no-fp16`: Disable FP16 precision
- `--device`: Specify device to use (`cpu`, `cuda`, `cuda:0`, `mps`)
- `--model-dir`: Model directory path (default: `checkpoints`)

## API Usage

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8889/docs`
- **ReDoc**: `http://localhost:8889/redoc`
- **Health Check**: `http://localhost:8889/health`

### Endpoint: Generate Speech

**POST** `/v1/audio/speech`

#### Headers
```
Authorization: Bearer <your_token>
Content-Type: application/json
```

#### Request Body

**Basic Example:**
```json
{
  "model": "IndexTTS2",
  "input": "Hello, this is a test message for IndexTTS2.",
  "voice": "alex",
  "response_format": "mp3",
  "sample_rate": 24000,
  "stream": false,
  "speed": 1.0,
  "gain": 0.0
}
```

**With Emotion Control (Reference Audio):**
```json
{
  "model": "IndexTTS2",
  "input": "I'm so excited about this new technology!",
  "voice": "alex",
  "emotion_voice": "emotion_happy",
  "emotion_weight": 0.8,
  "response_format": "mp3"
}
```

**With Emotion Control (Text Description):**
```json
{
  "model": "IndexTTS2",
  "input": "This is amazing!",
  "voice": "alex",
  "emotion_text": "excited and joyful",
  "emotion_weight": 0.6,
  "response_format": "mp3"
}
```

**With Emotion Vector:**
```json
{
  "model": "IndexTTS2",
  "input": "I feel wonderful today.",
  "voice": "alex",
  "emotion_vector": [0.8, 0, 0, 0, 0, 0, 0.2, 0.5],
  "emotion_weight": 0.7,
  "response_format": "mp3"
}
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | "IndexTTS2" | Model identifier |
| `input` | string | **required** | Text to synthesize |
| `voice` | string | **required** | Voice identifier (filename without .wav) |
| `voice_base64` | string | null | **NEW:** Base64 encoded audio for voice reference |
| `response_format` | string | "mp3" | Output format: `mp3`, `wav`, `ogg` |
| `sample_rate` | integer | 24000 | Output sample rate in Hz |
| `stream` | boolean | false | Enable streaming response |
| `speed` | float | 1.0 | Speech speed factor |
| `gain` | float | 0.0 | Audio gain in dB |
| `emotion_voice` | string | null | Emotion reference audio identifier |
| `emotion_voice_base64` | string | null | **NEW:** Base64 encoded audio for emotion reference |
| `emotion_weight` | float | 0.65 | Emotion weight (0.0-1.0) |
| `emotion_vector` | array | null | Emotion vector [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm] |
| `emotion_text` | string | null | Text description of desired emotion |
| `use_random` | boolean | false | Enable random sampling |
| `do_sample` | boolean | true | Enable sampling |
| `temperature` | float | 0.8 | Sampling temperature |
| `top_p` | float | 0.8 | Top-p sampling |
| `top_k` | integer | 30 | Top-k sampling |
| `repetition_penalty` | float | 10.0 | Repetition penalty |
| `max_mel_tokens` | integer | 1500 | Maximum mel tokens |

### Using the Python Client

A sample client is provided in `api_client_example.py`:

**Basic usage:**
```bash
python api_client_example.py \
  --text "Hello, this is a test message for IndexTTS2." \
  --voice alex \
  --output output.mp3
```

**With emotion control:**
```bash
python api_client_example.py \
  --text "I'm so excited!" \
  --voice alex \
  --emotion-voice emotion_happy \
  --emotion-weight 0.8 \
  --output excited.mp3
```

**With emotion text:**
```bash
python api_client_example.py \
  --text "This is wonderful!" \
  --voice alex \
  --emotion-text "joyful and energetic" \
  --emotion-weight 0.6 \
  --output joyful.mp3
```

### Using curl

**Basic request:**
```bash
curl -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "IndexTTS2",
    "input": "Hello, this is a test message.",
    "voice": "alex",
    "response_format": "mp3"
  }' \
  --output output.mp3
```

**With emotion control:**
```bash
curl -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "IndexTTS2",
    "input": "I am so happy!",
    "voice": "alex",
    "emotion_text": "excited and joyful",
    "emotion_weight": 0.7,
    "response_format": "mp3"
  }' \
  --output happy.mp3
```

## Authentication

The API uses Bearer token authentication. By default, any non-empty token is accepted. For production use, implement proper token validation in `app/main.py`:

```python
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Add your token validation logic here
    # Example: validate against database, JWT, etc.
    if not is_valid_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
```

## Troubleshooting

### GPU Issues
- Ensure CUDA is properly installed
- Use `--device cpu` to force CPU mode
- Use `--no-fp16` for older GPUs

### Audio Generation Issues
- Verify voice files exist in `characters/` directory
- Check voice files are in WAV format
- Ensure model files are in `checkpoints/` directory

### API Connection Issues
- Check server is running: `curl http://localhost:8889/health`
- Verify firewall settings
- Ensure correct host/port configuration
- Check authorization token is included

## Advanced Features

### Progressive Streaming

The API supports **sentence-by-sentence progressive streaming** for real-time audio generation:
- Start playing audio while generation continues
- Lower latency for long texts
- Perfect for audiobooks, conversational AI, and podcasts
- Automatic sentence splitting and chunking

**See [STREAMING_GUIDE.md](STREAMING_GUIDE.md) for complete documentation and examples.**

Quick example:
```python
response = requests.post(url, json={
    "input": "First sentence. Second sentence. Third sentence.",
    "voice": "alex",
    "stream": True,  # Enable progressive streaming
    "response_format": "mp3"
}, stream=True)

# Receive chunks as they're generated
for chunk in response.iter_content(chunk_size=None):
    # Process audio chunk
    pass
```

### Base64 Audio Support

The API supports base64 encoded audio for both voice and emotion references. This is perfect for:
- Dynamic voice generation without file uploads
- Web applications with user-uploaded audio
- Testing and prototyping
- Stateless API operations

**See [BASE64_API_GUIDE.md](BASE64_API_GUIDE.md) for complete documentation and examples.**

Quick example:
```python
import base64
with open('voice.wav', 'rb') as f:
    voice_base64 = base64.b64encode(f.read()).decode('utf-8')

response = requests.post(url, json={
    "voice": "base64_voice",
    "voice_base64": voice_base64,
    "input": "Hello!",
    ...
})
```

## License

This API implementation follows the same license as IndexTTS2. See LICENSE file for details.

## Acknowledgements

- Based on the IndexTTS2 model by Bilibili IndexTTS Team
- API implementation inspired by OpenAI's speech API format
- FastAPI framework for the REST API
