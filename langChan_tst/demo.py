"""
Demonstration script for the new modular architecture
Shows how to use the video generation system programmatically
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.engine import create_video_engine
from src.core.models import (
    TTSConfig, ManimConfig, RenderConfig,
    TTSProvider, QualityPreset
)
from src.utils.logging import setup_logging

def demo_video_generation():
    """Demonstrate the video generation system"""
    print("🎬 AI Video Generator v2.0 - Modular Architecture Demo")
    print("=" * 60)
    
    # Setup logging
    setup_logging("INFO", include_console=True)
    
    # Configure the system
    print("📋 Configuring video generation...")
    
    tts_config = TTSConfig(
        provider=TTSProvider.GEMINI,
        voice="Kore"
    )
    print(f"   🔊 TTS: {tts_config.provider.value} with voice '{tts_config.voice}'")
    
    manim_config = ManimConfig(
        use_thinking=True,
        thinking_budget=5000,
        use_batch=True
    )
    print(f"   🧠 Manim: Thinking={manim_config.use_thinking}, Batch={manim_config.use_batch}")
    
    render_config = RenderConfig(
        quality=QualityPreset.MEDIUM,
        output_format="mp4"
    )
    print(f"   🎥 Render: {render_config.quality.value} quality, {render_config.output_format} format")
    
    # Create the engine
    print("\n🚀 Creating video generation engine...")
    engine = create_video_engine(
        tts_config=tts_config,
        manim_config=manim_config,
        render_config=render_config
    )
    print("   ✅ Engine created successfully")
    
    # Show what would happen in a real generation
    print("\n📖 What happens during video generation:")
    print("   1. 🤖 LLM generates educational script from topic")
    print("   2. 🎭 Script is broken into scenes with narration")
    print("   3. 🔊 TTS provider converts text to speech")
    print("   4. 🎨 Manim code is generated for visual animations")
    print("   5. 🎬 Scenes are rendered and combined into final video")
    print("   6. 📁 All content is archived with timestamps")
    
    print("\n🏗️ Architecture highlights:")
    print("   📦 Modular design with clear separation of concerns")
    print("   🔧 Type-safe configuration with Pydantic models")
    print("   🏭 Factory patterns for provider extensibility")
    print("   📊 Comprehensive logging and progress tracking")
    print("   🗃️ Automated content archiving and organization")
    print("   🔄 Batch processing for improved efficiency")
    print("   ⚙️ Rich CLI with advanced options")
    
    print("\n✨ Ready for video generation!")
    print("   To generate a video, run:")
    print('   python main.py "machine learning basics"')
    print('   python main.py "quantum computing" --quality high --tts-provider openai')
    
    return True

if __name__ == "__main__":
    demo_video_generation()
