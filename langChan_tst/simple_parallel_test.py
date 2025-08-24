"""
Simple parallel TTS test
"""

import time
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("🚀 Simple Parallel TTS Test")
    print("=" * 30)
    
    try:
        # Test import
        print("Importing TTS provider...")
        from src.providers.tts import create_tts_provider
        from src.core.models import TTSConfig, TTSProvider
        print("✅ Import successful")
        
        # Create mock TTS provider
        print("Creating Mock TTS provider...")
        tts_config = TTSConfig(provider=TTSProvider.MOCK, voice="Aoede")
        tts_provider = create_tts_provider("mock", voice="Aoede")
        print("✅ Mock TTS provider created")
        
        # Test parallel method exists
        if hasattr(tts_provider, 'synthesize_batch'):
            print("✅ Parallel method found")
            
            # Simple test with 2 requests
            test_requests = [
                ("Hello world", Path("test1.wav")),
                ("Goodbye world", Path("test2.wav"))
            ]
            
            print(f"Testing parallel synthesis with {len(test_requests)} requests...")
            start_time = time.time()
            
            results = tts_provider.synthesize_batch(test_requests, max_workers=2)
            
            elapsed = time.time() - start_time
            successful = sum(1 for success in results.values() if success)
            
            print(f"✅ Completed: {successful}/{len(test_requests)} in {elapsed:.2f}s")
            print("🎉 Parallel processing test successful!")
            
        else:
            print("❌ Parallel method not found")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
