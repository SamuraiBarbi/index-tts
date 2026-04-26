import os
import tempfile
import logging
import base64
import time
from indextts.infer_v2 import IndexTTS2
from ..utils.audio_utils import convert_audio, apply_audio_effects, decode_base64_audio
from ..utils.text_utils import split_into_sentences

logger = logging.getLogger(__name__)

class TTSService:
    """
    Service for text-to-speech generation using IndexTTS2
    """
    
    def __init__(self, model_dir="checkpoints", cfg_path="checkpoints/config.yaml", use_fp16=True, device=None):
        """
        Initialize the TTS service
        
        Args:
            model_dir (str): Directory containing model files
            cfg_path (str): Path to config file
            use_fp16 (bool): Whether to use FP16 precision
            device (str): Device to use (cpu, cuda, mps)
        """
        logger.info(f"Initializing IndexTTS2 service with model_dir={model_dir}, cfg_path={cfg_path}")
        
        use_fp16_env = os.environ.get("TTS_FP16", "1") == "1"
        use_fp16 = use_fp16 and use_fp16_env
        
        device_env = os.environ.get("TTS_DEVICE")
        if device_env:
            device = device_env
        
        self.tts = IndexTTS2(
            model_dir=model_dir,
            cfg_path=cfg_path,
            use_fp16=use_fp16,
            use_cuda_kernel=False,
            use_deepspeed=False
        )
        self.voices_dir = "characters"
        os.makedirs(self.voices_dir, exist_ok=True)
        logger.info(f"Voice directory: {self.voices_dir}")
        logger.info(f"IndexTTS2 service initialized successfully")
        
    def generate_speech(self, text, voice, voice_base64=None, response_format="mp3", sample_rate=24000, 
                       speed=1.0, gain=0.0, emotion_voice=None, emotion_voice_base64=None, 
                       emotion_weight=0.65, emotion_vector=None, emotion_text=None, use_random=False,
                       do_sample=True, temperature=0.8, top_p=0.8, top_k=30,
                       repetition_penalty=10.0, max_mel_tokens=1500):
        """
        Generate speech from text using IndexTTS2
        
        Args:
            text (str): Text to synthesize
            voice (str): Voice identifier (file name without extension)
            voice_base64 (str): Base64 encoded audio data for voice reference
            response_format (str): Output format (mp3, wav, ogg)
            sample_rate (int): Output sample rate
            speed (float): Speed factor
            gain (float): Gain adjustment in dB
            emotion_voice (str): Emotion reference audio identifier
            emotion_voice_base64 (str): Base64 encoded audio data for emotion reference
            emotion_weight (float): Emotion weight (0.0-1.0)
            emotion_vector (list): Emotion vector [happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]
            emotion_text (str): Text description of desired emotion
            use_random (bool): Enable random sampling for emotion
            do_sample (bool): Enable sampling
            temperature (float): Sampling temperature
            top_p (float): Top-p sampling
            top_k (int): Top-k sampling
            repetition_penalty (float): Repetition penalty
            max_mel_tokens (int): Maximum mel tokens to generate
            
        Returns:
            str: Path to the generated audio file
        """
        # Handle voice reference - either from file or base64
        voice_file = None
        temp_voice_file = None
        
        if voice_base64:
            # Decode base64 audio and save to temp file
            logger.info("Using base64 encoded voice reference")
            temp_voice_file = decode_base64_audio(voice_base64)
            voice_file = temp_voice_file
        else:
            # Use file from characters directory
            voice_file = os.path.join(self.voices_dir, f"{voice}.wav")
            if not os.path.exists(voice_file):
                logger.error(f"Voice file not found: {voice_file}")
                raise ValueError(f"Voice file {voice_file} not found. Please add {voice}.wav to the {self.voices_dir} directory.")
        
        # Handle emotion reference - either from file or base64
        emotion_audio_path = None
        temp_emotion_file = None
        
        if emotion_voice_base64:
            logger.info("Using base64 encoded emotion reference")
            temp_emotion_file = decode_base64_audio(emotion_voice_base64)
            emotion_audio_path = temp_emotion_file
        elif emotion_voice:
            emotion_audio_path = os.path.join(self.voices_dir, f"{emotion_voice}.wav")
            if not os.path.exists(emotion_audio_path):
                logger.warning(f"Emotion voice file not found: {emotion_audio_path}, ignoring")
                emotion_audio_path = None
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav_output = tmp.name
        
        logger.info(f"Generating speech: voice={voice}, text='{text[:50]}...', emotion_voice={emotion_voice}")
        
        use_emo_text = emotion_text is not None
        
        kwargs = {
            "do_sample": do_sample,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k if top_k > 0 else None,
            "repetition_penalty": repetition_penalty,
            "max_mel_tokens": max_mel_tokens,
            "num_beams": 3,
            "length_penalty": 0.0
        }
        
        self.tts.infer(
            spk_audio_prompt=voice_file,
            text=text,
            output_path=wav_output,
            emo_audio_prompt=emotion_audio_path,
            emo_alpha=emotion_weight,
            emo_vector=emotion_vector,
            use_emo_text=use_emo_text,
            emo_text=emotion_text,
            use_random=use_random,
            verbose=False,
            **kwargs
        )
        
        if speed != 1.0 or gain != 0.0:
            logger.info(f"Applying audio effects: speed={speed}, gain={gain}")
            effect_output = apply_audio_effects(wav_output, speed, gain)
            if effect_output != wav_output:
                os.remove(wav_output)
            wav_output = effect_output
        
        if response_format != "wav":
            logger.info(f"Converting to {response_format} with sample rate {sample_rate}")
            output_path = convert_audio(wav_output, response_format, sample_rate)
            os.remove(wav_output)
        else:
            output_path = wav_output
        
        # Clean up temporary files
        if temp_voice_file and os.path.exists(temp_voice_file):
            os.remove(temp_voice_file)
        if temp_emotion_file and os.path.exists(temp_emotion_file):
            os.remove(temp_emotion_file)
        
        logger.info(f"Speech generation completed: {output_path}")
        return output_path
    
    def generate_speech_streaming(self, text, voice, voice_base64=None, response_format="mp3", sample_rate=24000,
                                  speed=1.0, gain=0.0, emotion_voice=None, emotion_voice_base64=None,
                                  emotion_weight=0.65, emotion_vector=None, emotion_text=None, use_random=False,
                                  do_sample=True, temperature=0.8, top_p=0.8, top_k=30,
                                  repetition_penalty=10.0, max_mel_tokens=1500):
        """
        Generate speech progressively, sentence by sentence (streaming).
        
        This is a generator function that yields audio chunks as they are generated.
        
        Args:
            Same as generate_speech()
            
        Yields:
            tuple: (audio_bytes, metadata_dict) for each sentence
        """
        # Handle voice reference - either from file or base64
        voice_file = None
        temp_voice_file = None
        
        if voice_base64:
            logger.info("Using base64 encoded voice reference for streaming")
            temp_voice_file = decode_base64_audio(voice_base64)
            voice_file = temp_voice_file
        else:
            voice_file = os.path.join(self.voices_dir, f"{voice}.wav")
            if not os.path.exists(voice_file):
                logger.error(f"Voice file not found: {voice_file}")
                raise ValueError(f"Voice file {voice_file} not found.")
        
        # Handle emotion reference
        emotion_audio_path = None
        temp_emotion_file = None
        
        if emotion_voice_base64:
            logger.info("Using base64 encoded emotion reference for streaming")
            temp_emotion_file = decode_base64_audio(emotion_voice_base64)
            emotion_audio_path = temp_emotion_file
        elif emotion_voice:
            emotion_audio_path = os.path.join(self.voices_dir, f"{emotion_voice}.wav")
            if not os.path.exists(emotion_audio_path):
                logger.warning(f"Emotion voice file not found: {emotion_audio_path}, ignoring")
                emotion_audio_path = None
        
        # Split text into sentences
        sentences = split_into_sentences(text)
        total_sentences = len(sentences)
        logger.info(f"Streaming generation: {total_sentences} sentences")
        
        use_emo_text = emotion_text is not None
        
        kwargs = {
            "do_sample": do_sample,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k if top_k > 0 else None,
            "repetition_penalty": repetition_penalty,
            "max_mel_tokens": max_mel_tokens,
            "num_beams": 3,
            "length_penalty": 0.0
        }
        
        generated_files = []
        
        try:
            for i, sentence in enumerate(sentences):
                if not sentence.strip():
                    continue
                
                logger.info(f"Generating sentence {i+1}/{total_sentences}: {sentence[:60]}...")
                
                # Generate audio for this sentence
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    wav_output = tmp.name
                
                self.tts.infer(
                    spk_audio_prompt=voice_file,
                    text=sentence,
                    output_path=wav_output,
                    emo_audio_prompt=emotion_audio_path,
                    emo_alpha=emotion_weight,
                    emo_vector=emotion_vector,
                    use_emo_text=use_emo_text,
                    emo_text=emotion_text,
                    use_random=use_random,
                    verbose=False,
                    **kwargs
                )
                
                # Apply effects if needed
                if speed != 1.0 or gain != 0.0:
                    effect_output = apply_audio_effects(wav_output, speed, gain)
                    if effect_output != wav_output:
                        os.remove(wav_output)
                    wav_output = effect_output
                
                # Convert format if needed
                if response_format != "wav":
                    output_path = convert_audio(wav_output, response_format, sample_rate)
                    os.remove(wav_output)
                else:
                    output_path = wav_output
                
                generated_files.append(output_path)
                
                # Read the audio file and yield it
                with open(output_path, 'rb') as f:
                    audio_bytes = f.read()
                
                metadata = {
                    "sentence_index": i,
                    "total_sentences": total_sentences,
                    "sentence_text": sentence,
                    "format": response_format
                }
                
                yield audio_bytes, metadata
                
        finally:
            # Cleanup temporary files
            for file_path in generated_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
            
            if temp_voice_file and os.path.exists(temp_voice_file):
                os.remove(temp_voice_file)
            if temp_emotion_file and os.path.exists(temp_emotion_file):
                os.remove(temp_emotion_file)
            
            logger.info("Streaming generation completed and cleaned up")
