# IndexTTS2 API - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Create Conda Environment (Currently Running)

The conda environment is being created. This may take 10-15 minutes.

```bash
conda env create -f environment.yml
```

**Status:** Check the terminal for progress. PyTorch (1.35 GB) is the largest package.

### Step 2: Activate Environment

Once creation completes:

```bash
conda activate indextts2-api
```

### Step 3: Set Up Voice Files

```bash
./setup_api.sh
```

This will:
- Install API dependencies
- Create `characters/` directory
- Copy example voice files
- Download NLTK data

### Step 4: Start the Server

```bash
python api_run.py
```

You should see:
```
╔══════════════════════════════════════════════════════════════╗
║                  IndexTTS2 API Server                        ║
╚══════════════════════════════════════════════════════════════╝

Starting server on 0.0.0.0:8000
API Documentation: http://localhost:8000/docs
```

### Step 5: Test the API

Open a new terminal and run:

```bash
# Health check
curl http://localhost:8000/health

# Generate speech
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hello from IndexTTS2!",
    "voice": "alex",
    "response_format": "mp3"
  }' \
  --output test.mp3

# Play the result
mpg123 test.mp3  # or: afplay test.mp3 on macOS
```

## 📚 Documentation

- **CONDA_SETUP_GUIDE.md** - Detailed conda environment guide
- **SETUP_AND_TEST.md** - Complete setup and testing instructions
- **API_README.md** - Full API documentation
- **STREAMING_GUIDE.md** - Progressive streaming guide
- **BASE64_API_GUIDE.md** - Base64 audio support guide

## 🎯 Key Features

✅ **Voice Cloning** - Clone any voice from audio samples
✅ **Emotion Control** - Control emotion via audio, vectors, or text
✅ **Progressive Streaming** - Real-time sentence-by-sentence generation
✅ **Base64 Support** - Send audio data directly in requests
✅ **Multiple Formats** - MP3, WAV, OGG output
✅ **Interactive Docs** - Swagger UI at http://localhost:8000/docs

## 🔧 Common Commands

```bash
# Activate environment
conda activate indextts2-api

# Start server
python api_run.py

# Start with custom settings
python api_run.py --port 9000 --device cuda:0

# Test with Python client
python api_client_example.py --text "Hello!" --voice alex --output test.mp3

# Test streaming
python api_client_streaming_example.py --text "First. Second. Third." --voice alex

# Test base64
python api_client_base64_example.py --voice-file examples/voice_01.wav --text "Test" --output test.mp3
```

## ⚡ Quick Tests

### Test 1: Basic Generation
```bash
python api_client_example.py \
  --text "This is a test of IndexTTS2." \
  --voice alex \
  --output test1.mp3
```

### Test 2: With Emotion
```bash
python api_client_example.py \
  --text "I am so happy!" \
  --voice alex \
  --emotion-voice emotion_happy \
  --emotion-weight 0.8 \
  --output test2.mp3
```

### Test 3: Streaming
```bash
python api_client_streaming_example.py \
  --text "First sentence. Second sentence. Third sentence." \
  --voice alex \
  --output-dir streaming_test
```

## 🐛 Troubleshooting

### Conda environment creation failed
```bash
# Update conda
conda update -n base conda

# Try again
conda env create -f environment.yml
```

### Server won't start
```bash
# Check if models are downloaded
ls -la checkpoints/

# Download if missing
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
```

### "Voice file not found"
```bash
# Set up voices
./setup_api.sh

# Or manually
mkdir -p characters
cp examples/voice_01.wav characters/alex.wav
```

### CUDA errors
```bash
# Use CPU mode
python api_run.py --device cpu

# Or disable FP16
python api_run.py --no-fp16
```

## 📊 What's Next?

1. ✅ **Environment created** (in progress)
2. 🎤 **Add your own voices** to `characters/`
3. 🔧 **Customize** authentication in `app/main.py`
4. 📖 **Read docs** for advanced features
5. 🚀 **Deploy** to production

## 🎉 You're Ready!

Once the conda environment finishes creating:

1. Activate: `conda activate indextts2-api`
2. Setup: `./setup_api.sh`
3. Start: `python api_run.py`
4. Test: Visit `http://localhost:8000/docs`

Enjoy your IndexTTS2 API! 🎊
