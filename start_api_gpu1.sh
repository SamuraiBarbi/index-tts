#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Starting IndexTTS2 API on RTX 3090 (GPU 1)              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate indextts2-api

# Set CUDA device to GPU 1 (RTX 3090)
export CUDA_VISIBLE_DEVICES=1

echo "Using GPU 1 (RTX 3090)"
echo ""

# Start the API server
python api_run.py --device cuda:0
