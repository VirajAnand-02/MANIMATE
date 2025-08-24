"""
Data models for the video generation pipeline
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
import sys
from pathlib import Path

# Add project root to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config.settings import MANIM_MODEL, get_max_output_tokens_for_model, TTS_VOICE_NAME, TTS_PROVIDER


class LayoutType(str, Enum):
    """Available layout types"""
    TITLE_AND_MAIN = "title_and_main_content"
    SPLIT_SCREEN = "split_screen"
    CUSTOM = "custom"


class TTSProvider(str, Enum):
    """Available TTS providers"""
    GEMINI = "gemini"
    GEMINI_BATCH = "gemini_batch"
    OPENAI = "openai"
    DIA = "dia"
    MOCK = "mock"


def get_tts_provider_from_config() -> TTSProvider:
    """Get TTSProvider enum from config string"""
    try:
        return TTSProvider(TTS_PROVIDER)
    except ValueError:
        # Fallback to Gemini if invalid provider specified
        return TTSProvider.GEMINI


class QualityPreset(str, Enum):
    """Available quality presets"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    TWO_K = "2k"
    FOUR_K = "4k"


class Scene(BaseModel):
    """Scene model for video script"""
    seq: int = Field(description="Scene sequence number")
    text: str = Field(description="Scene narration text")
    anim: str = Field(description="Animation description")
    layout: LayoutType = Field(
        default=LayoutType.TITLE_AND_MAIN,
        description="Layout template to use"
    )


class VideoScript(BaseModel):
    """Video script model containing multiple scenes"""
    title: str = Field(description="Video title")
    scenes: List[Scene] = Field(description="List of scenes")
    
    def get_scene_count(self) -> int:
        """Get total number of scenes"""
        return len(self.scenes)
    
    def get_scene_by_seq(self, seq: int) -> Optional[Scene]:
        """Get scene by sequence number"""
        return next((scene for scene in self.scenes if scene.seq == seq), None)


class GenerationStats(BaseModel):
    """Statistics for generation process"""
    success: int = 0
    failed: int = 0
    fallback: int = 0
    thinking_success: int = 0
    non_thinking_success: int = 0
    self_corrected: int = 0
    correction_attempts: int = 0


class ProcessingSummary(BaseModel):
    """Summary of entire processing pipeline"""
    topic: str
    total_scenes: int = 0
    scenes: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Stats
    script_llm: Dict[str, Any] = Field(default_factory=dict)
    tts_stats: GenerationStats = Field(default_factory=GenerationStats)
    manim_stats: GenerationStats = Field(default_factory=GenerationStats)
    render_stats: GenerationStats = Field(default_factory=GenerationStats)
    audio_mux_stats: GenerationStats = Field(default_factory=GenerationStats)
    
    # Layout usage
    layout_stats: Dict[str, int] = Field(default_factory=lambda: {
        "title_and_main_content": 0,
        "split_screen": 0,
        "custom": 0
    })
    
    total_duration: float = 0.0
    
    def add_scene_summary(self, scene_summary: Dict[str, Any]):
        """Add a scene processing summary"""
        self.scenes.append(scene_summary)
        
        # Update layout stats
        layout = scene_summary.get("layout", "title_and_main_content")
        if layout in self.layout_stats:
            self.layout_stats[layout] += 1


class BatchRequest(BaseModel):
    """Batch processing request"""
    id: str
    scene_data: Dict[str, Any]
    layout: LayoutType
    system_prompt: str
    user_prompt: str


class BatchResponse(BaseModel):
    """Batch processing response"""
    id: str
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None


class ArchiveMetadata(BaseModel):
    """Metadata for archived content"""
    topic: str
    timestamp: str
    total_scenes: int
    generation_stats: ProcessingSummary
    archive_path: str
    
    # File listings
    audio_files: List[str] = Field(default_factory=list)
    scene_codes: List[str] = Field(default_factory=list)
    final_videos: List[str] = Field(default_factory=list)
    llm_outputs: List[str] = Field(default_factory=list)


class RenderConfig(BaseModel):
    """Configuration for video rendering"""
    quality: QualityPreset = QualityPreset.HIGH
    output_format: str = "mp4"
    include_audio: bool = True
    timeout: int = 180
    
    def get_manim_args(self) -> List[str]:
        """Get Manim command line arguments"""
        quality_map = {
            QualityPreset.LOW: "-ql",
            QualityPreset.MEDIUM: "-qm", 
            QualityPreset.HIGH: "-qh",
            QualityPreset.TWO_K: "-qp",
            QualityPreset.FOUR_K: "-qk"
        }
        
        # Ensure we get the string value of the enum
        quality_key = self.quality
        if isinstance(quality_key, str):
            # Convert string to enum if needed
            quality_key = QualityPreset(quality_key)
        
        args = [quality_map[quality_key]]
        
        if self.output_format == "gif":
            args.append("--format")
            args.append("gif")
            
        return args


class TTSConfig(BaseModel):
    """Configuration for TTS generation"""
    provider: TTSProvider = Field(default_factory=get_tts_provider_from_config)
    voice: str = TTS_VOICE_NAME  # Using environment variable
    model: Optional[str] = None
    speed: float = 1.0
    pitch: float = 0.0
    
    def get_provider_config(self) -> Dict[str, Any]:
        """Get provider-specific configuration"""
        config = {
            "voice": self.voice,
            "speed": self.speed,
            "pitch": self.pitch
        }
        
        if self.model:
            config["model"] = self.model
            
        return config


class ManimConfig(BaseModel):
    """Configuration for Manim code generation"""
    model: str = MANIM_MODEL
    use_thinking: bool = True
    thinking_budget: int = 6000
    max_output_tokens: int = Field(default_factory=lambda: get_max_output_tokens_for_model(MANIM_MODEL))
    temperature: float = 0.3
    use_batch: bool = True
    
    def get_generation_config(self) -> Dict[str, Any]:
        """Get generation configuration"""
        return {
            "max_output_tokens": self.max_output_tokens,
            "temperature": self.temperature,
            "thinking_budget": self.thinking_budget if self.use_thinking else 0
        }
