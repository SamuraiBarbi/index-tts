#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         IndexTTS2 API Setup Script                          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if conda environment is active
if [[ "$CONDA_DEFAULT_ENV" != "index-tts" ]]; then
    echo "⚠️  Conda environment 'index-tts' is not active"
    echo "Please run: conda activate index-tts"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Step 1: Installing API dependencies..."
uv sync --extra api
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"
echo ""

echo "📁 Step 2: Setting up voice references directory..."
mkdir -p characters
if [ -d "examples" ]; then
    if [ -f "examples/voice_01.wav" ]; then
        cp examples/voice_01.wav characters/alex.wav 2>/dev/null || true
        echo "✅ Copied alex.wav"
    fi
    if [ -f "examples/voice_07.wav" ]; then
        cp examples/voice_07.wav characters/narrator.wav 2>/dev/null || true
        echo "✅ Copied narrator.wav"
    fi
    if [ -f "examples/emo_happy.wav" ]; then
        cp examples/emo_happy.wav characters/emotion_happy.wav 2>/dev/null || true
        echo "✅ Copied emotion_happy.wav"
    fi
else
    echo "⚠️  Examples directory not found, skipping voice setup"
fi
echo ""

echo "🔍 Step 3: Checking model files..."
if [ ! -d "checkpoints" ]; then
    echo "❌ Checkpoints directory not found"
    echo "Please download models first:"
    echo "  hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints"
    exit 1
fi

required_files=("bpe.model" "gpt.pth" "config.yaml" "s2mel.pth" "wav2vec2bert_stats.pt")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "checkpoints/$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo ""
    echo "Please download models:"
    echo "  hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints"
    exit 1
fi
echo "✅ All model files present"
echo ""

echo "📥 Step 4: Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True)" 2>/dev/null || true
echo "✅ NLTK data ready"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start the API server:"
echo "     python api_run.py"
echo ""
echo "  2. Test the API:"
echo "     curl http://localhost:8889/health"
echo ""
echo "  3. View interactive docs:"
echo "     http://localhost:8889/docs"
echo ""
echo "  4. Run test suite:"
echo "     See SETUP_AND_TEST.md for detailed testing instructions"
echo ""
