"""
Language detection and translation utilities
"""
import re
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Make language detection consistent
DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    """
    Detect if text is English, Hindi, or mixed
    
    Returns:
        'en' for English
        'hi' for Hindi
        'mixed' for bilingual
    """
    if not text or len(text.strip()) < 10:
        return "en"
    
    try:
        # Count Devanagari characters (Hindi script)
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        total_chars = len(re.findall(r'[\w]', text))
        
        if total_chars == 0:
            return "en"
        
        hindi_ratio = hindi_chars / total_chars
        
        # Determine language based on ratio
        if hindi_ratio > 0.5:
            return "hi"
        elif hindi_ratio > 0.1:
            return "mixed"
        else:
            # Use langdetect as fallback
            lang = detect(text[:500])  # Sample first 500 chars
            return "hi" if lang == "hi" else "en"
            
    except Exception as e:
        print(f"Language detection error: {e}")
        return "en"


def is_hindi_text(text: str) -> bool:
    """Check if text contains Hindi characters"""
    return bool(re.search(r'[\u0900-\u097F]', text))


def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Translate text to target language
    
    Args:
        text: Input text
        target_lang: 'en' or 'hi'
    
    Returns:
        Translated text
    """
    try:
        if len(text.strip()) < 5:
            return text
        
        # Don't translate if already in target language
        current_lang = detect_language(text)
        if current_lang == target_lang:
            return text
        
        # Split long text into chunks (API limit: 5000 chars)
        max_chunk_size = 4500
        if len(text) > max_chunk_size:
            chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
            translated_chunks = []
            
            for chunk in chunks:
                translator = GoogleTranslator(source='auto', target=target_lang)
                translated_chunks.append(translator.translate(chunk))
            
            return " ".join(translated_chunks)
        else:
            translator = GoogleTranslator(source='auto', target=target_lang)
            return translator.translate(text)
            
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def get_language_display_name(lang_code: str) -> str:
    """Get friendly display name for language"""
    names = {
        "en": "English",
        "hi": "Hindi (हिंदी)",
        "mixed": "Bilingual (English + Hindi)"
    }
    return names.get(lang_code, "Unknown")