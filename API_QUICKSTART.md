# IndexTTS2 API Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install API Dependencies

```bash
# Install FastAPI and related dependencies
uv sync --extra api

# Or install all extras including API
uv sync --all-extras
```

### 2. Prepare Voice Files

Create a `characters` directory and add your voice reference files:

```bash
mkdir -p characters
```

Add WAV files to `characters/`:
- `characters/alex.wav` - Example voice 1
- `characters/narrator.wav` - Example voice 2
- `characters/emotion_happy.wav` - Emotion reference (optional)

You can use any of the example voices from the `examples/` directory:

```bash
cp examples/voice_01.wav characters/alex.wav
cp examples/voice_07.wav characters/narrator.wav
```

### 3. Start the API Server

```bash
python api_run.py
```

The server will start on `http://localhost:8000`

### 4. Test the API

**Option A: Using the Python client**

```bash
python api_client_example.py \
  --text "Hello, this is IndexTTS2 speaking!" \
  --voice alex \
  --output test.mp3
```

**Option B: Using curl**

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "IndexTTS2",
    "input": "Hello, this is IndexTTS2!",
    "voice": "alex",
    "response_format": "mp3"
  }' \
  --output test.mp3
```

**Option C: Using the interactive API docs**

Visit `http://localhost:8000/docs` in your browser for an interactive API interface.

## 📖 Common Use Cases

### Basic Text-to-Speech

```bash
python api_client_example.py \
  --text "Welcome to IndexTTS2" \
  --voice alex \
  --output welcome.mp3
```

### With Emotion Control (Reference Audio)

```bash
python api_client_example.py \
  --text "I'm so excited about this!" \
  --voice alex \
  --emotion-voice emotion_happy \
  --emotion-weight 0.8 \
  --output excited.mp3
```

### With Emotion Control (Text Description)

```bash
python api_client_example.py \
  --text "This is wonderful news!" \
  --voice alex \
  --emotion-text "joyful and energetic" \
  --emotion-weight 0.6 \
  --output joyful.mp3
```

### Different Output Formats

```bash
# WAV format
python api_client_example.py \
  --text "Testing WAV output" \
  --voice alex \
  --format wav \
  --output test.wav

# OGG format
python api_client_example.py \
  --text "Testing OGG output" \
  --voice alex \
  --format ogg \
  --output test.ogg
```

### Adjust Speed and Gain

```bash
python api_client_example.py \
  --text "Speaking faster with more volume" \
  --voice alex \
  --speed 1.2 \
  --gain 3.0 \
  --output faster_louder.mp3
```

## 🔧 Server Configuration

### Run on Different Port

```bash
python api_run.py --port 9000
```

### Enable Development Mode (Auto-reload)

```bash
python api_run.py --reload
```

### Use CPU Instead of GPU

```bash
python api_run.py --device cpu
```

### Disable FP16 (for older GPUs)

```bash
python api_run.py --no-fp16
```

## 📚 Full Documentation

For complete API documentation, see [`API_README.md`](API_README.md)

## 🐛 Troubleshooting

### "Voice file not found" error
- Ensure your WAV files are in the `characters/` directory
- Check the filename matches (without .wav extension in the API call)

### "Model directory missing" error
- Ensure model files are downloaded to `checkpoints/`
- Run the model download commands from the main README

### FFmpeg errors
- Install FFmpeg: `sudo apt install ffmpeg` (Linux) or `brew install ffmpeg` (Mac)

### CUDA/GPU errors
- Use `--device cpu` to run on CPU
- Use `--no-fp16` for older GPUs
- Check CUDA installation with `nvidia-smi`

## 💡 Tips

1. **Voice Quality**: Use clear, 5-10 second voice samples for best results
2. **Emotion Weight**: Start with 0.6-0.7 for natural-sounding emotion control
3. **Performance**: Enable FP16 for faster inference on modern GPUs
4. **Authentication**: Change the default token in production environments

## 🔗 Next Steps

- Explore the interactive API docs at `http://localhost:8000/docs`
- Read the full API documentation in `API_README.md`
- Check out emotion control examples in the main README
- Integrate the API into your applications using the provided examples
