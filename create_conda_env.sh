#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║      Creating Conda Environment for IndexTTS2 API           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed or not in PATH"
    echo "Please install Miniconda or Anaconda first"
    exit 1
fi

echo "📦 Creating conda environment from environment.yml..."
echo ""

# Create the environment
conda env create -f environment.yml

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Conda environment created successfully!"
    echo ""
    echo "To activate the environment, run:"
    echo "  conda activate indextts2-api"
    echo ""
    echo "After activation, run the setup script:"
    echo "  ./setup_api.sh"
else
    echo ""
    echo "❌ Failed to create conda environment"
    echo ""
    echo "If the environment already exists, you can:"
    echo "  1. Remove it: conda env remove -n indextts2-api"
    echo "  2. Update it: conda env update -f environment.yml"
    exit 1
fi
