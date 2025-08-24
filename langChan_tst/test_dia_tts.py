#!/usr/bin/env python3
"""
Test script for DiaTTS provider
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.providers.tts import create_tts_provider
from src.core.models import TTSConfig, TTSProvider

def test_dia_tts():
    """Test DiaTTS provider functionality"""
    
    # Create TTS configuration for Dia
    config = TTSConfig(
        provider=TTSProvider.DIA,
        voice="dialogue"  # This maps to voice_mode in Dia TTS
    )
    
    try:
        # Create the provider
        provider = create_tts_provider("dia", **config.get_provider_config())
        print(f"✓ DiaTTS provider created successfully")
        print(f"  Provider name: {provider.get_provider_name()}")
        print(f"  Base URL: {provider.base_url}")
        print(f"  Voice mode: {provider.default_config['voice_mode']}")
        print(f"  Timeout: {provider.default_config['timeout']}s")
        print(f"  Fallback enabled: {provider.enable_fallback}")
        
        # Test synthesis with a short text
        test_text = "Hello world, this is a test of the DiaTTS provider."
        output_path = Path("test_dia_output.wav")
        
        print(f"\n🎵 Testing synthesis...")
        print(f"  Text: {test_text}")
        print(f"  Output: {output_path}")
        
        success = provider.synthesize(test_text, output_path)
        
        if success:
            print(f"✓ Synthesis successful!")
            if output_path.exists():
                print(f"  File size: {output_path.stat().st_size} bytes")
            else:
                print(f"  Warning: Output file not found")
        else:
            print(f"✗ Synthesis failed (may have used fallback)")
            if output_path.exists():
                print(f"  Fallback file created, size: {output_path.stat().st_size} bytes")
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_chunked_synthesis():
    """Test chunked synthesis with longer text"""
    
    config = TTSConfig(
        provider=TTSProvider.DIA,
        voice="dialogue"
    )
    
    try:
        provider = create_tts_provider("dia", **config.get_provider_config())
        
        # Long text that should trigger chunking
        long_text = """
        This is a longer text that should demonstrate the chunking capability of the DiaTTS provider.
        When text is longer than the chunk size, it can be split into smaller parts for processing.
        This helps handle very long scripts that might otherwise fail or take too long to process.
        The provider supports both server-side chunking (default) and client-side chunking for compatibility.
        """
        
        output_path = Path("test_dia_chunked.wav")
        
        print(f"\n🎵 Testing chunked synthesis...")
        print(f"  Text length: {len(long_text)} characters")
        print(f"  Output: {output_path}")
        
        success = provider.synthesize_chunked(long_text, output_path, chunk_locally=False)
        
        if success:
            print(f"✓ Chunked synthesis successful!")
            if output_path.exists():
                print(f"  File size: {output_path.stat().st_size} bytes")
        else:
            print(f"✗ Chunked synthesis failed")
            
    except Exception as e:
        print(f"✗ Chunked test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== DiaTTS Provider Test ===\n")
    
    print("Configuration:")
    print(f"  Default base URL: http://139.84.154.247:8003")
    print(f"  Default voice mode: dialogue")
    print(f"  Default format: wav")
    print()
    
    test_dia_tts()
    test_chunked_synthesis()
    
    print(f"\n=== Test Complete ===")
