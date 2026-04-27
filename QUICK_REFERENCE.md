# IndexTTS2 API - Quick Reference

## 🚀 Start Server (Optimized)

```bash
conda activate indextts2-api
./start_api_optimized.sh
```

**Server will run on:** http://localhost:8889

## 📡 API Endpoints

- **Docs**: http://localhost:8889/docs
- **Health**: http://localhost:8889/health
- **Speech**: POST http://localhost:8889/v1/audio/speech

## ⚡ Performance Settings

**Enabled by default:**
- ✅ FP16 Precision (2x faster)
- ✅ CUDA Kernels (20-30% faster)
- ✅ RTX 3090 GPU
- ✅ Port 8889 (no conflicts)

**Total speedup: ~2.4-2.6x faster!**

## 🎯 Quick Test

```bash
# Simple test
curl -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world","voice":"alex","response_format":"wav"}' \
  --output test.wav

# Play directly
curl -X POST "http://localhost:8889/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world","voice":"alex","response_format":"wav"}' \
  --output - | aplay
```

## 🎨 Features

- Voice cloning from reference audio
- Base64 audio input (no file uploads)
- Progressive streaming
- Emotion control (text, audio, vectors)
- Multiple formats (MP3, WAV, OGG)

## 📚 Documentation

- `PERFORMANCE_GUIDE.md` - Performance optimization
- `API_README.md` - Complete API documentation
- `STREAMING_GUIDE.md` - Streaming features
- `BASE64_API_GUIDE.md` - Base64 audio guide

## 🔧 Environment Variables

```bash
export CUDA_VISIBLE_DEVICES=1    # Use RTX 3090
export TTS_FP16=1                # Enable FP16
export TTS_CUDA_KERNEL=1         # Enable CUDA kernels
```

## 🎉 Ready to Use!

Start the server and visit http://localhost:8889/docs for interactive API documentation.
