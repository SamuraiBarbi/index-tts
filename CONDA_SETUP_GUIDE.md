# Conda Environment Setup Guide

## Quick Start

### 1. Create the Conda Environment

```bash
# Create environment from environment.yml
conda env create -f environment.yml
```

This will create a new conda environment named `indextts2-api` with all dependencies.

### 2. Activate the Environment

```bash
conda activate indextts2-api
```

### 3. Verify Installation

```bash
# Check Python version
python --version

# Check PyTorch installation
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Check FastAPI installation
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
```

### 4. Set Up Voice Files

```bash
# Run the setup script
./setup_api.sh
```

Or manually:

```bash
# Create characters directory
mkdir -p characters

# Copy example voices
cp examples/voice_01.wav characters/alex.wav
cp examples/voice_07.wav characters/narrator.wav
```

### 5. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt')"
```

### 6. Start the API Server

```bash
python api_run.py
```

## Environment Management

### List All Conda Environments

```bash
conda env list
```

### Update the Environment

If you modify `environment.yml`:

```bash
conda env update -f environment.yml --prune
```

### Remove the Environment

```bash
conda deactivate
conda env remove -n indextts2-api
```

### Export Environment

To share your exact environment:

```bash
conda env export > environment_exact.yml
```

## What's Included

### System Packages (via Conda)
- **Python 3.10** - Base Python version
- **PyTorch 2.5+** - Deep learning framework with CUDA support
- **TorchAudio** - Audio processing for PyTorch
- **FFmpeg** - Audio/video processing
- **Git** - Version control

### Python Packages (via Pip)

**Core IndexTTS2 Dependencies:**
- accelerate, transformers, tokenizers
- librosa, soundfile, audiotools
- numba, numpy, pandas
- sentencepiece, jieba, cn2an
- And more...

**API Dependencies:**
- FastAPI - Web framework
- Uvicorn - ASGI server
- NLTK - Natural language processing
- Requests - HTTP client

**Optional:**
- Gradio - Web UI
- DeepSpeed - Training optimization (if needed)

## Troubleshooting

### Issue: "conda: command not found"

**Solution:**
Install Miniconda or Anaconda:
```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### Issue: "PackagesNotFoundError"

**Solution:**
Update conda and try again:
```bash
conda update -n base conda
conda env create -f environment.yml
```

### Issue: CUDA not available

**Solution:**
Check NVIDIA drivers:
```bash
nvidia-smi
```

If drivers are missing, install them:
```bash
# Ubuntu/Debian
sudo apt install nvidia-driver-535

# Or use conda
conda install -c conda-forge cudatoolkit=12.1
```

### Issue: Environment creation is slow

**Solution:**
This is normal. PyTorch is large (~1.5 GB). Be patient or use mamba for faster solving:
```bash
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

### Issue: "Solving environment: failed"

**Solution:**
Try creating with fewer constraints:
```bash
# Create minimal environment first
conda create -n indextts2-api python=3.10 pip
conda activate indextts2-api

# Then install via pip
pip install -r requirements.txt  # If you have one
# Or install uv and use pyproject.toml
pip install uv
uv sync --extra api
```

## Alternative: Using UV Instead

If conda is too slow or has issues, you can use UV with a virtual environment:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install uv
pip install uv

# Install dependencies
uv sync --extra api
```

## Activating on Different Shells

### Bash/Zsh
```bash
conda activate indextts2-api
```

### Fish
```fish
conda activate indextts2-api
```

### PowerShell (Windows)
```powershell
conda activate indextts2-api
```

### CMD (Windows)
```cmd
conda activate indextts2-api
```

## Auto-Activation

To automatically activate the environment when entering the directory:

### Using direnv

1. Install direnv:
```bash
# Ubuntu/Debian
sudo apt install direnv

# macOS
brew install direnv
```

2. Add to your shell config (~/.bashrc or ~/.zshrc):
```bash
eval "$(direnv hook bash)"  # or zsh
```

3. Create `.envrc` in project directory:
```bash
echo "conda activate indextts2-api" > .envrc
direnv allow
```

## Environment Variables

Set these in your activated environment:

```bash
# Enable FP16 (default)
export TTS_FP16=1

# Specify device
export TTS_DEVICE=cuda:0

# Or add to conda environment
conda env config vars set TTS_FP16=1
conda env config vars set TTS_DEVICE=cuda:0
```

## Testing the Environment

After setup, run this test:

```bash
# Activate environment
conda activate indextts2-api

# Test imports
python << EOF
import torch
import fastapi
import nltk
from indextts.infer_v2 import IndexTTS2

print("✅ All imports successful!")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"FastAPI: {fastapi.__version__}")
EOF
```

## Next Steps

After environment setup:

1. ✅ Environment created and activated
2. 📥 Download models (if not done):
   ```bash
   hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints
   ```
3. 🎤 Set up voice files:
   ```bash
   ./setup_api.sh
   ```
4. 🚀 Start the API:
   ```bash
   python api_run.py
   ```
5. 🧪 Test the API:
   ```bash
   curl http://localhost:8000/health
   ```

## Summary

Your conda environment includes:
- ✅ Python 3.10
- ✅ PyTorch 2.5+ with CUDA
- ✅ All IndexTTS2 dependencies
- ✅ FastAPI and API dependencies
- ✅ NLTK for streaming
- ✅ FFmpeg for audio processing
- ✅ Gradio for WebUI (optional)

Environment name: **indextts2-api**

Activate with: `conda activate indextts2-api`
