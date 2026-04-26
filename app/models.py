from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal, List

class SpeechRequest(BaseModel):
    """
    Request model for speech synthesis
    """
    model: str = "IndexTTS2"
    input: str = Field(..., description="Text to synthesize")
    voice: str = Field(..., description="Voice identifier (filename without extension) OR base64 encoded audio data")
    voice_base64: Optional[str] = Field(default=None, description="Base64 encoded audio data for voice reference (alternative to voice filename)")
    response_format: Literal["mp3", "wav", "ogg"] = Field(default="mp3", description="Output audio format")
    sample_rate: Optional[int] = Field(default=24000, description="Output sample rate in Hz")
    stream: Optional[bool] = Field(default=False, description="Whether to stream the response")
    speed: Optional[float] = Field(default=1.0, description="Speech speed factor (1.0 = normal)")
    gain: Optional[float] = Field(default=0.0, description="Audio gain in dB")
    
    # IndexTTS2 specific parameters
    emotion_voice: Optional[str] = Field(default=None, description="Emotion reference audio (filename without extension)")
    emotion_voice_base64: Optional[str] = Field(default=None, description="Base64 encoded audio data for emotion reference")
    emotion_weight: Optional[float] = Field(default=0.65, description="Emotion weight (0.0-1.0)")
    emotion_vector: Optional[List[float]] = Field(default=None, description="Emotion vector [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]")
    emotion_text: Optional[str] = Field(default=None, description="Text description of desired emotion")
    use_random: Optional[bool] = Field(default=False, description="Enable random sampling for emotion")
    
    # Advanced generation parameters
    do_sample: Optional[bool] = Field(default=True, description="Enable sampling")
    temperature: Optional[float] = Field(default=0.8, description="Sampling temperature")
    top_p: Optional[float] = Field(default=0.8, description="Top-p sampling")
    top_k: Optional[int] = Field(default=30, description="Top-k sampling")
    repetition_penalty: Optional[float] = Field(default=10.0, description="Repetition penalty")
    max_mel_tokens: Optional[int] = Field(default=1500, description="Maximum mel tokens to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "model": "IndexTTS2",
                "input": "Hello, this is a test message for IndexTTS2.",
                "voice": "alex",
                "response_format": "mp3",
                "sample_rate": 24000,
                "stream": False,
                "speed": 1.0,
                "gain": 0.0
            }
        }
