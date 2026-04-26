import re
import logging

logger = logging.getLogger(__name__)

def split_into_sentences(text, language='auto'):
    """
    Split text into sentences for progressive generation.
    
    Args:
        text (str): Input text to split
        language (str): Language hint ('auto', 'en', 'zh')
        
    Returns:
        list: List of sentences
    """
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            logger.info("Downloading NLTK punkt tokenizer...")
            nltk.download('punkt', quiet=True)
        
        sentences = nltk.sent_tokenize(text)
        return [s.strip() for s in sentences if s.strip()]
    except ImportError:
        logger.warning("NLTK not available, using simple sentence splitting")
        return simple_sentence_split(text)

def simple_sentence_split(text):
    """
    Simple sentence splitting without NLTK (fallback).
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences
    """
    # Split on common sentence endings
    sentences = re.split(r'[.!?。！？]+', text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_text(text, max_length=200):
    """
    Split text into chunks of maximum length, respecting sentence boundaries.
    
    Args:
        text (str): Input text
        max_length (int): Maximum chunk length
        
    Returns:
        list: List of text chunks
    """
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        if current_length + sentence_length > max_length and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
