# Troubleshooting Guide

## Issue: "Missing key qwen_emo_path"

**Error:**
```
omegaconf.errors.ConfigAttributeError: Missing key qwen_emo_path
```

**Cause:** Downloaded wrong model repository (Index-TTS v1 instead of IndexTTS-2)

**Solution:**
Download the correct IndexTTS-2 model:

```bash
conda activate indextts2-api
pip install huggingface_hub
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='IndexTeam/IndexTTS-2', local_dir='checkpoints', local_dir_use_symlinks=False)"
```

**Currently:** This is downloading now (~5.89 GB, will take 10-15 minutes)

## Required Model Files

The `checkpoints/` directory should contain:

### Core Models
- `gpt.pth` - Main GPT model (~2.5 GB)
- `s2mel.pth` - Speech-to-mel model (~1.5 GB)
- `bpe.model` - Tokenizer
- `wav2vec2bert_stats.pt` - Statistics file

### Qwen Emotion Model
- `qwen0.6bemo4-merge/` directory with:
  - `config.json`
  - `generation_config.json`
  - `model.safetensors`
  - `tokenizer.json`
  - `tokenizer_config.json`
  - And other tokenizer files

### Vocoder
- `bigvgan_generator.pth` - Vocoder generator
- `bigvgan_discriminator.pth` - Vocoder discriminator

### Configuration
- `config.yaml` - Main configuration (must have `qwen_emo_path` key)

## Verification

After download completes, verify:

```bash
# Check directory structure
ls -lh checkpoints/
ls -la checkpoints/qwen0.6bemo4-merge/

# Check config has required keys
grep -i qwen checkpoints/config.yaml
```

Expected output should show `qwen_emo_path: qwen0.6bemo4-merge`

## Other Common Issues

### Issue: CUDA out of memory

**Solution:**
```bash
# Use CPU
python api_run.py --device cpu

# Or disable FP16
python api_run.py --no-fp16
```

### Issue: FFmpeg not found

**Solution:**
```bash
# Install FFmpeg
conda install -c conda-forge ffmpeg
```

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use different port
python api_run.py --port 9000
```

### Issue: Voice file not found

**Solution:**
```bash
# Ensure voice files exist
mkdir -p characters
cp examples/voice_01.wav characters/alex.wav
```

## Download Progress

**Current Status:** Downloading IndexTTS-2 model (~5.89 GB)

Monitor progress in the terminal. Once complete, you can start the server:

```bash
python api_run.py
```
