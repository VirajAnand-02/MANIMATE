"""
Final verification that the modular architecture is working
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def verify_architecture():
    """Verify the modular architecture works correctly"""
    print("🔍 Final Architecture Verification")
    print("=" * 50)
    
    test_results = []
    
    # Test 1: Import all core modules
    try:
        from src.core.engine import create_video_engine, VideoGenerationEngine
        from src.core.models import TTSConfig, ManimConfig, RenderConfig
        from src.core.models import TTSProvider, QualityPreset, LayoutType
        test_results.append(("Core modules import", True, ""))
    except Exception as e:
        test_results.append(("Core modules import", False, str(e)))
    
    # Test 2: Import providers
    try:
        from src.providers.llm import LLMProvider
        from src.providers.tts import TTSProviderFactory
        test_results.append(("Provider modules import", True, ""))
    except Exception as e:
        test_results.append(("Provider modules import", False, str(e)))
    
    # Test 3: Import utilities
    try:
        from src.utils.logging import setup_logging
        from src.utils.file_ops import ensure_directory
        from src.utils.video import VideoProcessor
        test_results.append(("Utility modules import", True, ""))
    except Exception as e:
        test_results.append(("Utility modules import", False, str(e)))
    
    # Test 4: Configuration
    try:
        from config.settings import validate_config, setup_directories
        errors = validate_config()
        has_config = len(errors) == 0 or all("API_KEY" in err for err in errors)  # API keys might not be set
        test_results.append(("Configuration system", has_config, f"{len(errors)} validation issues"))
    except Exception as e:
        test_results.append(("Configuration system", False, str(e)))
    
    # Test 5: Engine creation
    try:
        tts_config = TTSConfig(provider=TTSProvider.GEMINI)
        manim_config = ManimConfig()
        render_config = RenderConfig()
        
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=manim_config,
            render_config=render_config
        )
        test_results.append(("Engine creation", True, f"Engine type: {type(engine).__name__}"))
    except Exception as e:
        test_results.append(("Engine creation", False, str(e)))
    
    # Test 6: CLI import
    try:
        import main
        test_results.append(("CLI module import", True, ""))
    except Exception as e:
        test_results.append(("CLI module import", False, str(e)))
    
    # Display results
    print("\nTest Results:")
    print("-" * 50)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success, message in test_results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:<8} {test_name:<25} {message}")
        if success:
            passed += 1
    
    print("-" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ The modular architecture is working correctly")
        print("✅ All imports are functioning properly")
        print("✅ Configuration system is operational")
        print("✅ Engine creation is successful")
        print("✅ CLI is ready for use")
        
        print("\n🚀 Ready for video generation!")
        print("Try: python main.py \"machine learning basics\"")
        return True
    else:
        print(f"\n⚠️  {total-passed} tests failed")
        print("Some components may need attention")
        return False

if __name__ == "__main__":
    success = verify_architecture()
    sys.exit(0 if success else 1)
