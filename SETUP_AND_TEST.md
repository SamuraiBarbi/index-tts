# IndexTTS2 API Setup and Testing Guide

## Step 1: Activate Conda Environment

The conda environment was already created. Let's activate it:

```bash
conda activate index-tts
```

## Step 2: Install Dependencies

### Install Core Dependencies with UV

```bash
# Install all dependencies including API support
uv sync --extra api

# Or install everything (API + WebUI + DeepSpeed)
uv sync --all-extras
```

### Alternative: Install API Dependencies with Pip

If you prefer pip:

```bash
pip install fastapi uvicorn[standard] python-multipart requests nltk
```

## Step 3: Verify Model Files

Check that model files are in the `checkpoints/` directory:

```bash
ls -lh checkpoints/
```

Required files:
- `bpe.model`
- `gpt.pth`
- `config.yaml`
- `s2mel.pth`
- `wav2vec2bert_stats.pt`

If missing, download them:

```bash
# Using huggingface-cli
uv tool install "huggingface-hub[cli,hf_xet]"
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints

# Or using modelscope
uv tool install "modelscope"
modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints
```

## Step 4: Set Up Voice References

Create the characters directory and add voice samples:

```bash
mkdir -p characters

# Copy example voices
cp examples/voice_01.wav characters/alex.wav
cp examples/voice_07.wav characters/narrator.wav
cp examples/emo_happy.wav characters/emotion_happy.wav
```

## Step 5: Start the API Server

```bash
python api_run.py
```

You should see:

```
╔══════════════════════════════════════════════════════════════╗
║                  IndexTTS2 API Server                        ║
╚══════════════════════════════════════════════════════════════╝

Starting server on 0.0.0.0:8000
Model directory: checkpoints
FP16: Enabled
Device: Auto

API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health

Press CTRL+C to stop the server
```

## Step 6: Test the API

### Test 1: Health Check

Open a new terminal and test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"ok","model":"IndexTTS2"}
```

### Test 2: Basic Speech Generation

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "IndexTTS2",
    "input": "Hello, this is a test of the IndexTTS2 API.",
    "voice": "alex",
    "response_format": "mp3"
  }' \
  --output test_basic.mp3
```

### Test 3: Using Python Client

```bash
python api_client_example.py \
  --text "Hello from IndexTTS2 API!" \
  --voice alex \
  --output test_client.mp3
```

### Test 4: Base64 Audio

```bash
python api_client_base64_example.py \
  --text "Testing base64 audio support!" \
  --voice-file examples/voice_01.wav \
  --output test_base64.mp3
```

### Test 5: Progressive Streaming

```bash
python api_client_streaming_example.py \
  --text "First sentence for streaming. Second sentence here. Third sentence complete." \
  --voice alex \
  --output-dir streaming_test
```

### Test 6: Emotion Control

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "IndexTTS2",
    "input": "I am so happy and excited!",
    "voice": "alex",
    "emotion_voice": "emotion_happy",
    "emotion_weight": 0.8,
    "response_format": "mp3"
  }' \
  --output test_emotion.mp3
```

### Test 7: Interactive API Documentation

Open your browser and visit:

```
http://localhost:8000/docs
```

This provides an interactive Swagger UI where you can:
- See all available endpoints
- Test API calls directly in the browser
- View request/response schemas
- Try different parameters

## Step 7: Verify Generated Audio

Play the generated audio files to verify quality:

```bash
# On Linux
mpg123 test_basic.mp3

# On macOS
afplay test_basic.mp3

# Or use any media player
vlc test_basic.mp3
```

## Troubleshooting

### Issue: "Model directory missing"

**Solution:**
```bash
# Download models
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

### Issue: "Voice file not found"

**Solution:**
```bash
# Ensure voice files exist
ls -la characters/
# Add voice files if missing
cp examples/voice_01.wav characters/alex.wav
```

### Issue: "CUDA out of memory"

**Solution:**
```bash
# Use CPU mode
python api_run.py --device cpu

# Or disable FP16
python api_run.py --no-fp16
```

### Issue: "NLTK punkt tokenizer not found"

**Solution:**
```python
# Run Python and download
python -c "import nltk; nltk.download('punkt')"
```

### Issue: "FFmpeg not found"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Conda
conda install -c conda-forge ffmpeg
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use different port
python api_run.py --port 9000
```

## Complete Test Suite

Run all tests in sequence:

```bash
#!/bin/bash

echo "🧪 Running IndexTTS2 API Test Suite"
echo "===================================="

# Test 1: Health Check
echo "Test 1: Health Check"
curl -s http://localhost:8000/health | jq .
echo ""

# Test 2: Basic Generation
echo "Test 2: Basic Speech Generation"
python api_client_example.py \
  --text "This is test number two." \
  --voice alex \
  --output test_02.mp3
echo ""

# Test 3: Different Format
echo "Test 3: WAV Format"
python api_client_example.py \
  --text "Testing WAV format." \
  --voice alex \
  --format wav \
  --output test_03.wav
echo ""

# Test 4: Speed and Gain
echo "Test 4: Speed and Gain Adjustment"
python api_client_example.py \
  --text "Testing speed and volume." \
  --voice alex \
  --speed 1.2 \
  --gain 3.0 \
  --output test_04.mp3
echo ""

# Test 5: Emotion Control
echo "Test 5: Emotion Control"
python api_client_example.py \
  --text "I am very happy today!" \
  --voice alex \
  --emotion-voice emotion_happy \
  --emotion-weight 0.8 \
  --output test_05.mp3
echo ""

# Test 6: Base64 Audio
echo "Test 6: Base64 Audio Input"
python api_client_base64_example.py \
  --text "Testing base64 encoding." \
  --voice-file examples/voice_01.wav \
  --output test_06.mp3
echo ""

# Test 7: Progressive Streaming
echo "Test 7: Progressive Streaming"
python api_client_streaming_example.py \
  --text "First sentence. Second sentence. Third sentence." \
  --voice alex \
  --output-dir test_streaming
echo ""

echo "✅ All tests complete!"
echo "Check generated files: test_*.mp3, test_*.wav, test_streaming/"
```

Save this as `run_tests.sh` and execute:

```bash
chmod +x run_tests.sh
./run_tests.sh
```

## Performance Testing

### Test Response Time

```bash
time curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Performance test.",
    "voice": "alex",
    "response_format": "mp3"
  }' \
  --output perf_test.mp3
```

### Test Concurrent Requests

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Run load test (10 requests, 2 concurrent)
ab -n 10 -c 2 -p request.json -T application/json \
  -H "Authorization: Bearer test_token" \
  http://localhost:8000/v1/audio/speech
```

## Development Mode

For development with auto-reload:

```bash
python api_run.py --reload --log-level debug
```

## Production Deployment

For production use:

```bash
# With multiple workers
python api_run.py \
  --host 0.0.0.0 \
  --port 8000 \
  --log-level info

# Or use gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Environment Variables

Set these for custom configuration:

```bash
export TTS_FP16=1          # Enable FP16 (default: 1)
export TTS_DEVICE=cuda:0   # Specify device (default: auto)

python api_run.py
```

## Next Steps

1. ✅ API is running and tested
2. 📚 Read the documentation:
   - `API_README.md` - Complete API reference
   - `STREAMING_GUIDE.md` - Streaming documentation
   - `BASE64_API_GUIDE.md` - Base64 audio guide
3. 🔧 Customize authentication in `app/main.py`
4. 🚀 Deploy to production server
5. 📊 Set up monitoring and logging

## Summary

Your IndexTTS2 API is now:
- ✅ Set up in conda environment
- ✅ Dependencies installed
- ✅ Model files verified
- ✅ Voice references configured
- ✅ Server running
- ✅ Tested and working

Enjoy your IndexTTS2 API! 🎉
