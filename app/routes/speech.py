from fastapi import APIRouter, HTTPException, BackgroundTasks, Request
from fastapi.responses import StreamingResponse, FileResponse
import os
import logging
import json
from ..models import SpeechRequest
from ..services.tts_service import TTSService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize TTS service lazily to avoid startup issues
tts_service = None

def get_tts_service():
    global tts_service
    if tts_service is None:
        logger.info("Initializing TTS service...")
        tts_service = TTSService()
    return tts_service

@router.post("/speech")
async def generate_speech(request: SpeechRequest, background_tasks: BackgroundTasks, req: Request):
    """
    Generate speech from text using IndexTTS2
    
    Supports:
    - Voice cloning from reference audio
    - Emotion control via reference audio, vectors, or text descriptions
    - Multiple output formats (mp3, wav, ogg)
    - Streaming and non-streaming responses
    """
    try:
        logger.info(f"Speech request: model={request.model}, voice={request.voice}, format={request.response_format}")
        
        model, voice = request.voice.split(":", 1) if ":" in request.voice else ("IndexTTS2", request.voice)
        
        service = get_tts_service()
        output_path = service.generate_speech(
            text=request.input,
            voice=voice,
            voice_base64=request.voice_base64,
            response_format=request.response_format,
            sample_rate=request.sample_rate,
            speed=request.speed,
            gain=request.gain,
            emotion_voice=request.emotion_voice,
            emotion_voice_base64=request.emotion_voice_base64,
            emotion_weight=request.emotion_weight,
            emotion_vector=request.emotion_vector,
            emotion_text=request.emotion_text,
            use_random=request.use_random,
            do_sample=request.do_sample,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            repetition_penalty=request.repetition_penalty,
            max_mel_tokens=request.max_mel_tokens
        )
        
        if request.stream:
            logger.info(f"Progressive streaming response requested")
            
            # Use progressive sentence-by-sentence streaming
            def stream_generator():
                service = get_tts_service()
                for audio_bytes, metadata in service.generate_speech_streaming(
                    text=request.input,
                    voice=voice,
                    voice_base64=request.voice_base64,
                    response_format=request.response_format,
                    sample_rate=request.sample_rate,
                    speed=request.speed,
                    gain=request.gain,
                    emotion_voice=request.emotion_voice,
                    emotion_voice_base64=request.emotion_voice_base64,
                    emotion_weight=request.emotion_weight,
                    emotion_vector=request.emotion_vector,
                    emotion_text=request.emotion_text,
                    use_random=request.use_random,
                    do_sample=request.do_sample,
                    temperature=request.temperature,
                    top_p=request.top_p,
                    top_k=request.top_k,
                    repetition_penalty=request.repetition_penalty,
                    max_mel_tokens=request.max_mel_tokens
                ):
                    # Send metadata header followed by audio chunk
                    metadata_json = json.dumps(metadata) + "\n"
                    yield metadata_json.encode('utf-8')
                    yield audio_bytes
                
            return StreamingResponse(
                stream_generator(),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; filename=speech_stream.{request.response_format}",
                    "X-Stream-Type": "progressive"
                }
            )
        else:
            logger.info(f"File response: {output_path}")
            background_tasks.add_task(os.remove, output_path)
            
            return FileResponse(
                output_path,
                media_type=f"audio/{request.response_format}",
                filename=f"speech.{request.response_format}"
            )
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
