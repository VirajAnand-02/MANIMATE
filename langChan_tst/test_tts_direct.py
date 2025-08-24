#!/usr/bin/env python3
"""
Direct test script for Gemini TTS functionality
"""

from google import genai
from google.genai import types
import wave
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from config.settings import GOOGLE_API_KEY
except ImportError:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Write PCM data to wave file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def test_gemini_tts_direct():
    """Test Gemini TTS directly using the example code"""
    
    # Get API key from config or environment
    api_key = GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in config or environment")
        return False
    
    try:
        print("🔑 API Key found, initializing client...")
        client = genai.Client(api_key=api_key)
        
        # Test text
        test_text = "Say cheerfully: Have a wonderful day!"
        output_path = "test_direct_output.wav"
        
        print(f"🎤 Testing TTS with text: {test_text}")
        print(f"📁 Output file: {output_path}")
        
        # Make TTS request
        print("📡 Making TTS request to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=test_text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Kore',
                        )
                    )
                ),
            )
        )
        
        print("📦 Response received, extracting audio data...")
        
        # Extract audio data
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    data = part.inline_data.data
                    
                    print(f"🎵 Audio data found, size: {len(data)} bytes")
                    
                    # Save as WAV file
                    wave_file(output_path, data)
                    
                    print("✅ TTS test successful!")
                    print(f"📂 Audio file created: {output_path}")
                    
                    # Check file size
                    file_size = Path(output_path).stat().st_size
                    print(f"📏 File size: {file_size} bytes")
                    
                    return True
        
        print("❌ No audio data found in response")
        return False
        
    except Exception as e:
        print(f"❌ TTS test error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting direct Gemini TTS test...")
    test_gemini_tts_direct()
