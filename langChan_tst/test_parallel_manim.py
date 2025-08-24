#!/usr/bin/env python3
"""
Test script specifically for parallel Manim rendering
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.engine import VideoGenerationEngine
from src.core.models import TTSConfig, ManimConfig, RenderConfig, TTSProvider, QualityPreset
from src.utils.logging import setup_logging

def test_parallel_manim():
    """Test parallel Manim rendering specifically"""
    
    # Setup logging
    setup_logging("INFO", include_console=True)
    
    # Create engine with parallel processing enabled
    engine = VideoGenerationEngine(
        tts_config=TTSConfig(provider=TTSProvider.MOCK),
        manim_config=ManimConfig(use_batch=False),  # Disable batch for simpler testing
        render_config=RenderConfig(quality=QualityPreset.LOW),
        enable_parallel=True,
        max_tts_workers=2,
        max_render_workers=2
    )
    
    print("🧪 Testing Parallel Manim Rendering")
    print(f"Engine parallel enabled: {engine.enable_parallel}")
    print(f"Manim parallel processor: {engine.manim_parallel is not None}")
    print(f"Max render workers: {engine.max_render_workers}")
    print("-" * 50)
    
    # Generate a video with multiple scenes to test parallel rendering
    success, summary = engine.generate_video("Simple parallel test topic")
    
    print("\n📊 Results:")
    print(f"Overall success: {success}")
    print(f"Total scenes: {summary.total_scenes}")
    print(f"TTS success: {summary.tts_stats.success}/{summary.total_scenes}")
    print(f"Code generation: {summary.manim_stats.success}/{summary.total_scenes}")
    print(f"Rendering success: {summary.render_stats.success}/{summary.total_scenes}")
    print(f"Audio mux success: {summary.audio_mux_stats.success}/{summary.total_scenes}")
    
    if summary.render_stats.self_corrected > 0:
        print(f"Self-corrections: {summary.render_stats.self_corrected}")
        print(f"Correction attempts: {summary.render_stats.correction_attempts}")
    
    print("\n✅ Test completed!")
    
    return success

if __name__ == "__main__":
    test_parallel_manim()
