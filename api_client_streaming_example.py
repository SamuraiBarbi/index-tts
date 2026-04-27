import requests
import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Test IndexTTS2 API progressive streaming")
    parser.add_argument("--url", type=str, default="http://localhost:8889/v1/audio/speech", 
                        help="URL of the IndexTTS2 API")
    parser.add_argument("--token", type=str, default="test_token", help="API token")
    parser.add_argument("--text", type=str, required=True, help="Text to synthesize (will be split into sentences)")
    parser.add_argument("--voice", type=str, required=True, help="Voice to use")
    parser.add_argument("--output-dir", type=str, default="streaming_output", help="Output directory for chunks")
    parser.add_argument("--format", type=str, default="mp3", choices=["mp3", "wav", "ogg"], 
                        help="Output format")
    parser.add_argument("--sample-rate", type=int, default=24000, help="Sample rate")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--gain", type=float, default=0.0, help="Audio gain in dB")
    parser.add_argument("--emotion-voice", type=str, default=None, help="Emotion reference voice")
    parser.add_argument("--emotion-weight", type=float, default=0.65, help="Emotion weight")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    payload = {
        "model": "IndexTTS2",
        "input": args.text,
        "voice": args.voice,
        "response_format": args.format,
        "sample_rate": args.sample_rate,
        "stream": True,  # Enable progressive streaming
        "speed": args.speed,
        "gain": args.gain
    }
    
    if args.emotion_voice:
        payload["emotion_voice"] = args.emotion_voice
        payload["emotion_weight"] = args.emotion_weight
    
    headers = {
        "Authorization": f"Bearer {args.token}",
        "Content-Type": "application/json"
    }
    
    print(f"🚀 Starting progressive streaming to {args.url}")
    print(f"📝 Text: {args.text}")
    print(f"🎤 Voice: {args.voice}")
    print(f"📁 Output directory: {args.output_dir}")
    print()
    
    response = requests.post(args.url, json=payload, headers=headers, stream=True)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return
    
    print("📥 Receiving audio chunks...")
    print()
    
    chunk_files = []
    buffer = b""
    
    for chunk in response.iter_content(chunk_size=None):
        if not chunk:
            continue
        
        buffer += chunk
        
        # Try to parse metadata (JSON line followed by audio data)
        if b'\n' in buffer:
            parts = buffer.split(b'\n', 1)
            try:
                metadata_str = parts[0].decode('utf-8')
                metadata = json.loads(metadata_str)
                
                # The rest is audio data
                if len(parts) > 1:
                    audio_data = parts[1]
                    
                    # Save this chunk
                    chunk_filename = os.path.join(
                        args.output_dir,
                        f"chunk_{metadata['sentence_index']:03d}.{args.format}"
                    )
                    
                    with open(chunk_filename, 'wb') as f:
                        f.write(audio_data)
                    
                    chunk_files.append(chunk_filename)
                    
                    print(f"✅ Chunk {metadata['sentence_index']+1}/{metadata['total_sentences']}: {chunk_filename}")
                    print(f"   📝 \"{metadata['sentence_text']}\"")
                    print(f"   💾 {len(audio_data)} bytes")
                    print()
                    
                    buffer = b""
                    
            except json.JSONDecodeError:
                # Not a metadata line, keep buffering
                pass
    
    print(f"🎉 Streaming complete! Received {len(chunk_files)} chunks")
    print(f"📁 Files saved to: {args.output_dir}/")
    
    # List all files
    print("\n📋 Generated files:")
    for f in chunk_files:
        print(f"   - {f}")

if __name__ == "__main__":
    main()
