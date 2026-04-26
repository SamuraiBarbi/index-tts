# Progressive Streaming Guide for IndexTTS2 API

## Overview

The IndexTTS2 API now supports **progressive sentence-by-sentence streaming**, allowing you to receive and play audio chunks as they are generated, rather than waiting for the entire text to be processed.

## Benefits

✅ **Lower latency** - Start playing audio while generation continues
✅ **Better UX** - Users hear responses faster
✅ **Memory efficient** - Process long texts without loading everything into memory
✅ **Real-time feel** - Perfect for conversational AI and audiobooks
✅ **Progress tracking** - Know which sentence is being generated

## How It Works

1. **Text Splitting**: Input text is automatically split into sentences using NLTK
2. **Progressive Generation**: Each sentence is generated sequentially
3. **Chunk Streaming**: Audio chunks are streamed as soon as they're ready
4. **Metadata Included**: Each chunk includes metadata (sentence index, text, etc.)

## Usage

### Enable Streaming

Simply set `stream: true` in your API request:

```json
{
  "model": "IndexTTS2",
  "input": "First sentence. Second sentence. Third sentence.",
  "voice": "alex",
  "stream": true,
  "response_format": "mp3"
}
```

### Stream Format

The API streams data in the following format:

```
{metadata_json}\n
{audio_bytes}
{metadata_json}\n
{audio_bytes}
...
```

Each chunk consists of:
1. **Metadata line** - JSON object with sentence info, ending with `\n`
2. **Audio data** - Raw audio bytes in the requested format

### Metadata Structure

```json
{
  "sentence_index": 0,
  "total_sentences": 3,
  "sentence_text": "First sentence.",
  "format": "mp3"
}
```

## Examples

### Python Client

**Basic streaming:**

```python
import requests
import json

response = requests.post(
    'http://localhost:8000/v1/audio/speech',
    headers={'Authorization': 'Bearer test_token'},
    json={
        'input': 'Hello world. This is streaming. It works great!',
        'voice': 'alex',
        'stream': True,
        'response_format': 'mp3'
    },
    stream=True
)

buffer = b""
for chunk in response.iter_content(chunk_size=None):
    buffer += chunk
    
    # Parse metadata and audio
    if b'\n' in buffer:
        parts = buffer.split(b'\n', 1)
        metadata = json.loads(parts[0].decode('utf-8'))
        audio_data = parts[1]
        
        print(f"Received: {metadata['sentence_text']}")
        # Play or save audio_data
        
        buffer = b""
```

**Using the provided client:**

```bash
python api_client_streaming_example.py \
  --text "Hello world. This is a test. Streaming works great!" \
  --voice alex \
  --output-dir streaming_output
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8000/v1/audio/speech', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer test_token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    input: 'First sentence. Second sentence. Third sentence.',
    voice: 'alex',
    stream: true,
    response_format: 'mp3'
  })
});

const reader = response.body.getReader();
let buffer = '';

while (true) {
  const {done, value} = await reader.read();
  if (done) break;
  
  buffer += new TextDecoder().decode(value);
  
  // Process chunks
  const lines = buffer.split('\n');
  for (let i = 0; i < lines.length - 1; i++) {
    const metadata = JSON.parse(lines[i]);
    console.log(`Sentence ${metadata.sentence_index + 1}: ${metadata.sentence_text}`);
    // Next chunk is audio data
  }
  
  buffer = lines[lines.length - 1];
}
```

### curl (Save chunks)

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Authorization: Bearer test_token" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "First sentence. Second sentence. Third sentence.",
    "voice": "alex",
    "stream": true,
    "response_format": "mp3"
  }' \
  --no-buffer \
  --output streaming_output.bin
```

## Advanced Features

### With Emotion Control

```json
{
  "input": "I am so happy! This is wonderful! Life is great!",
  "voice": "alex",
  "emotion_text": "joyful and excited",
  "emotion_weight": 0.7,
  "stream": true,
  "response_format": "mp3"
}
```

### With Base64 Voice

```python
import base64

with open('my_voice.wav', 'rb') as f:
    voice_base64 = base64.b64encode(f.read()).decode('utf-8')

response = requests.post(url, json={
    'input': 'Streaming with base64 voice. This is amazing!',
    'voice': 'base64',
    'voice_base64': voice_base64,
    'stream': True
}, stream=True)
```

## Real-Time Playback Example

### Python with PyAudio

```python
import requests
import json
import pyaudio
from io import BytesIO
from pydub import AudioSegment

# Initialize audio player
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

response = requests.post(url, json={
    'input': 'Your long text here...',
    'voice': 'alex',
    'stream': True,
    'response_format': 'wav'  # WAV is easier to play directly
}, stream=True)

buffer = b""
for chunk in response.iter_content(chunk_size=None):
    buffer += chunk
    
    if b'\n' in buffer:
        parts = buffer.split(b'\n', 1)
        metadata = json.loads(parts[0].decode('utf-8'))
        audio_data = parts[1]
        
        # Play audio immediately
        audio = AudioSegment.from_file(BytesIO(audio_data), format='wav')
        stream.write(audio.raw_data)
        
        buffer = b""

stream.stop_stream()
stream.close()
p.terminate()
```

### Browser with Web Audio API

```html
<!DOCTYPE html>
<html>
<head>
    <title>IndexTTS2 Streaming Demo</title>
</head>
<body>
    <textarea id="text" rows="5" cols="50">First sentence. Second sentence. Third sentence.</textarea>
    <button onclick="streamSpeech()">Stream Speech</button>
    <div id="status"></div>
    <audio id="player" controls></audio>

    <script>
    let audioQueue = [];
    let isPlaying = false;
    
    async function streamSpeech() {
        const text = document.getElementById('text').value;
        const status = document.getElementById('status');
        
        const response = await fetch('http://localhost:8000/v1/audio/speech', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer test_token',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                input: text,
                voice: 'alex',
                stream: true,
                response_format: 'mp3'
            })
        });
        
        const reader = response.body.getReader();
        let buffer = new Uint8Array();
        
        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            
            // Append to buffer
            const newBuffer = new Uint8Array(buffer.length + value.length);
            newBuffer.set(buffer);
            newBuffer.set(value, buffer.length);
            buffer = newBuffer;
            
            // Try to extract metadata and audio
            const text = new TextDecoder().decode(buffer);
            const newlineIndex = text.indexOf('\n');
            
            if (newlineIndex !== -1) {
                const metadataStr = text.substring(0, newlineIndex);
                const metadata = JSON.parse(metadataStr);
                
                status.innerHTML = `Generating: ${metadata.sentence_text}`;
                
                // Extract audio data (after newline)
                const audioStart = new TextEncoder().encode(metadataStr + '\n').length;
                const audioData = buffer.slice(audioStart);
                
                // Create blob and queue for playback
                const blob = new Blob([audioData], {type: 'audio/mp3'});
                const url = URL.createObjectURL(blob);
                audioQueue.push(url);
                
                if (!isPlaying) {
                    playNext();
                }
                
                buffer = new Uint8Array();
            }
        }
    }
    
    function playNext() {
        if (audioQueue.length === 0) {
            isPlaying = false;
            return;
        }
        
        isPlaying = true;
        const player = document.getElementById('player');
        player.src = audioQueue.shift();
        player.play();
        
        player.onended = () => playNext();
    }
    </script>
</body>
</html>
```

## Performance Considerations

### Sentence Splitting

- Uses NLTK's `sent_tokenize` for accurate sentence detection
- Falls back to simple regex splitting if NLTK unavailable
- Handles multiple languages (English, Chinese, etc.)

### Memory Usage

- Each sentence is generated independently
- Temporary files are cleaned up immediately after streaming
- Total memory usage is proportional to single sentence, not entire text

### Latency

- First chunk arrives as soon as first sentence is generated
- Subsequent chunks stream progressively
- Total time is similar to non-streaming, but perceived latency is much lower

## Comparison: Streaming vs Non-Streaming

| Feature | Non-Streaming | Progressive Streaming |
|---------|---------------|----------------------|
| **Time to first audio** | Wait for all text | ~5-10 seconds |
| **Memory usage** | Full audio in memory | Per-sentence |
| **User experience** | Wait then play | Progressive playback |
| **Best for** | Short texts | Long texts, real-time apps |
| **Complexity** | Simple | Moderate |

## Best Practices

1. **Use WAV for real-time playback** - Easier to decode on-the-fly
2. **Buffer management** - Implement proper buffering for smooth playback
3. **Error handling** - Handle network interruptions gracefully
4. **Progress indication** - Show users which sentence is being generated
5. **Chunk size** - Sentences are optimal; don't split mid-sentence

## Troubleshooting

### Chunks not arriving

**Issue:** No data received from stream

**Solution:**
- Ensure `stream: true` is set
- Check network/firewall settings
- Verify server is running

### Playback stuttering

**Issue:** Audio playback is choppy

**Solution:**
- Implement audio queue/buffer
- Use WAV format for simpler decoding
- Pre-buffer 1-2 chunks before starting playback

### Metadata parsing errors

**Issue:** Cannot parse JSON metadata

**Solution:**
- Ensure proper buffering (wait for `\n`)
- Handle partial chunks correctly
- Check encoding (UTF-8)

## API Response Headers

Streaming responses include special headers:

```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=speech_stream.mp3
X-Stream-Type: progressive
```

## Limitations

- Streaming is sentence-based (not word-based or phoneme-based)
- Minimum chunk size is one sentence
- Cannot seek/skip in stream (sequential only)
- Requires stable network connection

## Future Enhancements

Potential improvements:
- [ ] Word-level streaming
- [ ] Adjustable chunk size
- [ ] Stream pause/resume
- [ ] Server-Sent Events (SSE) format option
- [ ] WebSocket support
- [ ] Chunk compression

## Examples Repository

Complete working examples:
- **Python**: `api_client_streaming_example.py`
- **Browser**: See HTML example above
- **Node.js**: See JavaScript example above

## Summary

Progressive streaming in IndexTTS2 API:
- ✅ Sentence-by-sentence generation
- ✅ Real-time audio delivery
- ✅ Metadata with each chunk
- ✅ Works with all API features (emotion, base64, etc.)
- ✅ Production-ready

Perfect for:
- 📖 Audiobook narration
- 💬 Conversational AI
- 🎙️ Podcast generation
- 📱 Mobile apps
- 🌐 Web applications

Start streaming today with `stream: true`!
