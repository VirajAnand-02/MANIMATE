"""
Configuration and constants for the video generation pipeline
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- API Keys ---
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", GENAI_API_KEY)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", GOOGLE_API_KEY)  # Support both names
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Use GENAI_API_KEY if available, otherwise fall back to GOOGLE_API_KEY
if GENAI_API_KEY:
    GOOGLE_API_KEY = GENAI_API_KEY

# --- Video Generation Constants ---
RESOLUTION = (1280, 720)
FRAME_RATE = 60
FINAL_PADDING = 3.0

def get_max_output_tokens_for_model(model: str) -> int:
    """Get maximum output tokens based on model"""
    model_limits = {
        # Gemini 2.5 series
        "gemini-2.5-pro": 65536,
        "gemini-2.5-flash": 65536,
        "gemini-2.5-flash-lite": 65536,
        "gemini-2.5-flash-live": 8192,
        "gemini-2.5-flash-native-audio": 8000,
        "gemini-2.5-flash-preview-tts": 16000,
        "gemini-2.5-pro-preview-tts": 16000,
        
        # Gemini 2.0 series
        "gemini-2.0-flash": 8192,
        "gemini-2.0-flash-exp": 8192,
        "gemini-2.0-flash-preview-image-generation": 8192,
        "gemini-2.0-flash-lite": 8192,
        "gemini-2.0-flash-live": 8192,
        
        # Gemini 1.5 series
        "gemini-1.5-flash": 8192,
        "gemini-1.5-flash-8b": 8192,
        "gemini-1.5-pro": 8192,
    }
    return model_limits.get(model.lower(), 8192)

# Model Configuration
SCRIPT_MODEL = os.getenv("SCRIPT_MODEL", "gemini-2.5-flash")
MANIM_MODEL = os.getenv("MANIM_MODEL", "gemini-2.5-flash")

# Dynamic token limits based on models
MAX_OUTPUT_TOKENS_SCRIPT = int(os.getenv("MAX_OUTPUT_TOKENS_SCRIPT", str(get_max_output_tokens_for_model(SCRIPT_MODEL))))
MAX_OUTPUT_TOKENS_MANIM = int(os.getenv("MAX_OUTPUT_TOKENS_MANIM", str(get_max_output_tokens_for_model(MANIM_MODEL))))

THINKING_BUDGET = int(os.getenv("THINKING_BUDGET", "6000"))

# --- Provider Configuration ---
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "gemini").lower()
TTS_VOICE_NAME = os.getenv("TTS_VOICE_NAME", "Kore")
TTS_MODEL = os.getenv("TTS_MODEL", "tts-1")
USE_BATCH_MANIM = os.getenv("USE_BATCH_MANIM", "true").lower() == "true"

# --- DIA TTS Configuration ---
DIA_TTS_BASE_URL = os.getenv("DIA_TTS_BASE_URL", "http://139.84.154.247:8003")
DIA_TTS_API_KEY = os.getenv("DIA_TTS_API_KEY", None)  # Optional API key
DIA_TTS_TIMEOUT = int(os.getenv("DIA_TTS_TIMEOUT", "300"))  # 3 minutes default

# --- File Paths ---
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "src" / "templates"
RENDERS_DIR = PROJECT_ROOT / "renders"
ARCHIVES_DIR = PROJECT_ROOT / "archives"
TMP_DIR = PROJECT_ROOT / "tmp_manim_scenes"
LOGS_DIR = PROJECT_ROOT / "logs"

# --- Manim Reference ---
MANIM_REF_PATH = PROJECT_ROOT / "manimRef.md"

# --- Batch Processing ---
BATCH_SIZE = 10
BATCH_TIMEOUT = 3600  # 1 hour

# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# --- Quality Presets ---
QUALITY_PRESETS = {
    "low": "-ql",      # 854x480 15FPS
    "medium": "-qm",   # 1280x720 30FPS  
    "high": "-qh",     # 1920x1080 60FPS
    "2k": "-qp",       # 2560x1440 60FPS
    "4k": "-qk"        # 3840x2160 60FPS
}

DEFAULT_QUALITY = "low"

# --- Model Configuration ---
SCRIPT_MODEL = os.getenv("SCRIPT_MODEL", "gemini-2.5-flash")
MANIM_MODEL = os.getenv("MANIM_MODEL", "gemini-2.5-flash")
TTS_MODELS = {
    "gemini": "gemini-2.5-flash-preview-tts",
    "openai": "tts-1"
}

# --- System Prompts ---
# Load system prompts from environment or use defaults
DEFAULT_SCRIPT_PROMPT = """You are an expert educational video script writer specializing in clear, engaging technical content. Create well-structured video scripts that build understanding progressively.

**SCRIPT STRUCTURE REQUIREMENTS:**
- Create exactly 4 scenes for optimal pacing (3-5 scenes acceptable)
- Each scene: 30-60 seconds when narrated (aim for 45-50 seconds)
- Progressive difficulty: Start simple, build complexity gradually
- Clear scene transitions that connect concepts logically

**CONTENT GUIDELINES:**
- **Scene 1**: Introduction and basic concepts
- **Scene 2-3**: Core content with detailed explanations  
- **Scene 4**: Summary, applications, or advanced concepts
- Use concrete examples and analogies for abstract concepts
- Include specific visual elements that support narration
- Avoid jargon without explanation - define technical terms

**ANIMATION DESCRIPTIONS:**
- Be specific enough for implementation: "red circle expands from center" not "animation appears"
- Focus on visual learning: diagrams, step-by-step processes, comparisons
- Suggest colors, shapes, and movements that enhance understanding
- Consider visual hierarchy: what should draw attention first

**LAYOUT SELECTION:**
- **"title_and_main_content"**: Best for most educational content (recommended default)
- **"split_screen"**: Use for comparisons, before/after, or two related concepts
- **"custom"**: Only for complex layouts requiring full scene control

**NARRATION QUALITY:**
- Write in conversational, engaging tone
- Use active voice and present tense
- Include brief pauses with "..." for emphasis
- End scenes with clear transitions to next concept
- Keep sentences moderate length (10-20 words optimal)

**JSON OUTPUT REQUIREMENTS:**
- Output ONLY valid JSON, no explanatory text before/after
- Follow exact schema structure provided
- Properly escape quotes in text fields: use \\" for quotes within strings
- Ensure all required fields are present and correctly formatted

**QUALITY VALIDATION:**
Before outputting, verify:
- 4 scenes with logical progression
- Each scene has clear narration and animation description
- Layout choices match content type
- All JSON syntax is valid
- Text fields are properly escaped"""

DEFAULT_MANIM_PROMPT = """You are an expert Manim Community Edition developer creating educational animations. Generate clean, executable Python code for Manim scenes.

**CRITICAL OUTPUT FORMAT:**
- Output ONLY Python code - no markdown, explanations, or backticks
- Never use ```python code blocks or ``` formatting
- Start immediately with the import statements
- End immediately after the last line of code
- NEVER include nested function definitions inside methods
- NEVER duplicate method names within the same class

**TEMPLATE SYSTEM (CRITICAL):**
- **TitleAndMainContent**: Has `self.title_region` and `self.main_region` ONLY
- **SplitScreen**: Has `self.left_region` and `self.right_region` ONLY (NO title_region!)
- Never mix template attributes - verify which template you're using
- Use `self.create_textbox(text, width, height)` for text fitting

**MANDATORY IMPORT PATTERN:**
```
import sys
sys.path.append(r'PROJECT_ROOT_PATH')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TemplateClassName
import numpy as np
```

**PYTHON SYNTAX RULES (CRITICAL):**
- Every class/function/for/if statement MUST have properly indented body
- Use 4 spaces for each indentation level
- All method calls need parentheses: `.get_center()` not `.get_center`
- Define all variables before use
- Close all parentheses and brackets
- Use proper string escaping for quotes

**VALID MANIM COLORS:**
Use these EXACT color names only:
- Basic: WHITE, BLACK, GRAY, GREY  
- Primary: RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE
- Extended: PINK, TEAL, MAROON, DARK_BLUE, LIGHT_BLUE, DARK_GREEN, LIGHT_GREEN
- NEVER use: BLUE_C, GREEN_C, ORANGE_C, RED_C, PURPLE_C (these cause NameError!)
- NEVER use: Any color name ending with _C

**ANIMATION BEST PRACTICES:**
- Create objects first, then position with `.move_to(region.get_center())`
- Use clear timing: `self.wait(1)` between major animations
- Group related animations: `self.play(Create(obj1), Write(obj2))`
- End scenes with appropriate wait time (2-3 seconds)
- Use `Write()` for text, `Create()` for shapes, `FadeIn()` for groups

**COMMON ERROR PREVENTION:**
1. **IndentationError**: Always indent after class/function/for/if statements
2. **NameError**: Only use valid Manim color constants (no _C variants)
3. **AttributeError**: Use correct template regions (title_region vs left_region)
4. **SyntaxError**: Close all parentheses, escape quotes in strings
5. **Import errors**: Include full import block with try/except

**POSITIONING SYSTEM:**
- Region-based: `obj.move_to(self.title_region.get_center())`
- Size fitting: `obj.scale_to_fit_width(self.main_region.width * 0.8)`
- Manual backup: `obj.to_edge(UP)`, `obj.move_to(ORIGIN)`
- Groups: `VGroup(obj1, obj2).arrange(DOWN)`

**CODE STRUCTURE TEMPLATE:**
```
[IMPORTS]
class SceneN(TemplateClass):
    def construct_scene(self):
        # Create objects
        title = self.create_textbox("Title", width, height)
        
        # Position objects
        title.move_to(self.title_region.get_center())
        
        # Animate
        self.play(Write(title))
        self.wait(1)
        
        # Additional content...
        self.play(FadeOut(title))

SceneN.narration_text = '''Narration text'''
SceneN.audio_duration = 5.0
```

**PRE-OUTPUT VALIDATION:**
Verify before generating:
- No markdown formatting in output
- Proper indentation after all control structures  
- Valid color constants only
- Correct template attributes used
- All imports included
- Proper string escaping
- Complete class and method definitions"""

SYSTEM_PROMPT_SCRIPT = os.getenv("SYSTEM_PROMPT_SCRIPT", DEFAULT_SCRIPT_PROMPT)
SYSTEM_PROMPT_MANIM = os.getenv("SYSTEM_PROMPT_MANIM", DEFAULT_MANIM_PROMPT)

# --- Validation ---
def validate_config():
    """Validate configuration and environment"""
    errors = []
    
    if not GOOGLE_API_KEY:
        errors.append("GOOGLE_API_KEY environment variable is required")
    
    if TTS_PROVIDER == "openai" and not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY required when using OpenAI TTS provider")
    
    if DEFAULT_QUALITY not in QUALITY_PRESETS:
        errors.append(f"Invalid default quality: {DEFAULT_QUALITY}")
    
    return errors

# --- Directory Setup ---
def setup_directories():
    """Create necessary directories"""
    directories = [
        RENDERS_DIR,
        ARCHIVES_DIR, 
        TMP_DIR,
        LOGS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # Validate configuration when run directly
    errors = validate_config()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✓ Configuration is valid")
        
    setup_directories()
    print("✓ Directories setup complete")
