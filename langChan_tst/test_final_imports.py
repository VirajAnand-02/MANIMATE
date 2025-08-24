"""
Final test to confirm all import issues are resolved
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_all_imports():
    """Test all critical imports"""
    print("🔧 Testing All Imports After Fix")
    print("=" * 40)
    
    try:
        # Test core imports
        print("1. Testing core imports...")
        from src.core.engine import create_video_engine, VideoGenerationEngine
        from src.core.models import TTSConfig, ManimConfig, RenderConfig
        from src.core.models import TTSProvider, QualityPreset
        print("   ✅ Core imports successful")
        
        # Test provider imports
        print("2. Testing provider imports...")
        from src.providers.llm import BaseLLMProvider, create_llm_provider, BatchManimLLM
        from src.providers.tts import TTSProviderFactory, create_tts_provider
        print("   ✅ Provider imports successful")
        
        # Test utility imports
        print("3. Testing utility imports...")
        from src.utils.logging import setup_logging
        from src.utils.file_ops import ensure_directory
        from src.utils.video import VideoProcessor
        print("   ✅ Utility imports successful")
        
        # Test configuration
        print("4. Testing configuration...")
        from config.settings import validate_config, setup_directories
        print("   ✅ Configuration imports successful")
        
        # Test engine creation
        print("5. Testing engine creation...")
        tts_config = TTSConfig(provider=TTSProvider.GEMINI)
        manim_config = ManimConfig()
        render_config = RenderConfig()
        
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=manim_config,
            render_config=render_config
        )
        print("   ✅ Engine creation successful")
        
        # Test main CLI import
        print("6. Testing main CLI...")
        import main
        print("   ✅ Main CLI import successful")
        
        print("\n" + "=" * 40)
        print("🎉 ALL IMPORTS WORKING!")
        print("✅ Import issues completely resolved")
        print("✅ Modular architecture is functional")
        print("✅ Ready for video generation")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_imports()
    if success:
        print("\n🚀 Try running: python main.py \"machine learning basics\"")
    sys.exit(0 if success else 1)
