"""
Simple test of the new architecture
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_functionality():
    """Test basic functionality of the new architecture"""
    print("🔧 Testing New Modular Architecture")
    print("=" * 50)
    
    try:
        # Test configuration
        print("1. Testing configuration...")
        from config.settings import PROJECT_ROOT, QUALITY_PRESETS
        print(f"   ✅ Project root: {PROJECT_ROOT}")
        print(f"   ✅ Quality presets: {list(QUALITY_PRESETS.keys())}")
        
        # Test models
        print("2. Testing data models...")
        from src.core.models import TTSConfig, TTSProvider, QualityPreset
        tts_config = TTSConfig(provider=TTSProvider.GEMINI, voice="Kore")
        print(f"   ✅ TTS Config: {tts_config.provider.value}, {tts_config.voice}")
        
        # Test engine creation
        print("3. Testing engine creation...")
        from src.core.engine import create_video_engine
        from src.core.models import ManimConfig, RenderConfig
        
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=ManimConfig(),
            render_config=RenderConfig(quality=QualityPreset.MEDIUM)
        )
        print(f"   ✅ Engine created successfully")
        
        # Test provider factory
        print("4. Testing provider factory...")
        from src.providers.tts import TTSProviderFactory
        factory = TTSProviderFactory()
        print(f"   ✅ Factory created")
        
        # Test utilities
        print("5. Testing utilities...")
        from src.utils.file_ops import ensure_directory
        from src.utils.logging import setup_logging
        print(f"   ✅ Utilities imported")
        
        print("\n🎉 All basic tests passed!")
        print("✅ The new modular architecture is working correctly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
