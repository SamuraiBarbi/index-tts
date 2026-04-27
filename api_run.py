import os
import uvicorn
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run the IndexTTS2 API server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8889, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--log-level", type=str, default="info", help="Log level (debug, info, warning, error)")
    parser.add_argument("--no-fp16", action="store_true", help="Disable FP16 precision")
    parser.add_argument("--device", type=str, default=None, help="Device to use (cpu, cuda, cuda:0, mps)")
    parser.add_argument("--model-dir", type=str, default="checkpoints", help="Model directory path")
    
    args = parser.parse_args()
    
    if args.no_fp16:
        os.environ["TTS_FP16"] = "0"
    if args.device:
        os.environ["TTS_DEVICE"] = args.device
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                  IndexTTS2 API Server                        ║
╚══════════════════════════════════════════════════════════════╝

Starting server on {args.host}:{args.port}
Model directory: {args.model_dir}
FP16: {'Disabled' if args.no_fp16 else 'Enabled'}
Device: {args.device or 'Auto'}

API Documentation: http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}/docs
Health Check: http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}/health

Press CTRL+C to stop the server
""")
    
    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level
    )

if __name__ == "__main__":
    main()
