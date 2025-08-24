#!/usr/bin/env python3
"""
Integration test that tests the main command-line interface without external APIs
"""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Set test environment
os.environ['GOOGLE_API_KEY'] = 'test_key_123'

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_main_cli_validation():
    """Test the main CLI validation and help"""
    print("=== Testing CLI Interface ===")
    
    try:
        from main import parse_arguments, create_configs_from_args, validate_environment
        
        # Test argument parsing with minimal args
        sys.argv = ['main.py', '--validate-only', 'test_topic']
        args = parse_arguments()
        assert args.validate_only == True
        print("Argument parsing: ✓")
        
        # Test config creation
        sys.argv = ['main.py', 'test_topic', '--quality', 'high', '--tts-provider', 'gemini']
        args = parse_arguments()
        tts_config, manim_config, render_config = create_configs_from_args(args)
        
        assert tts_config.provider.value == 'gemini'
        assert render_config.quality.value == 'high'
        print("Configuration creation: ✓")
        
        # Test validation
        valid = validate_environment()
        assert valid == True
        print("Environment validation: ✓")
        
        return True
        
    except Exception as e:
        print(f"CLI testing failed: ✗ - {e}")
        return False


def test_fallback_code_generation():
    """Test fallback code generation without API calls"""
    print("\n=== Testing Fallback Code Generation ===")
    
    try:
        from src.core.engine import VideoGenerationEngine
        from src.core.models import Scene, LayoutType
        
        engine = VideoGenerationEngine()
        
        # Test fallback scene generation
        scene = Scene(
            seq=1,
            text="This is a test scene with \"quotes\" and special characters.",
            anim="Simple animation description",
            layout=LayoutType.TITLE_AND_MAIN
        )
        
        code, class_name = engine._generate_fallback_scene(scene)
        
        # Verify the code is valid Python
        try:
            compile(code, '<string>', 'exec')
            print("Generated code compiles: ✓")
        except SyntaxError as e:
            print(f"Generated code syntax error: ✗ - {e}")
            print("Code preview:")
            print(code[:500] + "..." if len(code) > 500 else code)
            return False
        
        # Verify code structure
        assert f"class {class_name}(TitleAndMainContent):" in code
        assert "def construct_scene(self):" in code
        assert "narration_text" in code
        assert "audio_duration" in code
        print("Code structure validation: ✓")
        
        return True
        
    except Exception as e:
        print(f"Fallback code generation failed: ✗ - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_system():
    """Test the Manim template system"""
    print("\n=== Testing Template System ===")
    
    try:
        from src.templates.layouts import TitleAndMainContent, SplitScreen
        from manim import Text, Rectangle
        
        # Test title and main content template
        template = TitleAndMainContent()
        
        # Test textbox creation (this uses Manim which should be available)
        test_textbox = template.create_textbox("Test Text", 200, 100, font_size=24)
        assert isinstance(test_textbox, Text)
        print("Template textbox creation: ✓")
        
        # Test split screen template  
        split_template = SplitScreen()
        assert hasattr(split_template, 'left_region')
        assert hasattr(split_template, 'right_region')
        print("Split screen template: ✓")
        
        return True
        
    except Exception as e:
        print(f"Template system testing failed: ✗ - {e}")
        return False


def test_video_utils():
    """Test video utility functions (without actually processing video)"""
    print("\n=== Testing Video Utilities ===")
    
    try:
        from src.utils.video import get_video_info, get_audio_duration
        
        # These will fail gracefully with non-existent files
        # but we can test that the functions exist and handle errors properly
        
        # Test audio duration with non-existent file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            temp_path = Path(temp_audio.name)
        
        # This should return default fallback duration
        duration = get_audio_duration(temp_path)
        assert duration == 5.0  # Default fallback
        print("Audio duration fallback: ✓")
        
        # Clean up
        temp_path.unlink(missing_ok=True)
        
        return True
        
    except Exception as e:
        print(f"Video utilities testing failed: ✗ - {e}")
        return False


def test_project_structure():
    """Test that all required components are present"""
    print("\n=== Testing Project Structure ===")
    
    try:
        # Check that key files exist
        required_files = [
            'main.py',
            'config/settings.py',
            'src/core/engine.py',
            'src/core/models.py', 
            'src/providers/llm.py',
            'src/providers/tts.py',
            'src/templates/layouts.py',
            'src/utils/file_ops.py',
            'src/utils/video.py',
            'src/utils/logging.py'
        ]
        
        project_root = Path(__file__).parent
        for file_path in required_files:
            full_path = project_root / file_path
            assert full_path.exists(), f"Missing required file: {file_path}"
        
        print("Required files present: ✓")
        
        # Check that directories are created
        from config.settings import RENDERS_DIR, ARCHIVES_DIR, TMP_DIR, LOGS_DIR
        
        for directory in [RENDERS_DIR, ARCHIVES_DIR, TMP_DIR, LOGS_DIR]:
            assert directory.exists(), f"Missing directory: {directory}"
        
        print("Required directories present: ✓")
        
        return True
        
    except Exception as e:
        print(f"Project structure testing failed: ✗ - {e}")
        return False


def main():
    """Run integration tests"""
    print("🔧 Starting Integration Test")
    print("=" * 50)
    
    test_functions = [
        test_project_structure,
        test_main_cli_validation,
        test_template_system,
        test_fallback_code_generation,
        test_video_utils,
    ]
    
    results = []
    for test_func in test_functions:
        results.append(test_func())
    
    print("\n" + "=" * 50)
    print("📊 Integration Test Results")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        print("✅ The system is ready for use with real API keys.")
    else:
        print("❌ Some integration tests failed.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
