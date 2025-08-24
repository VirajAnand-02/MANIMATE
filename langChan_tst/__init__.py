"""
AI-Powered Educational Video Generator
A modular system for creating educational videos using LLMs and Manim
"""

__version__ = "2.0.0"
__author__ = "AI Video Generator Team"

# Core modules
from src.core.engine import VideoGenerationEngine, create_video_engine
from src.core.models import (
    VideoScript, Scene, ProcessingSummary,
    TTSConfig, ManimConfig, RenderConfig,
    TTSProvider, QualityPreset, LayoutType
)

# Providers
from src.providers.llm import BaseLLMProvider, create_llm_provider
from src.providers.tts import TTSProviderFactory

# Utilities
from src.utils.logging import setup_logging
from src.utils.file_ops import ensure_directory, create_timestamped_dir
from src.utils.video import VideoProcessor

__all__ = [
    # Core
    "VideoGenerationEngine",
    "create_video_engine",
    
    # Models
    "VideoScript",
    "Scene", 
    "ProcessingSummary",
    "TTSConfig",
    "ManimConfig", 
    "RenderConfig",
    "TTSProvider",
    "QualityPreset",
    "LayoutType",
    
    # Providers
    "BaseLLMProvider",
    "create_llm_provider",
    "TTSProviderFactory",
    
    # Utilities
    "setup_logging",
    "ensure_directory",
    "create_timestamped_dir",
    "VideoProcessor",
]
