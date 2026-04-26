#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         Downloading IndexTTS2 Model Files                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate indextts2-api

echo "📥 Downloading models from HuggingFace..."
echo "This will download approximately 4-5 GB of data."
echo ""

# Install huggingface-cli if not present
pip install -q huggingface-hub[cli] 2>/dev/null

# Download the models
echo "Downloading to checkpoints/ directory..."
huggingface-cli download IndexTeam/Index-TTS --local-dir checkpoints --local-dir-use-symlinks False

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Models downloaded successfully!"
    echo ""
    echo "Verifying files..."
    ls -lh checkpoints/ | head -20
    echo ""
    echo "You can now start the API server:"
    echo "  python api_run.py"
else
    echo ""
    echo "❌ Download failed"
    echo ""
    echo "Alternative: Use modelscope (for users in China)"
    echo "  pip install modelscope"
    echo "  modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints"
fi
