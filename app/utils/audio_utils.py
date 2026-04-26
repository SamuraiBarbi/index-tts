import subprocess
import os
import tempfile
import logging
import base64
import ffmpeg

logger = logging.getLogger(__name__)

def decode_base64_audio(base64_data):
    """
    Decode base64 encoded audio data and save to a temporary file.
    
    Args:
        base64_data (str): Base64 encoded audio data
        
    Returns:
        str: Path to the temporary audio file
    """
    try:
        # Remove data URI prefix if present (e.g., "data:audio/wav;base64,")
        if ',' in base64_data and base64_data.startswith('data:'):
            base64_data = base64_data.split(',', 1)[1]
        
        # Decode base64 data
        audio_bytes = base64.b64decode(base64_data)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            temp_path = tmp.name
        
        logger.info(f"Decoded base64 audio to temporary file: {temp_path}")
        return temp_path
    except Exception as e:
        logger.error(f"Failed to decode base64 audio: {str(e)}")
        raise ValueError(f"Invalid base64 audio data: {str(e)}")

def convert_audio(input_path, output_format, sample_rate=24000):
    """
    Convert audio to specified format using ffmpeg-python.
    
    Args:
        input_path (str): Path to input audio file
        output_format (str): Output format (mp3, wav, ogg)
        sample_rate (int): Output sample rate
        
    Returns:
        str: Path to converted audio file
    """
    output_path = os.path.splitext(input_path)[0] + f".{output_format}"
    
    try:
        logger.info(f"Converting audio to {output_format} with sample rate {sample_rate}")
        
        stream = ffmpeg.input(input_path)
        
        if output_format == "mp3":
            stream = ffmpeg.output(stream, output_path, ar=sample_rate, **{'c:a': 'libmp3lame', 'q:a': 2})
        elif output_format == "ogg":
            stream = ffmpeg.output(stream, output_path, ar=sample_rate, **{'c:a': 'libvorbis', 'q:a': 4})
        else:
            stream = ffmpeg.output(stream, output_path, ar=sample_rate)
        
        ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        
        logger.info(f"Successfully converted to {output_format}")
        return output_path
    except ffmpeg.Error as e:
        stderr = e.stderr.decode() if e.stderr else 'No stderr'
        stdout = e.stdout.decode() if e.stdout else 'No stdout'
        logger.error(f"FFmpeg conversion failed. Stderr: {stderr}, Stdout: {stdout}")
        raise RuntimeError(f"Audio conversion failed: ffmpeg error (see stderr output for detail)")

def apply_audio_effects(input_path, speed=1.0, gain=0.0):
    """
    Apply audio effects (speed, gain) using ffmpeg.
    
    Args:
        input_path (str): Path to input audio file
        speed (float): Speed factor (1.0 = normal)
        gain (float): Gain adjustment in dB
        
    Returns:
        str: Path to processed audio file
    """
    if speed == 1.0 and gain == 0.0:
        return input_path
    
    output_path = input_path.replace(".wav", "_processed.wav")
    
    filters = []
    if speed != 1.0:
        filters.append(f"atempo={speed}")
    if gain != 0.0:
        filters.append(f"volume={gain}dB")
    
    filter_str = ",".join(filters)
    
    # Use full path to ffmpeg
    ffmpeg_cmd = "/usr/bin/ffmpeg"
    
    cmd = [ffmpeg_cmd, "-y", "-i", input_path, "-af", filter_str, output_path]
    
    logger.info(f"Applying audio effects: speed={speed}, gain={gain}")
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg effects failed: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        raise
    
    return output_path
