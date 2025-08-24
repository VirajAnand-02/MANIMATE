#!/usr/bin/env python3
"""
Comprehensive test script for the video generation system
This script tests all components without making actual API calls
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch
import logging

# Set test environment
os.environ['GOOGLE_API_KEY'] = 'test_key_123'
os.environ['OPENAI_API_KEY'] = 'test_key_456'

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import project modules
from config.settings import validate_config, setup_directories
from src.core.models import VideoScript, Scene, LayoutType, TTSConfig, ManimConfig, RenderConfig
from src.core.engine import VideoGenerationEngine
from src.templates.layouts import TitleAndMainContent, SplitScreen
from src.utils.logging import setup_logging
from src.utils.file_ops import ensure_directory, clean_filename, save_json


def create_mock_script() -> VideoScript:
    """Create a mock video script for testing"""
    scenes = [
        Scene(
            seq=1,
            text="Welcome to our educational video about mathematics.",
            anim="Show a title and mathematical symbols floating in the background.",
            layout=LayoutType.TITLE_AND_MAIN
        ),
        Scene(
            seq=2,
            text="Let's explore the concept of matrix multiplication.",
            anim="Display two matrices and show the multiplication process step by step.",
            layout=LayoutType.SPLIT_SCREEN
        )
    ]
    
    return VideoScript(
        title="Mathematics: Matrix Multiplication",
        scenes=scenes
    )


def test_configuration():
    """Test configuration and directory setup"""
    print("=== Testing Configuration ===")
    
    # Test validation
    errors = validate_config()
    print(f"Config validation: {'✓' if not errors else '✗'}")
    if errors:
        for error in errors:
            print(f"  Error: {error}")
    
    # Test directory setup
    try:
        setup_directories()
        print("Directory setup: ✓")
    except Exception as e:
        print(f"Directory setup: ✗ - {e}")
        return False
    
    return True


def test_models():
    """Test data models"""
    print("\n=== Testing Data Models ===")
    
    try:
        # Test Scene model
        scene = Scene(
            seq=1,
            text="Test scene",
            anim="Test animation",
            layout=LayoutType.TITLE_AND_MAIN
        )
        print("Scene model: ✓")
        
        # Test VideoScript model
        script = VideoScript(
            title="Test Video",
            scenes=[scene]
        )
        print("VideoScript model: ✓")
        
        # Test configuration models
        tts_config = TTSConfig()
        manim_config = ManimConfig()
        render_config = RenderConfig()
        print("Configuration models: ✓")
        
        return True
        
    except Exception as e:
        print(f"Model testing failed: ✗ - {e}")
        return False


def test_templates():
    """Test Manim templates"""
    print("\n=== Testing Manim Templates ===")
    
    try:
        # Test template instantiation
        title_template = TitleAndMainContent()
        split_template = SplitScreen()
        
        # Test textbox creation
        test_text = title_template.create_textbox("Test", 100, 50)
        print("Template instantiation: ✓")
        
        return True
        
    except Exception as e:
        print(f"Template testing failed: ✗ - {e}")
        return False


def test_file_operations():
    """Test file operations"""
    print("\n=== Testing File Operations ===")
    
    try:
        from src.utils.file_ops import clean_filename, save_json, load_json
        
        # Test filename cleaning
        dirty_name = 'test<>:"/\\|?*file.txt'
        clean_name = clean_filename(dirty_name)
        assert '<' not in clean_name and '>' not in clean_name
        print("Filename cleaning: ✓")
        
        # Test JSON operations
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.json"
            test_data = {"test": "data", "number": 42}
            
            # Save and load
            save_json(test_data, test_file)
            loaded_data = load_json(test_file)
            assert loaded_data == test_data
            print("JSON operations: ✓")
        
        return True
        
    except Exception as e:
        print(f"File operations testing failed: ✗ - {e}")
        return False


def test_video_engine_mock():
    """Test video generation engine with mocked dependencies"""
    print("\n=== Testing Video Generation Engine (Mocked) ===")
    
    try:
        # Create mock script
        script = create_mock_script()
        print("Mock script creation: ✓")
        
        # Mock external dependencies
        with patch('src.providers.llm.genai') as mock_genai, \
             patch('src.providers.tts.genai') as mock_tts_genai, \
             patch('subprocess.run') as mock_subprocess:
            
            # Setup mocks
            mock_genai.configure = MagicMock()
            mock_genai.Client.return_value = MagicMock()
            mock_tts_genai.configure = MagicMock()
            mock_tts_genai.Client.return_value = MagicMock()
            
            # Mock successful subprocess calls (for manim and ffmpeg)
            mock_subprocess.return_value = MagicMock(returncode=0)
            
            # Test engine creation
            engine = VideoGenerationEngine()
            print("Engine instantiation: ✓")
            
            # Test internal methods
            archive_dir = engine._setup_archive("test_topic")
            assert archive_dir.exists()
            print("Archive setup: ✓")
            
            # Test script saving
            engine._save_script(script, archive_dir)
            script_file = archive_dir / "llm_outputs" / "script_generation.json"
            assert script_file.exists()
            print("Script saving: ✓")
            
            # Test fallback code generation
            scene_data = {"seq": 1, "text": "Test text", "anim": "Test animation"}
            fallback_code, class_name = engine._generate_fallback_scene(Scene(**scene_data, layout=LayoutType.TITLE_AND_MAIN))
            assert "Scene1" in class_name
            assert "Scene1" in fallback_code
            print("Fallback code generation: ✓")
        
        return True
        
    except Exception as e:
        print(f"Video engine testing failed: ✗ - {e}")
        import traceback
        traceback.print_exc()
        return False


def test_code_generation():
    """Test Manim code generation patterns"""
    print("\n=== Testing Code Generation Patterns ===")
    
    try:
        from src.core.engine import VideoGenerationEngine
        
        engine = VideoGenerationEngine()
        scene = Scene(
            seq=1,
            text="Test narration text",
            anim="Test animation description",
            layout=LayoutType.TITLE_AND_MAIN
        )
        
        # Test fallback code generation
        code, class_name = engine._generate_fallback_scene(scene)
        
        # Verify code structure
        assert f"class {class_name}(TitleAndMainContent):" in code
        assert "def construct_scene(self):" in code
        assert "narration_text" in code
        assert "audio_duration" in code
        print("Code structure validation: ✓")
        
        # Test code indentation
        indented = engine._indent_code("test_line\nanother_line")
        lines = indented.split('\n')
        for line in lines:
            if line.strip():  # Skip empty lines
                assert line.startswith('        ')  # 8 spaces
        print("Code indentation: ✓")
        
        return True
        
    except Exception as e:
        print(f"Code generation testing failed: ✗ - {e}")
        return False


def test_logging_system():
    """Test logging system"""
    print("\n=== Testing Logging System ===")
    
    try:
        from src.utils.logging import ProcessLogger, StatsLogger, setup_logging
        
        # Setup logging
        logger = setup_logging("INFO", include_console=False)
        print("Logging setup: ✓")
        
        # Test process logger
        process_logger = ProcessLogger("test_process")
        process_logger.start_process("Test Process", 3)
        process_logger.step("Step 1")
        process_logger.step("Step 2")
        process_logger.complete("Test completed")
        print("Process logging: ✓")
        
        # Test stats logger
        stats_logger = StatsLogger("test_stats")
        stats_logger.record("test_metric", 42)
        stats_logger.increment("counter")
        stats = stats_logger.get_stats()
        assert "test_metric" in stats
        assert stats["counter"] == 1
        print("Statistics logging: ✓")
        
        return True
        
    except Exception as e:
        print(f"Logging system testing failed: ✗ - {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 Starting Comprehensive System Test")
    print("=" * 50)
    
    test_results = [
        test_configuration(),
        test_models(),
        test_templates(),
        test_file_operations(),
        test_code_generation(),
        test_logging_system(),
        test_video_engine_mock(),
    ]
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready for use.")
        print("\n⚠️  Note: This test used mocked external dependencies.")
        print("   For actual video generation, you'll need:")
        print("   - Valid Google API key (for Gemini)")
        print("   - Valid OpenAI API key (optional, for OpenAI TTS)")
        print("   - Manim properly installed and configured")
        return True
    else:
        print("❌ Some tests failed. Please review the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
