#!/usr/bin/env python3
"""
Test script for Gemini TTS functionality
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.providers.tts import GeminiTTSProvider
from src.core.models import TTSConfig, TTSProvider
from config.settings import GOOGLE_API_KEY

def test_gemini_tts():
    """Test Gemini TTS with the fixed implementation"""
    
    if not GOOGLE_API_KEY:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
    
    try:
        # Create TTS config
        config = TTSConfig(
            provider=TTSProvider.GEMINI,
            voice="Kore"
        )
        
        # Create provider
        tts_provider = GeminiTTSProvider(config)
        
        # Test text
        test_text = "Hello! This is a test of the Gemini text-to-speech system."
        output_path = Path("test_output.wav")
        
        print(f"🎤 Testing TTS with text: {test_text}")
        print(f"📁 Output file: {output_path}")
        
        # Synthesize speech
        success = tts_provider.synthesize(test_text, output_path)
        
        if success:
            print("✅ TTS test successful!")
            print(f"📂 Audio file created: {output_path}")
            print(f"📏 File size: {output_path.stat().st_size} bytes")
            return True
        else:
            print("❌ TTS test failed!")
            return False
            
    except Exception as e:
        print(f"❌ TTS test error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Gemini TTS test...")
    test_gemini_tts()
