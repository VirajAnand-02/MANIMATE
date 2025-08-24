"""
Simple test for TTS provider import
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_tts_import():
    """Test TTS provider import directly"""
    try:
        from src.providers.tts import create_tts_provider
        print("✅ TTS provider imported successfully")
        return True
    except Exception as e:
        print(f"❌ TTS provider import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_engine_import():
    """Test engine import"""
    try:
        from src.core.engine import VideoGenerationEngine, create_video_engine
        print("✅ Engine imported successfully")
        return True
    except Exception as e:
        print(f"❌ Engine import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_parallel_import():
    """Test parallel module import"""
    try:
        from src.utils.parallel import ParallelProcessor
        print("✅ Parallel module imported successfully")
        return True
    except Exception as e:
        print(f"❌ Parallel module import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing imports...")
    print("=" * 40)
    
    success = True
    success &= test_parallel_import()
    success &= test_tts_import()
    success &= test_engine_import()
    
    if success:
        print("\n🎉 All imports successful!")
    else:
        print("\n❌ Some imports failed")
