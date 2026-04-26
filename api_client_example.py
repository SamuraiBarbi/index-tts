import requests
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Test the IndexTTS2 API")
    parser.add_argument("--url", type=str, default="http://localhost:8000/v1/audio/speech", 
                        help="URL of the IndexTTS2 API")
    parser.add_argument("--token", type=str, default="test_token", help="API token")
    parser.add_argument("--text", type=str, required=True, help="Text to synthesize")
    parser.add_argument("--voice", type=str, required=True, help="Voice to use (filename without .wav)")
    parser.add_argument("--output", type=str, default="output.mp3", help="Output file")
    parser.add_argument("--format", type=str, default="mp3", choices=["mp3", "wav", "ogg"], 
                        help="Output format")
    parser.add_argument("--sample-rate", type=int, default=24000, help="Sample rate")
    parser.add_argument("--stream", action="store_true", help="Use streaming response")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed")
    parser.add_argument("--gain", type=float, default=0.0, help="Audio gain in dB")
    
    parser.add_argument("--emotion-voice", type=str, default=None, help="Emotion reference voice")
    parser.add_argument("--emotion-weight", type=float, default=0.65, help="Emotion weight (0.0-1.0)")
    parser.add_argument("--emotion-text", type=str, default=None, help="Emotion description text")
    
    args = parser.parse_args()
    
    payload = {
        "model": "IndexTTS2",
        "input": args.text,
        "voice": args.voice,
        "response_format": args.format,
        "sample_rate": args.sample_rate,
        "stream": args.stream,
        "speed": args.speed,
        "gain": args.gain
    }
    
    if args.emotion_voice:
        payload["emotion_voice"] = args.emotion_voice
        payload["emotion_weight"] = args.emotion_weight
    
    if args.emotion_text:
        payload["emotion_text"] = args.emotion_text
        payload["emotion_weight"] = args.emotion_weight
    
    headers = {
        "Authorization": f"Bearer {args.token}",
        "Content-Type": "application/json"
    }
    
    print(f"Sending request to {args.url}")
    print(f"Text: {args.text}")
    print(f"Voice: {args.voice}")
    if args.emotion_voice:
        print(f"Emotion Voice: {args.emotion_voice}")
    if args.emotion_text:
        print(f"Emotion Text: {args.emotion_text}")
    
    if args.stream:
        response = requests.post(args.url, json=payload, headers=headers, stream=True)
        if response.status_code == 200:
            with open(args.output, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"✅ Stream saved to {args.output}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    else:
        response = requests.post(args.url, json=payload, headers=headers)
        if response.status_code == 200:
            with open(args.output, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio saved to {args.output}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    main()
