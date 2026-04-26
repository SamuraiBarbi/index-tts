# IndexTTS2 API - Final Testing

## ✅ Setup Complete!

The API is ready to test with the following fixes applied:
- ✅ Real voice file (SamuraiBarbi.wav) copied to characters/alex.wav
- ✅ FFmpeg path fixed to use /usr/bin/ffmpeg
- ✅ WAV generation confirmed working
- ✅ Ready to test MP3 generation

## 🚀 Restart Server and Test

### 1. Restart the Server

Press CTRL+C in the server terminal, then:

```bash
conda activate indextts2-api
python api_run.py
```

### 2. Test WAV Generation (Already Working)

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world","voice":"alex","response_format":"wav"}' \
  --output test.wav
```

### 3. Test MP3 Generation (Should Work Now)

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{"input":"Hello world","voice":"alex","response_format":"mp3"}' \
  --output test.mp3
```

### 4. Test with Python Client

```bash
python api_client_example.py \
  --text "Hello from IndexTTS2 API! This is working great." \
  --voice alex \
  --format mp3 \
  --output final.mp3
```

### 5. Test Progressive Streaming

```bash
python api_client_streaming_example.py \
  --text "First sentence here. Second sentence follows. Third sentence complete." \
  --voice alex \
  --output-dir streaming_test
```

### 6. Test Base64 Audio

```bash
python api_client_base64_example.py \
  --text "Testing base64 audio input!" \
  --voice-file examples/SamuraiBarbi.wav \
  --output base64_test.mp3
```

## 📊 Expected Results

All tests should return **HTTP 200** and generate valid audio files.

## 🎉 Success Criteria

- ✅ Health check returns `{"status":"ok","model":"IndexTTS2"}`
- ✅ WAV generation works
- ✅ MP3 generation works
- ✅ Python client works
- ✅ Streaming works
- ✅ Base64 input works

## 🔧 If Issues Persist

Check server logs for errors and verify:
1. FFmpeg is accessible at `/usr/bin/ffmpeg`
2. Voice file exists at `characters/alex.wav`
3. Temporary directory is writable

Restart the server now and run the tests! 🚀
