#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         IndexTTS2 API - Quick Test Script                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Activate the conda environment
echo "🔧 Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate indextts2-api

# Verify activation
if [[ "$CONDA_DEFAULT_ENV" != "indextts2-api" ]]; then
    echo "❌ Failed to activate environment"
    exit 1
fi
echo "✅ Environment activated: $CONDA_DEFAULT_ENV"
echo ""

# Set up voice files
echo "🎤 Setting up voice files..."
mkdir -p characters
if [ -f "examples/voice_01.wav" ]; then
    cp examples/voice_01.wav characters/alex.wav
    echo "✅ Copied alex.wav"
fi
if [ -f "examples/voice_07.wav" ]; then
    cp examples/voice_07.wav characters/narrator.wav
    echo "✅ Copied narrator.wav"
fi
echo ""

# Download NLTK data
echo "📥 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True)" 2>/dev/null
echo "✅ NLTK data ready"
echo ""

# Verify imports
echo "🔍 Verifying installations..."
python << 'EOF'
try:
    import torch
    import fastapi
    import nltk
    print(f"✅ PyTorch {torch.__version__}")
    print(f"✅ CUDA available: {torch.cuda.is_available()}")
    print(f"✅ FastAPI {fastapi.__version__}")
    print(f"✅ NLTK ready")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
EOF

if [ $? -ne 0 ]; then
    echo "❌ Verification failed"
    exit 1
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start the API server:"
echo "     python api_run.py"
echo ""
echo "  2. In another terminal, test it:"
echo "     curl http://localhost:8889/health"
echo ""
echo "  3. Or use the Python client:"
echo "     python api_client_example.py --text \"Hello!\" --voice alex --output test.mp3"
echo ""
