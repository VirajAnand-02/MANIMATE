"""
Simple test of video generation engine
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_engine():
    print("🧪 Testing Video Generation Engine")
    
    try:
        from src.core.engine import create_video_engine
        from src.core.models import TTSConfig, ManimConfig, RenderConfig
        from src.core.models import TTSProvider, QualityPreset
        
        print("✅ Imports successful")
        
        # Create configuration
        tts_config = TTSConfig(provider=TTSProvider.GEMINI, voice="Kore")
        manim_config = ManimConfig(use_thinking=False, use_batch=False)  # Disable complex features for test
        render_config = RenderConfig(quality=QualityPreset.MEDIUM)
        
        print("✅ Configuration created")
        
        # Create engine
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=manim_config,
            render_config=render_config
        )
        
        print("✅ Engine created successfully")
        print(f"   TTS Provider: {engine.tts_config.provider.value}")
        print(f"   Render Quality: {engine.render_config.quality.value}")
        
        # Check environment
        from config.settings import validate_config
        errors = validate_config()
        if errors:
            print("⚠️  Configuration issues:")
            for error in errors:
                print(f"   - {error}")
        else:
            print("✅ Configuration validated")
        
        print("\n🎉 Basic engine test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_engine()
