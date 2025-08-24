"""
Basic integration test for the new modular architecture
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.models import TTSConfig, ManimConfig, RenderConfig, TTSProvider, QualityPreset
from src.core.engine import create_video_engine
from config.settings import validate_config
from src.utils.logging import setup_logging


class TestArchitecture(unittest.TestCase):
    """Test the new modular architecture"""
    
    def setUp(self):
        """Set up test environment"""
        setup_logging("ERROR")  # Quiet during tests
    
    def test_config_validation(self):
        """Test configuration validation"""
        errors = validate_config()
        if errors:
            self.skipTest(f"Configuration not set up: {errors}")
    
    def test_model_creation(self):
        """Test Pydantic model creation"""
        # TTS Config
        tts_config = TTSConfig(
            provider=TTSProvider.GEMINI,
            voice="Kore"
        )
        self.assertEqual(tts_config.provider, TTSProvider.GEMINI)
        self.assertEqual(tts_config.voice, "Kore")
        
        # Manim Config
        manim_config = ManimConfig(
            use_thinking=True,
            thinking_budget=5000,
            use_batch=True
        )
        self.assertTrue(manim_config.use_thinking)
        self.assertEqual(manim_config.thinking_budget, 5000)
        
        # Render Config
        render_config = RenderConfig(
            quality=QualityPreset.MEDIUM,
            output_format="mp4"
        )
        self.assertEqual(render_config.quality, QualityPreset.MEDIUM)
    
    def test_engine_creation(self):
        """Test video engine creation"""
        tts_config = TTSConfig(provider=TTSProvider.GEMINI)
        manim_config = ManimConfig()
        render_config = RenderConfig()
        
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=manim_config,
            render_config=render_config
        )
        
        self.assertIsNotNone(engine)
        self.assertEqual(engine.tts_config.provider, TTSProvider.GEMINI)
    
    def test_import_structure(self):
        """Test that all modules can be imported"""
        try:
            # Core imports
            from src.core.engine import VideoGenerationEngine
            from src.core.models import VideoScript, Scene
            
            # Provider imports
            from src.providers.llm import BaseLLMProvider, create_llm_provider
            from src.providers.tts import TTSProviderFactory
            
            # Template imports
            from src.templates.layouts import TemplateScene
            
            # Utility imports
            from src.utils.logging import setup_logging
            from src.utils.file_ops import ensure_directory
            from src.utils.video import VideoProcessor
            
            # Config imports
            from config.settings import GEMINI_API_KEY, PROJECT_ROOT
            
        except ImportError as e:
            self.fail(f"Import failed: {e}")


class TestProviderFactory(unittest.TestCase):
    """Test provider factory patterns"""
    
    def test_tts_factory(self):
        """Test TTS provider factory"""
        from src.providers.tts import TTSProviderFactory
        
        # Test factory creation
        factory = TTSProviderFactory()
        
        # Test provider creation (will skip if API keys not configured)
        try:
            gemini_provider = factory.create_provider(TTSProvider.GEMINI)
            self.assertIsNotNone(gemini_provider)
        except Exception:
            self.skipTest("Gemini API not configured")


def run_architecture_test():
    """Run the architecture test"""
    print("🔍 Testing new modular architecture...")
    
    # Create test suite
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestArchitecture))
    suite.addTest(unittest.makeSuite(TestProviderFactory))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("✅ All architecture tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False


if __name__ == "__main__":
    success = run_architecture_test()
    sys.exit(0 if success else 1)
