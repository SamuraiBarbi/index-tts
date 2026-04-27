#!/bin/bash

# Select RTX 3090 explicitly
# NOTE: PyTorch sees GPUs in different order than nvidia-smi!
# PyTorch GPU 0 = RTX 3090 (nvidia-smi GPU 1)
# PyTorch GPU 1 = GTX 1080 Ti (nvidia-smi GPU 0)
export TTS_GPU_ID=0  # Use PyTorch GPU 0 = RTX 3090

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     Starting IndexTTS2 API (Optimized Performance)          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Activate conda environment
eval "$(conda shell.bash hook)"
conda activate indextts2-api

# Performance optimizations (CUDA_VISIBLE_DEVICES already set above)
export TTS_FP16=1              # Enable FP16 precision (2x faster, less VRAM)
export TTS_CUDA_KERNEL=1       # Enable optimized CUDA kernels
export TTS_USE_ACCEL=1         # Enable Flash Attention 2 + paged KV-cache
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True  # Better memory management

# Optional: Reduce memory fragmentation
export CUDA_LAUNCH_BLOCKING=0  # Async CUDA operations (faster)

echo "🚀 Performance Optimizations Enabled:"
echo "  - GPU: RTX 3090 (CUDA 12.1)"
echo "  - FP16 Precision: Enabled"
echo "  - CUDA Kernels: Enabled"
echo "  - Flash Attention 2: Enabled"
echo "  - Paged KV-Cache: Enabled"
echo "  - Memory Management: Optimized"
echo ""

# Start the API server
python api_run.py --port 8889

echo ""
echo "Server stopped."
