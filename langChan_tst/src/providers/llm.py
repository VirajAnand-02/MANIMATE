"""
Large Language Model provider implementations
"""

import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Optional imports with error handling
try:
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    # Create stubs to prevent import errors
    class genai:
        class Client:
            def __init__(self, api_key): pass
            
    class types:
        class GenerateContentConfig:
            def __init__(self, **kwargs): pass
        class Content:
            def __init__(self, **kwargs): pass
        class Part:
            def __init__(self, **kwargs): pass
    
    GOOGLE_GENAI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Google GenAI not available - Gemini LLM provider will be disabled")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    class OpenAI:
        def __init__(self, api_key): pass
    OPENAI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("OpenAI not available - OpenAI LLM provider will be disabled")

import sys
from pathlib import Path
# Add project root to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.models import (
    VideoScript, Scene, ManimConfig, BatchRequest, BatchResponse,
    LayoutType, ProcessingSummary
)

from config.settings import (
    GOOGLE_API_KEY, OPENAI_API_KEY, SYSTEM_PROMPT_SCRIPT, 
    SYSTEM_PROMPT_MANIM, MANIM_REF_PATH, SCRIPT_MODEL, MANIM_MODEL
)

logger = logging.getLogger(__name__)


def get_max_output_tokens(model: str) -> int:
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
    
    # Default to 8192 if model not found
    return model_limits.get(model.lower(), 8192)


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    def generate_script(self, topic: str) -> VideoScript:
        """Generate video script from topic"""
        pass
    
    @abstractmethod
    def generate_manim_code(self, scene_data: Dict[str, Any], layout: str) -> Tuple[str, str]:
        """Generate Manim code for a scene"""
        pass


class GeminiLLMProvider(BaseLLMProvider):
    """Gemini LLM provider implementation"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__(api_key or GOOGLE_API_KEY, model or SCRIPT_MODEL)
        if not GOOGLE_GENAI_AVAILABLE:
            raise ValueError("Google GenAI package not available - install with 'pip install google-genai'")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is required for Gemini LLM")
        
        self.client = genai.Client(api_key=self.api_key)
        self.manim_ref = self._load_manim_reference()
    
    def _load_manim_reference(self) -> str:
        """Load Manim reference documentation"""
        try:
            if MANIM_REF_PATH.exists():
                return MANIM_REF_PATH.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Could not load Manim reference: {e}")
        return "# Manim reference not available"
    
    def generate_script(self, topic: str) -> VideoScript:
        """Generate video script using Gemini"""
        try:
            logger.info(f"Generating script for topic: {topic}")
            
            prompt = f"""Create an educational video script about: {topic}

Output must be valid JSON with this exact structure:
{{
    "title": "Video title here",
    "scenes": [
        {{
            "seq": 1,
            "text": "Narration text for the scene",
            "anim": "Description of animation to show",
            "layout": "title_and_main_content"
        }}
    ]
}}

Guidelines:
- Create 3-5 scenes for a complete video
- Each scene should be 30-60 seconds of content
- Use layouts: "title_and_main_content", "split_screen", or "custom"
- Make animations visually engaging and educational
- Keep narration clear and concise

Output ONLY the JSON, no other text."""

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=get_max_output_tokens(self.model)
                )
            )
            
            # Extract response text with proper error handling
            response_text = ""
            if response and hasattr(response, 'text') and response.text:
                response_text = response.text.strip()
            elif response and hasattr(response, 'candidates') and response.candidates:
                # Try to extract from first candidate
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                response_text = part.text.strip()
                                break
            
            if not response_text:
                logger.error("Could not extract text from Gemini response")
                logger.error("This may be due to safety filters or API configuration issues")
                raise ValueError("Empty or filtered response from Gemini API")
            
            # Clean up response (remove markdown code blocks if present)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Convert to Pydantic model
            script = VideoScript(
                title=data["title"],
                scenes=[Scene(**scene) for scene in data["scenes"]]
            )
            
            logger.info(f"✓ Script generated with {len(script.scenes)} scenes")
            return script
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse script JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            raise
    
    def generate_manim_code(self, scene_data: Dict[str, Any], layout: str) -> Tuple[str, str]:
        """Generate Manim code for a scene"""
        try:
            scene_num = scene_data.get("seq", 1)
            narration = scene_data.get("text", "")
            animation = scene_data.get("anim", "")
            
            # Map layout to regions and template class
            regions_map = {
                "title_and_main_content": {
                    "regions": "`self.title_region` (for title) and `self.main_region` (for animation)",
                    "template_class": "TitleAndMainContent"
                },
                "split_screen": {
                    "regions": "`self.left_region` and `self.right_region`",
                    "template_class": "SplitScreen"
                }
            }
            
            layout_info = regions_map.get(layout, regions_map["title_and_main_content"])
            
            if layout == "custom":
                # Full scene generation
                user_prompt = f"""Create the COMPLETE Manim animation for scene {scene_num}.
                
Scene data:
- Narration: {narration}
- Animation: {animation}

The Scene class MUST be named `Scene{scene_num}`.
Output ONLY Python code, no explanation."""
            else:
                # Template-based generation
                user_prompt = f"""You are writing the Python code for a Manim animation that will be placed inside a pre-existing template.
Your task is to write ONLY the body of a method called `construct_scene(self)`. Do NOT write the class definition.

The template provides these regions for you to use: {layout_info['regions']}.
It also provides a helper method `self.create_textbox(text, width, height)` to create text that fits perfectly.
The template also provides BoundingBox objects for LayoutManager: use `self.title_bbox`, `self.main_bbox`, `self.left_bbox`, `self.right_bbox` as appropriate.

Scene information:
- Scene Number: {scene_num}
- Narration: {narration}
- Animation Description: {animation}

Instructions:
1. **USE LAYOUTMANAGER for positioning** instead of manual coordinates whenever possible.
2. Create the title text using `self.create_textbox` and add it to a LayoutManager for the title region.
3. Create the main animation described in "anim" and add it to a LayoutManager for the main region.
4. Use `self.play()` and `self.wait()` as normal.
5. For manual positioning (if needed): Use `text.move_to(self.region_name.get_center())` to position objects in regions.
6. For sizing: Use `self.region_name.width` and `self.region_name.height` for dimensions.
7. **Example LayoutManager usage in template:**
   ```python
   # Create layout manager for main region
   layout_manager = LayoutManager(self.main_bbox, padding=0.1)
   layout_manager.add(my_object, PreferredPosition.CENTER, priority=8)
   layout_manager.layout()
   for item in layout_manager.items:
       self.add(item.mobject)
   ```
8. Output ONLY the Python code for the *body* of the `construct_scene` method."""
            
            system_prompt = f"{SYSTEM_PROMPT_MANIM}\n\n--- MANIM REFERENCE ---\n{self.manim_ref}"
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(parts=[types.Part(text=system_prompt)], role="model"),
                    types.Content(parts=[types.Part(text=user_prompt)], role="user")
                ],
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=get_max_output_tokens(self.model)
                )
            )
            
            # Check if response has text content
            if not response or not hasattr(response, 'text') or response.text is None:
                logger.error("No text content in Gemini response for Manim generation")
                logger.debug(f"Response object: {response}")
                if hasattr(response, 'candidates') and response.candidates:
                    logger.debug(f"Candidates: {response.candidates}")
                raise ValueError("Empty response from Gemini API")
            
            code_content = response.text.strip()
            
            # Create full scene code
            if layout != "custom":
                template_class = layout_info["template_class"]
                current_dir = Path(__file__).parent.parent.parent
                
                full_code = f"""import sys
sys.path.append(r'{current_dir}')
from src.templates.layouts import {template_class}

class Scene{scene_num}({template_class}):
    def construct_scene(self):
{self._indent_code(code_content)}

# Set narration and duration
Scene{scene_num}.narration_text = '''{narration.replace("'", "\\'")}'''
Scene{scene_num}.audio_duration = 5.0
"""
            else:
                full_code = code_content
                # Add narration attributes
                full_code += f"""\n\n# Set narration and duration
Scene{scene_num}.narration_text = '''{narration.replace("'", "\\'")}'''
Scene{scene_num}.audio_duration = 5.0
"""
            
            logger.info(f"✓ Manim code generated for Scene {scene_num}")
            return full_code, f"Scene{scene_num}"
            
        except Exception as e:
            logger.error(f"Manim code generation failed: {e}")
            # Return fallback code
            return self._generate_fallback_code(scene_data)
    
    def _indent_code(self, code: str) -> str:
        """Indent code for class method"""
        lines = code.strip().split('\n')
        indented_lines = ['        ' + line if line.strip() else line for line in lines]
        return '\n'.join(indented_lines)
    
    def _generate_fallback_code(self, scene_data: Dict[str, Any]) -> Tuple[str, str]:
        """Generate fallback code when LLM fails"""
        scene_num = scene_data.get("seq", 1)
        text = scene_data.get("text", "Content could not be generated.")
        safe_text = text.replace('"', '\\"').replace('"""', '')[:200]
        
        current_dir = Path(__file__).parent.parent.parent
        code = f"""import sys
sys.path.append(r'{current_dir}')
from src.templates.layouts import TitleAndMainContent

class Scene{scene_num}(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene {scene_num}", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox(\"{safe_text}\", 
                                      self.main_region.width, 
                                      self.main_region.height, 
                                      font_size=24)
        main_text.move_to(self.main_region.get_center())
        
        # Animate
        self.play(Write(title_text))
        self.wait(1)
        self.play(Write(main_text))
        self.wait(3)
        self.play(FadeOut(title_text), FadeOut(main_text))

Scene{scene_num}.narration_text = \"{safe_text}\"
Scene{scene_num}.audio_duration = 5.0"""
        
        return code, f"Scene{scene_num}"


class BatchManimLLM:
    """Batch processing for Manim LLM generation"""
    
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GOOGLE_API_KEY
        self.model = model or MANIM_MODEL
        if not GOOGLE_GENAI_AVAILABLE:
            raise ValueError("Google GenAI package not available - install with 'pip install google-genai'")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY is required for batch Manim LLM")
        
        self.client = genai.Client(api_key=self.api_key)
        self.batch_requests: List[BatchRequest] = []
        self.batch_id: Optional[str] = None
        self.manim_ref = self._load_manim_reference()
    
    def _load_manim_reference(self) -> str:
        """Load Manim reference documentation"""
        try:
            if MANIM_REF_PATH.exists():
                return MANIM_REF_PATH.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Could not load Manim reference: {e}")
        return "# Manim reference not available"
    
    def add_to_batch(self, scene_data: Dict[str, Any], layout: str, request_id: str):
        """Add Manim generation request to batch"""
        scene_num = scene_data.get("seq", 1)
        narration = scene_data.get("text", "")
        animation = scene_data.get("anim", "")
        
        # Create prompts
        system_prompt = f"{SYSTEM_PROMPT_MANIM}\n\n--- MANIM REFERENCE ---\n{self.manim_ref}"
        
        if layout == "custom":
            user_prompt = f"Create the COMPLETE animation for scene {scene_num}. Scene data:\n{json.dumps(scene_data, indent=2)}\nThe Scene class MUST be named `Scene{scene_num}`. Output ONLY Python code."
        else:
            regions_map = {
                "title_and_main_content": "`self.title_region` (for title) and `self.main_region` (for animation)",
                "split_screen": "`self.left_region` and `self.right_region`"
            }
            regions = regions_map.get(layout, regions_map["title_and_main_content"])
            
            user_prompt = f"""You are writing the Python code for a Manim animation that will be placed inside a pre-existing template.
Your task is to write ONLY the body of a method called `construct_scene(self)`. Do NOT write the class definition.

The template provides these regions for you to use: {regions}.
It also provides a helper method `self.create_textbox(text, width, height)` to create text that fits perfectly.

Scene information:
- Scene Number: {scene_num}
- Narration: {narration}
- Animation Description: {animation}

Instructions:
1. Create the title text using `self.create_textbox` and place it in the title/text region.
2. Create the main animation described in "anim" and place it in the main/diagram region.
3. Use `self.play()` and `self.wait()` as normal.
4. For positioning: Use `text.move_to(self.region_name.get_center())` to position objects in regions.
5. For sizing: Use `self.region_name.width` and `self.region_name.height` for dimensions.
6. Output ONLY the Python code for the *body* of the `construct_scene` method."""
        
        request = BatchRequest(
            id=request_id,
            scene_data=scene_data,
            layout=LayoutType(layout),
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        
        self.batch_requests.append(request)
        logger.info(f"Added Manim request {request_id} to batch")
    
    def process_batch(self) -> Dict[str, BatchResponse]:
        """Process all Manim requests in batch"""
        if not self.batch_requests:
            return {}
        
        try:
            logger.info(f"Processing batch with {len(self.batch_requests)} Manim requests")
            
            # Process requests (simplified batch implementation)
            results = {}
            for req in self.batch_requests:
                try:
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=[
                            types.Content(parts=[types.Part(text=req.system_prompt)], role="model"),
                            types.Content(parts=[types.Part(text=req.user_prompt)], role="user")
                        ],
                        config=types.GenerateContentConfig(
                            temperature=0.3,
                            max_output_tokens=get_max_output_tokens(self.model)
                        )
                    )
                    
                    # Check if response has text content
                    if not response or not hasattr(response, 'text') or response.text is None:
                        logger.error(f"No text content in Gemini response for batch request {req.id}")
                        results[req.id] = BatchResponse(
                            id=req.id,
                            success=False,
                            content="",
                            error="Empty response from Gemini API"
                        )
                        continue
                    
                    results[req.id] = BatchResponse(
                        id=req.id,
                        success=True,
                        content=response.text.strip()
                    )
                    
                except Exception as e:
                    logger.error(f"Batch Manim generation failed for request {req.id}: {e}")
                    results[req.id] = BatchResponse(
                        id=req.id,
                        success=False,
                        error=str(e)
                    )
            
            # Clear batch
            self.batch_requests.clear()
            logger.info(f"✓ Batch Manim processing completed")
            return results
            
        except Exception as e:
            logger.error(f"Batch Manim processing failed: {e}")
            return {
                req.id: BatchResponse(id=req.id, success=False, error=str(e))
                for req in self.batch_requests
            }


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing when real providers are unavailable"""
    
    def __init__(self, api_key: str = None, model: str = None):
        super().__init__("mock_key", "mock_model")
    
    def generate_script(self, topic: str) -> VideoScript:
        """Generate a mock video script"""
        logger.info(f"Generating mock script for topic: {topic}")
        
        # Create a simple mock script
        mock_scenes = [
            Scene(
                seq=1,
                title=f"Introduction to {topic}",
                text=f"Welcome to this educational video about {topic}. In this video, we'll explore the fundamental concepts and applications.",
                duration=5.0
            ),
            Scene(
                seq=2,
                title=f"Understanding {topic}",
                text=f"Let's dive deeper into {topic} and understand its key principles and mechanisms.",
                duration=6.0
            ),
            Scene(
                seq=3,
                title=f"Examples of {topic}",
                text=f"Now, let's look at some practical examples of {topic} in action.",
                duration=5.5
            ),
            Scene(
                seq=4,
                title="Conclusion",
                text=f"In conclusion, {topic} is an important concept that has many practical applications. Thank you for watching!",
                duration=4.0
            )
        ]
        
        script = VideoScript(
            title=f"Understanding {topic}",
            scenes=mock_scenes
        )
        
        logger.info(f"✓ Mock script generated with {len(script.scenes)} scenes")
        return script
    
    def generate_manim_code(self, scene_data: Dict[str, Any], layout: str) -> Tuple[str, str]:
        """Generate mock Manim code"""
        logger.info(f"Generating mock Manim code for scene: {scene_data.get('title', 'Unknown')}")
        
        class_name = f"Scene{scene_data.get('seq', 1)}"
        
        # Create simple mock Manim code
        mock_code = f'''
import sys
sys.path.append(r'{Path(__file__).parent.parent.parent}')
from manim import *

class {class_name}(Scene):
    def construct(self):
        # Mock scene construction
        title = Text("{scene_data.get('title', 'Scene Title')}", font_size=48)
        title.to_edge(UP)
        
        content = Text(
            "{scene_data.get('text', 'Scene content goes here.')[:100]}...",
            font_size=24,
            line_spacing=1.5
        )
        content.next_to(title, DOWN, buff=1)
        content.set_width(config.frame_width - 2)
        
        self.play(Write(title))
        self.play(FadeIn(content))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(content))
'''
        
        return mock_code.strip(), class_name


def create_llm_provider(provider_name: str = "gemini", **kwargs) -> BaseLLMProvider:
    """Factory function to create LLM provider"""
    if provider_name.lower() == "gemini":
        try:
            return GeminiLLMProvider(**kwargs)
        except ValueError as e:
            if "Google GenAI package not available" in str(e):
                logger.warning("Google GenAI not available, falling back to Mock LLM provider")
                return MockLLMProvider(**kwargs)
            else:
                raise
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
