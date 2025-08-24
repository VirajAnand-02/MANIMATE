#!/usr/bin/env python3
"""
generate_video.py
Demo pipeline:
 - Input: topic (terminal argument or prompt)
 - Use Google GenAI (Gemini) as Script LLM with a Pydantic schema for robust JSON
 - For each scene:
     - Generate TTS audio using a modular provider system (e.g., Gemini, OpenAI)
     - Generate Manim Python code (gemini-2.5-flash) with thinking enabled
     - Render Manim scene (manim CLI) to an mp4
     - Combine audio + scene video with ffmpeg, extending the last frame if needed
 - Concatenate scene mp4s into final output

Environment Variables:
 - TTS_PROVIDER: "gemini" (default), "gemini_batch", or "openai"
   - gemini_batch: Uses Gemini Batch API for 50% cost reduction and improved efficiency
 - TTS_VOICE_NAME: Voice to use (default: "Kore" for Gemini, "alloy" for OpenAI)
 - TTS_MODEL: Model to use (OpenAI only, default: "tts-1")
 - USE_BATCH_MANIM: "true" (default) or "false" - enables batch processing for Manim LLM
 - THINKING_BUDGET: Token budget for thinking (default: 6000)

CAVEAT: This executes model-generated Python. Run only in an isolated sandbox.
"""


import os
import sys
import json
import subprocess
import tempfile
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Tuple
from abc import ABC, abstractmethod
from openai import OpenAI
from google import genai
from google.genai import types
from layouts import TemplateScene, TitleAndMainContent, SplitScreen
import logging

# --- Constants ---
RESOLUTION = (1280, 720)
FRAME_RATE = 60
FINAL_PADDING = 3.0
THINKING_BUDGET = int(os.environ.get("THINKING_BUDGET", "6000"))
MAX_OUTPUT_TOKENS_MANIM = 8192

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('video_generation.log')
    ]
)

# API Keys and Config
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in environment variables.")

# Manim Prompts and Config
SYSTEM_PROMPT_MANIM = """you are an expert developer specializing in the Manim Community Python library. Your task is to write a single, complete, and runnable Python script for one scene of an educational video.

**CRITICAL RULES:**
1.  **Output ONLY Python code.** Do not include any explanatory text, comments, or markdown fences like ```python.
2.  The code must define a single Scene subclass named with the pattern `Scene{N}` where N is the scene number.
3.  The entire script must be self-contained and use only `from manim import *`. Do not use any other imports.
4.  **Pay extreme attention to syntax.** Ensure all parentheses `()`, brackets `[]`, and braces `{}` are correctly balanced and closed. This is a common source of errors.
5.  **Correctly call methods.** When using methods like `.get_center()`, `.get_top()`, or `.next_to()`, you MUST include the parentheses `()` to execute the method. For example, use `my_mobject.get_center()` NOT `my_mobject.get_center`.
6.  Use `MathTex` for mathematical formulas (e.g., `MathTex("R_1")`) and `Text` for plain text words.
7.  Create animations that are appropriate for the content - use reasonable timing with `self.play(...)` and `self.wait(...)` calls.
8.  Do not include any code that writes to files or interacts with the network.
"""
THINKING_BUDGET = int(os.environ.get("THINKING_BUDGET", "6000"))
MAX_OUTPUT_TOKENS_MANIM = 8192

# --- MODULAR TTS SYSTEM ---

class TTSProvider(ABC):
    """Abstract base class for Text-to-Speech providers."""
    @abstractmethod
    def synthesize(self, text: str, output_path: Path) -> Path:
        """
        Synthesizes audio from text and saves it to a file.
        Returns the path to the output file on success, or raises an exception on failure.
        """
        pass

class GeminiTTSProvider(TTSProvider):
    """TTS provider using Google's Gemini API."""
    def __init__(self, config: dict):
        self.client = genai.Client(api_key=config.get("api_key"))
        self.voice = config.get("voice", "Kore")

    def synthesize(self, text: str, output_path: Path) -> Path:
        try:
            resp = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts", contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=self.voice)))
                )
            )
            audio_data = resp.candidates[0].content.parts[0].inline_data.data
            write_bytes_to_wav(str(output_path), audio_data)
            print(f"Gemini TTS audio generated successfully: {output_path}")
            return output_path
        except Exception as e:
            print(f"Gemini TTS generation error: {e}")
            raise

class GeminiBatchTTSProvider(TTSProvider):
    """Batch TTS provider using Google's Gemini API Batch Mode."""
    def __init__(self, config: dict):
        self.client = genai.Client(api_key=config.get("api_key"))
        self.voice = config.get("voice", "Kore")
        self.batch_requests = []
        self.batch_paths = {}
        
    def add_to_batch(self, text: str, output_path: Path, request_key: str):
        """Add a TTS request to the batch."""
        self.batch_requests.append({
            "key": request_key,
            "request": {
                "contents": [{"parts": [{"text": text}]}],
                "config": {
                    "response_modalities": ["AUDIO"],
                    "speech_config": {
                        "voice_config": {
                            "prebuilt_voice_config": {
                                "voice_name": self.voice
                            }
                        }
                    }
                }
            }
        })
        self.batch_paths[request_key] = output_path
        
    def process_batch(self) -> Dict[str, Path]:
        """Process all batch requests and return paths keyed by request_key."""
        if not self.batch_requests:
            return {}
            
        print(f"Processing batch of {len(self.batch_requests)} TTS requests...")
        
        try:
            # Create batch job
            batch_job = self.client.batches.create(
                model="gemini-2.5-flash-preview-tts",
                src=self.batch_requests,
                config={
                    'display_name': f"tts-batch-{int(time.time())}",
                },
            )
            
            print(f"Created batch job: {batch_job.name}")
            
            # Monitor job status
            completed_states = {
                'JOB_STATE_SUCCEEDED',
                'JOB_STATE_FAILED', 
                'JOB_STATE_CANCELLED',
                'JOB_STATE_EXPIRED'
            }
            
            print("Waiting for batch job to complete...")
            while True:
                current_job = self.client.batches.get(name=batch_job.name)
                print(f"Job status: {current_job.state.name}")
                
                if current_job.state.name in completed_states:
                    break
                    
                time.sleep(10)  # Check every 10 seconds
                
            # Process results
            result_paths = {}
            if current_job.state.name == 'JOB_STATE_SUCCEEDED':
                print("Batch job completed successfully. Processing results...")
                
                for i, inline_response in enumerate(current_job.dest.inlined_responses):
                    request_key = self.batch_requests[i]["key"]
                    output_path = self.batch_paths[request_key]
                    
                    if inline_response.response:
                        try:
                            # Extract audio data from response
                            audio_data = inline_response.response.candidates[0].content.parts[0].inline_data.data
                            write_bytes_to_wav(str(output_path), audio_data)
                            result_paths[request_key] = output_path
                            print(f"✓ Generated audio for {request_key}: {output_path}")
                        except Exception as e:
                            print(f"✗ Failed to process audio for {request_key}: {e}")
                    elif inline_response.error:
                        print(f"✗ Error for {request_key}: {inline_response.error}")
                        
            else:
                print(f"Batch job failed with state: {current_job.state.name}")
                if current_job.error:
                    print(f"Error: {current_job.error}")
                    
            return result_paths
            
        except Exception as e:
            print(f"Batch TTS processing failed: {e}")
            # Fallback: process individually 
            print("Falling back to individual processing...")
            result_paths = {}
            for request_data in self.batch_requests:
                request_key = request_data["key"]
                text = request_data["request"]["contents"][0]["parts"][0]["text"]
                output_path = self.batch_paths[request_key]
                
                try:
                    # Use regular TTS as fallback
                    fallback_provider = GeminiTTSProvider({"api_key": self.client.api_key})
                    result_path = fallback_provider.synthesize(text, output_path)
                    result_paths[request_key] = result_path
                except Exception as fallback_e:
                    print(f"Fallback TTS also failed for {request_key}: {fallback_e}")
                    
            return result_paths
    
    def synthesize(self, text: str, output_path: Path) -> Path:
        """Individual synthesis method for compatibility (not recommended for batch use)."""
        # This is for compatibility but not efficient - use add_to_batch + process_batch instead
        request_key = f"single_{int(time.time())}"
        self.add_to_batch(text, output_path, request_key)
        results = self.process_batch()
        return results.get(request_key, output_path)

class OpenAITTSProvider(TTSProvider):
    """TTS provider using OpenAI's API."""
    def __init__(self, config: dict):
        if not config.get("api_key"):
            raise ValueError("OPENAI_API_KEY is required for OpenAITTSProvider.")
        self.client = OpenAI(api_key=config.get("api_key"))
        self.model = config.get("model", "tts-1")
        self.voice = config.get("voice", "alloy")

    def synthesize(self, text: str, output_path: Path) -> Path:
        try:
            # Note: OpenAI can output various formats. We'll use wav for consistency.
            output_path_str = str(output_path.with_suffix(".wav"))
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=text,
                response_format="wav"
            )
            response.stream_to_file(output_path_str)
            print(f"OpenAI TTS audio generated successfully: {output_path_str}")
            return Path(output_path_str)
        except Exception as e:
            print(f"OpenAI TTS generation error: {e}")
            raise

def get_tts_provider(provider_name: str, config: dict) -> TTSProvider:
    """Factory function to get a TTS provider instance."""
    providers = {
        "gemini": GeminiTTSProvider,
        "gemini_batch": GeminiBatchTTSProvider,
        "openai": OpenAITTSProvider,
    }
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise ValueError(f"Unknown TTS provider: {provider_name}. Available: {list(providers.keys())}")
    return provider_class(config)

# --- END MODULAR TTS SYSTEM ---

# Pydantic models for structured output
class Scene(BaseModel):
    seq: int
    text: str
    anim: str

class VideoScript(BaseModel):
    title: str
    scenes: List[Scene]

# Initialize GenAI client for non-TTS tasks
client = genai.Client(api_key=GENAI_API_KEY)

# Helpers

def write_bytes_to_wav(filename: str, pcm_bytes: bytes, channels: int = 1, rate: int = 24000, sample_width: int = 2) -> None:
    import wave
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_bytes)


def get_audio_duration(audio_path: Path) -> float:
    if not audio_path or not audio_path.exists():
        return 0.0
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio_path)
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        logging.warning(f"Could not get audio duration from {audio_path}: {e}")
        return 0.0


def get_video_duration(video_path: Path) -> float:
    if not video_path or not video_path.exists():
        return 0.0
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(video_path)
        ], capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        logging.warning(f"Could not get video duration from {video_path}: {e}")
        return 0.0

def call_script_llm(topic: str, max_retries=3):
    user_prompt = f"""
    Create a JSON structure for an educational video about "{topic}".

    Output ONLY valid JSON in this exact format:

    {{
      "title": "Video Title Here",
      "scenes": [
        {{
          "seq": 1,
          "text": "First scene narration text",
          "anim": "Description of what to animate or show"
        }},
        {{
          "seq": 2,
          "text": "Second scene narration text", 
          "anim": "Description of what to animate or show"
        }}
      ]
    }}

    Rules:
    - Output ONLY the JSON, no other text
    - Create 3-5 scenes 
    - Keep narration text clear and educational
    - Make animation descriptions specific and visual
    - Scene duration will be automatically determined by audio and animation content
    """
    for attempt in range(max_retries):
        try:
            print(f"Calling Script LLM with structured output (Attempt {attempt+1})...")
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=user_prompt,
                config={"response_mime_type": "application/json", "response_schema": VideoScript}
            )
            if not response.parsed: raise ValueError(f"Model failed to return a parsable script. Raw text: {response.text}")
            video_script_dict = response.parsed.model_dump()
            if "scenes" not in video_script_dict or not isinstance(video_script_dict["scenes"], list):
                raise ValueError("Script model did not return a valid 'scenes' list.")
            print("✓ Successfully generated and parsed video script.")
            return video_script_dict
        except Exception as e:
            print(f"[script LLM] attempt {attempt+1} failed: {e}"); time.sleep(2)
    raise RuntimeError("Script LLM failed after all retries.")

def choose_layout(scene_data: dict) -> str:
    """
    Uses an LLM to choose the best layout template for a given scene.
    """
    template_descriptions = """
    - "title_and_main_content": Best for a scene with a clear title and a primary animation or diagram below it.
    - "split_screen": Best for comparing two items side-by-side, or showing text on one side and an animation on the other.
    - "custom": Use this only when the animation is very complex, full-screen, or does not fit any other layout.
    """

    prompt = f"""
    Based on the following scene description, choose the best layout from the list.
    Respond with ONLY the name of the template (e.g., "split_screen").

    Scene Text: "{scene_data.get('text', '')}"
    Animation Description: "{scene_data.get('anim', '')}"

    Available Templates:
    {template_descriptions}

    Your choice:
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", # A fast model is fine for this
            contents=prompt,
            config={"temperature": 0.0} # We want deterministic output
        )
        choice = response.text.strip().replace('"', '')
        if choice not in ["title_and_main_content", "split_screen", "custom"]:
            print(f"Warning: Layout chooser returned an unknown layout '{choice}'. Defaulting to 'custom'.")
            return "custom"
        return choice
    except Exception as e:
        print(f"Warning: Layout chooser LLM failed: {e}. Defaulting to 'custom'.")
        return "custom"

class BatchManimLLM:
    """Batch Manim LLM provider using Google's Gemini API Batch Mode."""
    def __init__(self, config: dict):
        self.client = genai.Client(api_key=config.get("api_key"))
        self.batch_requests = []
        self.batch_data = {}
        
    def add_to_batch(self, scene_data: dict, scene_num: int, layout: str, request_key: str):
        """Add a Manim code generation request to the batch."""
        # NOTE: system_instruction and generation_config are handled in process_batch for this API.
        # The individual request only needs the user prompt.
        
        if layout == "custom":
            user_prompt = f"Create the COMPLETE animation for scene {scene_num}. Scene data:\n{json.dumps(scene_data, indent=2)}\nThe Scene class MUST be named `Scene{scene_num}`. Output ONLY Python code."
        else:
            regions = {
                "title_and_main_content": "`self.title_region` (for the title) and `self.main_region` (for the animation)",
                "split_screen": "`self.left_region` and `self.right_region`"
            }.get(layout, "")

            user_prompt = f"""
            You are writing the Python code for a Manim animation that will be placed inside a pre-existing template.
            Your task is to write ONLY the body of a method called `construct_scene(self)`. Do NOT write the class definition.

            The template provides these regions for you to use: {regions}.
            It also provides a helper method `self.create_textbox(text, width, height)` to create text that fits perfectly.

            Here is the scene information:
            - Scene Number: {scene_num}
            - Scene Data: {json.dumps(scene_data, indent=2)}

            Instructions:
            1. Create the title text using `self.create_textbox` and place it in the title/text region.
            2. Create the main animation described in "anim" and place it in the main/diagram region.
            3. Use `self.play()` and `self.wait()` as normal.
            4. For positioning: Use `text.move_to(self.region_name.get_center())` to position objects in regions.
            5. For sizing: Use `self.region_name.width` and `self.region_name.height` for dimensions.
            6. Output ONLY the Python code for the *body* of the `construct_scene` method.
            """
        
        # Create the request with only the 'contents' as required for batching text models.
        batch_request = {
            'contents': [{
                'parts': [{'text': user_prompt}],
                'role': 'user'
            }]
        }
        
        self.batch_requests.append(batch_request)
        self.batch_data[request_key] = {
            "scene_data": scene_data,
            "scene_num": scene_num,
            "layout": layout,
            "index": len(self.batch_requests) - 1  # Store index for mapping results
        }
        
    def process_batch(self) -> Dict[str, Tuple[str, bool]]:
        """Process all batch requests and return code keyed by request_key."""
        if not self.batch_requests:
            return {}
            
        logging.info(f"Processing batch of {len(self.batch_requests)} Manim LLM requests...")
        
        try:
            # Prepare system instruction and generation config for the entire batch job.
            manim_ref_content = ""
            try:
                with open(Path(__file__).parent / "manimRef.md", 'r', encoding='utf-8') as f:
                    manim_ref_content = f.read()
            except Exception as e:
                logging.warning(f"Could not read manimRef.md: {e}")
            
            system_instruction_text = f"{SYSTEM_PROMPT_MANIM}\n\n--- MANIM REFERENCE ---\n{manim_ref_content}"

            job_config = {
                'display_name': f"manim-batch-{int(time.time())}",
                'system_instruction': {
                    'parts': [{'text': system_instruction_text}]
                },
                'generation_config': {
                    'max_output_tokens': MAX_OUTPUT_TOKENS_MANIM,
                    'temperature': 0.1
                }
            }

            # Create batch job with the correct structure for the 'src' and 'config' parameters.
            batch_job = self.client.batches.create(
                model="gemini-2.5-pro",
                src={'inlined_requests': self.batch_requests},  # FIX: Wrap the list in a dictionary
                config=job_config,                            # FIX: Provide shared config here
            )
            
            logging.info(f"Created batch job: {batch_job.name}")
            
            # Monitor job status (no changes here)
            completed_states = {
                'JOB_STATE_SUCCEEDED',
                'JOB_STATE_FAILED', 
                'JOB_STATE_CANCELLED',
                'JOB_STATE_EXPIRED'
            }
            
            logging.info("Waiting for batch job to complete...")
            while True:
                current_job = self.client.batches.get(name=batch_job.name)
                logging.info(f"Job status: {current_job.state.name}")
                
                if current_job.state.name in completed_states:
                    break
                    
                time.sleep(10)
                
            # Process results (no changes here)
            result_codes = {}
            if current_job.state.name == 'JOB_STATE_SUCCEEDED':
                logging.info("Batch job completed successfully. Processing results...")
                
                for request_key, batch_info in self.batch_data.items():
                    index = batch_info["index"]
                    if index < len(current_job.dest.inlined_responses):
                        inline_response = current_job.dest.inlined_responses[index]
                        
                        if inline_response.response:
                            try:
                                text = inline_response.response.text
                                if "```python" in text:
                                    text = text.split("```python")[1].split("```").strip()
                                result_codes[request_key] = (text, True)
                                logging.info(f"✓ Generated code for {request_key}")
                            except Exception as e:
                                logging.error(f"✗ Failed to process code for {request_key}: {e}")
                        elif inline_response.error:
                            logging.error(f"✗ Error for {request_key}: {inline_response.error}")
                        
            else:
                logging.error(f"Batch job failed with state: {current_job.state.name}")
                if current_job.error:
                    logging.error(f"Error: {current_job.error}")
                    
            return result_codes
            
        except Exception as e:
            logging.error(f"Batch Manim LLM processing failed: {e}")
            logging.info("Falling back to individual processing...")
            result_codes = {}
            for request_key, batch_info in self.batch_data.items():
                try:
                    code, thinking_used = call_manim_llm_individual(
                        batch_info["scene_data"], 
                        batch_info["scene_num"], 
                        batch_info["layout"]
                    )
                    result_codes[request_key] = (code, thinking_used)
                except Exception as fallback_e:
                    logging.error(f"Fallback Manim LLM also failed for {request_key}: {fallback_e}")
                    
            return result_codes
        

def call_manim_llm_individual(scene_data: dict, scene_num: int, layout: str, max_retries=2):
    manim_ref_content = ""
    try:
        with open(Path(__file__).parent / "manimRef.md", 'r', encoding='utf-8') as f:
            manim_ref_content = f.read()
    except Exception as e:
        print(f"Warning: Could not read manimRef.md: {e}")
    
    system_instruction = f"{SYSTEM_PROMPT_MANIM}\n\n--- MANIM REFERENCE ---\n{manim_ref_content}"
    
    if layout == "custom":
        # The original prompt for full scene generation
        user_prompt = f"Create the COMPLETE animation for scene {scene_num}. Scene data:\n{json.dumps(scene_data, indent=2)}\nThe Scene class MUST be named `Scene{scene_num}`. Output ONLY Python code."
    else:
        # The new prompt for filling a template
        regions = {
            "title_and_main_content": "`self.title_region` (for the title) and `self.main_region` (for the animation)",
            "split_screen": "`self.left_region` and `self.right_region`"
        }.get(layout, "")

        user_prompt = f"""
        You are writing the Python code for a Manim animation that will be placed inside a pre-existing template.
        Your task is to write ONLY the body of a method called `construct_scene(self)`. Do NOT write the class definition.

        The template provides these regions for you to use: {regions}.
        It also provides a helper method `self.create_textbox(text, width, height)` to create text that fits perfectly.

        Here is the scene information:
        - Scene Number: {scene_num}
        - Scene Data: {json.dumps(scene_data, indent=2)}

        Instructions:
        1. Create the title text using `self.create_textbox` and place it in the title/text region.
        2. Create the main animation described in "anim" and place it in the main/diagram region.
        3. Use `self.play()` and `self.wait()` as normal.
        4. For positioning: Use `text.move_to(self.region_name.get_center())` to position objects in regions.
        5. For sizing: Use `self.region_name.width` and `self.region_name.height` for dimensions.
        6. Output ONLY the Python code for the *body* of the `construct_scene` method.
        """
    
    for attempt in range(max_retries):
        try:
            use_thinking = (attempt == 0)
            print(f"Manim LLM attempt {attempt+1}/{max_retries} {'(with thinking)' if use_thinking else '(without thinking)'}")
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                thinking_config=types.ThinkingConfig(thinking_budget=THINKING_BUDGET) if use_thinking else None,
                max_output_tokens=MAX_OUTPUT_TOKENS_MANIM
            )
            resp = client.models.generate_content(model="gemini-2.5-pro", contents=user_prompt, config=config)
            text = resp.text if hasattr(resp, 'text') and resp.text else resp.candidates[0].content.parts[0].text
            if not text: raise ValueError(f"No text from Manim LLM. Response: {resp}")
            if "```python" in text: text = text.split("```python")[1].split("```")[0].strip()
            print(f"✓ Manim LLM succeeded on attempt {attempt+1}")
            return text, use_thinking
        except Exception as e:
            print(f"[manim LLM] attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1: time.sleep(1)
    raise RuntimeError("Manim LLM failed after retries")

def get_narration_for_scene(scene_data: dict) -> str:
    return scene_data.get("text", "").strip()

def call_correction_llm(correction_prompt: str):
    system_instruction = f"{SYSTEM_PROMPT_MANIM}\n\nYou are correcting broken Manim code."
    try:
        print("Correction LLM attempt 1/1")
        config = types.GenerateContentConfig(system_instruction=system_instruction, max_output_tokens=MAX_OUTPUT_TOKENS_MANIM)
        resp = client.models.generate_content(model="gemini-2.5-flash", contents=correction_prompt, config=config)
        text = resp.text if hasattr(resp, 'text') and resp.text else resp.candidates[0].content.parts[0].text
        if not text: raise ValueError(f"No text from correction LLM. Response: {resp}")
        if "```python" in text: text = text.split("```python")[1].split("```")[0].strip()
        print("✓ Correction LLM succeeded")
        return text.strip()
    except Exception as e:
        print(f"[correction LLM] failed: {e}"); raise RuntimeError("Correction LLM failed")

def save_and_render_manim(scene_code: str, scene_class_name: str, output_dir: Path, tmpdir: Path):
    script_path = tmpdir / f"scene_{scene_class_name}.py"
    script_path.write_text(scene_code, encoding="utf-8")
    try:
        compile(scene_code, str(script_path), 'exec')
        print(f"✓ Code syntax is valid for {scene_class_name}")
    except SyntaxError as e:
        print(f"✗ Syntax error in generated code: {e}"); raise
    
    # Use Manim's built-in quality presets instead of custom resolution/frame rate
    # -qh = high quality (1920x1080 60FPS) - good balance of quality and render time
    # Alternative options: -ql (low), -qm (medium), -qp (2k), -qk (4k)
    cmd = [
        "manim", str(script_path.absolute()), scene_class_name,
        "-qh",  # High quality preset (1920x1080 60FPS)
        "--media_dir", str(output_dir.absolute())
    ]
    print(f"Running manim: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)
        print(f"✓ Manim render successful for {scene_class_name}")
    except subprocess.CalledProcessError as e:
        print(f"Manim failed. Stderr:\n{e.stderr}"); raise
    mp4_candidates = sorted(list(output_dir.rglob("*.mp4")), key=lambda p: p.stat().st_mtime, reverse=True)
    if not mp4_candidates: raise FileNotFoundError("No mp4 produced by Manim")
    return mp4_candidates[0]

def mux_audio_video(video_path: Path, audio_path: Path, out_path: Path):
    if audio_path and audio_path.exists():
        audio_duration, video_duration = get_audio_duration(audio_path), get_video_duration(video_path)
        video_padding_needed = max(0, audio_duration - video_duration)
        base_duration = max(audio_duration, video_duration)
        target_duration = base_duration + FINAL_PADDING
        logging.info(f"Video: {video_duration:.2f}s, Audio: {audio_duration:.2f}s. Holding last frame for {video_padding_needed:.2f}s.")
        logging.info(f"Final scene duration will be {target_duration:.2f}s.")
        filter_complex = f"[0:v]tpad=stop_mode=clone:stop_duration={video_padding_needed + FINAL_PADDING}[v];[1:a]apad=pad_dur={FINAL_PADDING}[a]"
        cmd = ["ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path), "-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-c:a", "aac", "-shortest", str(out_path)]
    else:
        video_duration = get_video_duration(video_path)
        target_duration = video_duration + FINAL_PADDING
        logging.info(f"Video: {video_duration:.2f}s, Target: {target_duration:.2f}s (no audio)")
        filter_complex = f"[0:v]tpad=stop_mode=clone:stop_duration={FINAL_PADDING}[v]"
        cmd = ["ffmpeg", "-y", "-i", str(video_path), "-filter_complex", filter_complex, "-map", "[v]", "-c:v", "libx264", "-t", str(target_duration), str(out_path)]
    logging.info(f"Running ffmpeg mux: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path

def concat_videos(video_paths, out_final):
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
        for p in video_paths: f.write(f"file '{os.path.abspath(str(p))}'\n")
        listfile = f.name
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", out_final]
    subprocess.run(cmd, check=True, capture_output=True)
    os.unlink(listfile)
    return out_final

def simple_text_scene_template(scene_data: dict):
    scene_num = scene_data.get("seq", 1)
    scene_name = f"Scene{scene_num}"
    text = scene_data.get("text", "Content could not be generated.")
    safe_text = text.replace('"', '\\"').replace('"""', '')[:200]
    
    # Use the template system for fallback as well
    current_dir = Path(__file__).parent
    code = f"""import sys
sys.path.append(r'{current_dir}')
from layouts import TitleAndMainContent

class {scene_name}(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene {scene_num}", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox(r\"\"\"{safe_text}\"\"\", 
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

{scene_name}.narration_text = r\"\"\"{safe_text}\"\"\"
{scene_name}.audio_duration = 5.0"""
    
    return code, scene_name

def main(topic: str):
    out_root = Path("renders")
    out_root.mkdir(exist_ok=True)
    
    # Create tmpdir in the project root instead of system temp
    project_root = Path(__file__).parent
    tmpdir = project_root / "tmp_manim_scenes"
    tmpdir.mkdir(exist_ok=True)
    print(f"Using tmpdir: {tmpdir}")
    
    # --- TTS Provider Setup ---
    tts_provider_name = os.environ.get("TTS_PROVIDER", "gemini").lower()
    tts_config = {
        "gemini": {"api_key": GENAI_API_KEY, "voice": os.environ.get("TTS_VOICE_NAME", "Kore")},
        "gemini_batch": {"api_key": GENAI_API_KEY, "voice": os.environ.get("TTS_VOICE_NAME", "Kore")},
        "openai": {"api_key": OPENAI_API_KEY, "model": os.environ.get("TTS_MODEL", "tts-1"), "voice": os.environ.get("TTS_VOICE_NAME", "alloy")}
    }
    try:
        tts_synthesizer = get_tts_provider(tts_provider_name, tts_config.get(tts_provider_name, {}))
        print(f"Using TTS Provider: {tts_provider_name}")
    except Exception as e:
        print(f"Error initializing TTS provider: {e}"); return
    # --- End TTS Provider Setup ---
    
    summary = {"topic": topic, "total_scenes": 0, "scenes": [], "tts_stats": {"success": 0, "failed": 0}, "manim_stats": {"success": 0, "failed": 0, "fallback": 0, "thinking_success": 0, "non_thinking_success": 0}, "render_stats": {"success": 0, "failed": 0, "fallback": 0, "self_corrected": 0}, "audio_mux_stats": {"success": 0, "failed": 0}, "layout_stats": {"title_and_main_content": 0, "split_screen": 0, "custom": 0}, "total_duration": 0}
    
    try:
        data = call_script_llm(topic)
        summary["script_llm"] = {"success": True}
    except Exception as e:
        print(f"Script LLM failed: {e}"); summary["script_llm"] = {"success": False, "error": str(e)}; return
    
    scenes = data.get("scenes", [])
    summary["total_scenes"] = len(scenes)
    if not scenes: print("No scenes generated. Exiting."); return
    print(f"Generated {len(scenes)} scenes for the video: {data.get('title')}")
    
    video_out_dir = out_root / "video"; video_out_dir.mkdir(parents=True, exist_ok=True)
    per_scene_outputs = []
    
    # === BATCH TTS PROCESSING ===
    # Check if we're using batch TTS provider
    use_batch_tts = isinstance(tts_synthesizer, GeminiBatchTTSProvider)
    scene_narrations = {}  # seq -> narration text
    scene_layouts = {}     # seq -> layout choice
    audio_files = {}       # seq -> audio file path
    
    if use_batch_tts:
        print(f"\n{'='*20} BATCH TTS PHASE {'='*20}")
        print("Collecting all narrations for batch processing...")
        
        # Step 1: Collect all narrations and add to batch
        for i, scene in enumerate(scenes):
            seq = scene.get("seq", i + 1)
            print(f"Processing scene {seq} for batch TTS...")
            
            # Choose layout (needed for later processing)
            layout_choice = choose_layout(scene)
            scene_layouts[seq] = layout_choice
            summary["layout_stats"][layout_choice] += 1
            
            # Get narration and add to batch
            narration = get_narration_for_scene(scene)
            if narration:
                scene_narrations[seq] = narration
                audio_path = tmpdir / f"scene_{seq}_audio.wav"
                tts_synthesizer.add_to_batch(narration, audio_path, f"scene_{seq}")
                print(f"Added scene {seq} to TTS batch")
        
        # Step 2: Process entire batch at once
        if scene_narrations:
            print(f"Processing batch of {len(scene_narrations)} TTS requests...")
            batch_results = tts_synthesizer.process_batch()
            
            # Map results back to scenes
            for seq in scene_narrations:
                request_key = f"scene_{seq}"
                if request_key in batch_results:
                    audio_files[seq] = batch_results[request_key]
                    print(f"✓ Batch TTS completed for scene {seq}")
                else:
                    print(f"✗ Batch TTS failed for scene {seq}")
        
        print(f"Batch TTS completed. Generated {len(audio_files)} audio files.")
    
    # === BATCH MANIM LLM PROCESSING ===
    # Check if we should use batch processing for Manim LLM (enabled by default)
    use_batch_manim = os.environ.get("USE_BATCH_MANIM", "true").lower() == "true"
    scene_codes = {}       # seq -> (code, thinking_used)
    
    if use_batch_manim:
        print(f"\n{'='*20} BATCH MANIM LLM PHASE {'='*20}")
        print("Collecting all scene requests for batch processing...")
        
        # Step 1: Collect all scene requests and add to batch
        batch_manim_llm = BatchManimLLM({"api_key": GENAI_API_KEY})
        
        for i, scene in enumerate(scenes):
            seq = scene.get("seq", i + 1)
            print(f"Processing scene {seq} for batch Manim LLM...")
            
            # Choose layout (reuse from TTS batch or compute now)
            if use_batch_tts:
                layout_choice = scene_layouts[seq]
            else:
                layout_choice = choose_layout(scene)
                scene_layouts[seq] = layout_choice
                summary["layout_stats"][layout_choice] += 1
            
            # Add to batch
            batch_manim_llm.add_to_batch(scene, seq, layout_choice, f"scene_{seq}")
            print(f"Added scene {seq} to Manim LLM batch")
        
        # Step 2: Process entire batch at once
        print(f"Processing batch of {len(scenes)} Manim LLM requests...")
        batch_results = batch_manim_llm.process_batch()
        
        # Map results back to scenes
        for seq in range(1, len(scenes) + 1):
            request_key = f"scene_{seq}"
            if request_key in batch_results:
                scene_codes[seq] = batch_results[request_key]
                print(f"✓ Batch Manim LLM completed for scene {seq}")
            else:
                print(f"✗ Batch Manim LLM failed for scene {seq}")
        
        print(f"Batch Manim LLM completed. Generated {len(scene_codes)} code snippets.")
    
    # === MAIN SCENE PROCESSING ===
    for i, scene in enumerate(scenes):
        seq = scene.get("seq", i + 1)
        print(f"\n{'='*20} Processing Scene {seq} {'='*20}")
        scene_out_dir = video_out_dir / f"scene_{seq}"; scene_out_dir.mkdir(exist_ok=True)
        scene_summary = {"scene_number": seq, "duration": 0.0, "layout": "", "tts": {}, "manim_llm": {}, "render": {}, "audio_mux": {}}
        
        # Get layout (either from batch processing or compute now)
        if use_batch_tts or use_batch_manim:
            layout_choice = scene_layouts[seq]
        else:
            # Step 1: Choose layout
            print(f"Choosing layout for scene {seq}...")
            layout_choice = choose_layout(scene)
            summary["layout_stats"][layout_choice] += 1
        
        print(f"Layout choice: {layout_choice}")
        scene_summary["layout"] = layout_choice
        
        # Get TTS (either from batch results or generate now)
        narration = get_narration_for_scene(scene)
        audio_file = None
        
        if use_batch_tts:
            # Use batch results
            if seq in audio_files:
                audio_file = audio_files[seq]
                scene_summary["tts"]["success"] = True
                summary["tts_stats"]["success"] += 1
                print(f"Using batch TTS result for scene {seq}")
            else:
                print(f"No batch TTS result for scene {seq}")
                scene_summary["tts"]["success"] = False
                summary["tts_stats"]["failed"] += 1
        else:
            # Step 2: Generate narration and TTS individually
            if narration:
                try:
                    # Use the synthesizer object
                    audio_file = tts_synthesizer.synthesize(narration, tmpdir / f"scene_{seq}_audio.wav")
                    scene_summary["tts"]["success"] = True; summary["tts_stats"]["success"] += 1
                except Exception as e:
                    print(f"TTS synthesis failed for scene {seq}: {e}")
                    scene_summary["tts"]["success"] = False; summary["tts_stats"]["failed"] += 1
        
        # Step 3: Generate Manim code with template system
        manim_code, scene_class_name = None, f"Scene{seq}"
        
        # Get Manim code (either from batch results or generate now)
        if use_batch_manim:
            # Use batch results
            if seq in scene_codes:
                manim_content_code, thinking_used = scene_codes[seq]
                scene_summary["manim_llm"]["success"] = True
                summary["manim_stats"]["success"] += 1
                if thinking_used: summary["manim_stats"]["thinking_success"] += 1
                else: summary["manim_stats"]["non_thinking_success"] += 1
                print(f"Using batch Manim LLM result for scene {seq}")
            else:
                print(f"No batch Manim LLM result for scene {seq}, using fallback")
                manim_content_code, thinking_used = None, False
                summary["manim_stats"]["failed"] += 1
        else:
            # Generate individually
            try:
                manim_content_code, thinking_used = call_manim_llm_individual(scene, seq, layout_choice)
                scene_summary["manim_llm"]["success"] = True
                summary["manim_stats"]["success"] += 1
                if thinking_used: summary["manim_stats"]["thinking_success"] += 1
                else: summary["manim_stats"]["non_thinking_success"] += 1
            except Exception as e:
                print(f"Manim LLM failed: {e}. Using fallback.")
                manim_content_code, thinking_used = None, False
                summary["manim_stats"]["failed"] += 1
        
        # Combine template and generated code if we have valid code
        if manim_content_code:
            
            # Combine template and generated code
            if layout_choice != "custom":
                # Get the template class name (capitalize first letter of each word)
                template_class_name = ''.join(word.capitalize() for word in layout_choice.split('_'))
                
                # Create the final code by inheriting from the template
                # Use absolute import path since the script will be in a subdirectory
                current_dir = Path(__file__).parent
                final_code = f"import sys\nsys.path.append(r'{current_dir}')\nfrom layouts import {template_class_name}\n\n"
                final_code += f"class Scene{seq}({template_class_name}):\n"
                final_code += "    def construct_scene(self):\n"
                # Indent the LLM's code correctly
                indented_content = "        " + manim_content_code.replace("\n", "\n        ")
                final_code += indented_content + "\n"
                scene_class_name = f"Scene{seq}"
            else:
                final_code = manim_content_code # The LLM wrote the whole thing
                scene_class_name = f"Scene{seq}" # Assuming the LLM follows the rule

            # Add narration info for the template to use
            audio_duration = get_audio_duration(audio_file) if audio_file else 0
            final_code += f'\nScene{seq}.narration_text = """{narration.replace(chr(34), chr(92) + chr(34))}"""\n'
            final_code += f'Scene{seq}.audio_duration = {audio_duration}\n'

            manim_code = final_code
        else:
            # Use fallback if no valid code was generated
            manim_code, scene_class_name = simple_text_scene_template(scene)
            summary["manim_stats"]["fallback"] += 1
        
        rendered_mp4 = None
        try:
            rendered_mp4 = save_and_render_manim(manim_code, scene_class_name, scene_out_dir, tmpdir)
            scene_summary["render"]["success"] = True; summary["render_stats"]["success"] += 1
        except Exception as e:
            print(f"Initial render failed: {e}. Attempting self-correction...")
            try:
                error_message = e.stderr if isinstance(e, subprocess.CalledProcessError) else str(e)
                correction_prompt = f"The Manim code failed.\nSCENE DATA:\n{json.dumps(scene)}\nFAILED CODE:\n{manim_code}\nERROR:\n{error_message}\nProvide a corrected, complete script. Output ONLY code."
                corrected_code = call_correction_llm(correction_prompt)
                rendered_mp4 = save_and_render_manim(corrected_code, scene_class_name, scene_out_dir, tmpdir)
                print("✓ Self-correction successful!"); scene_summary["render"]["success"] = True; summary["render_stats"]["success"] += 1; summary["render_stats"]["self_corrected"] += 1
            except Exception as correction_e:
                print(f"✗ Self-correction failed: {correction_e}. Trying text fallback.")
                try:
                    fallback_code, fallback_name = simple_text_scene_template(scene)
                    rendered_mp4 = save_and_render_manim(fallback_code, fallback_name, scene_out_dir, tmpdir)
                    scene_summary["render"]["success"] = True; summary["render_stats"]["success"] += 1; summary["render_stats"]["fallback"] += 1
                except Exception as fallback_e:
                    print(f"✗ Fallback render also failed: {fallback_e}"); summary["render_stats"]["failed"] += 1
        
        if not rendered_mp4: print(f"All rendering attempts for scene {seq} failed."); summary["scenes"].append(scene_summary); continue
        
        try:
            final_scene_mp4 = mux_audio_video(rendered_mp4, audio_file, scene_out_dir / f"scene_{seq}_final.mp4")
            scene_summary["audio_mux"]["success"] = True; summary["audio_mux_stats"]["success"] += 1; per_scene_outputs.append(final_scene_mp4)
            scene_duration = get_video_duration(final_scene_mp4)
            scene_summary["duration"] = scene_duration; summary["total_duration"] += scene_duration
        except Exception as e:
            print(f"Audio muxing failed: {e}. Using video-only."); summary["audio_mux_stats"]["failed"] += 1; per_scene_outputs.append(rendered_mp4)
        
        summary["scenes"].append(scene_summary)
        
    if per_scene_outputs:
        final_file = out_root / f"{topic.replace(' ','_')}_final.mp4"
        concat_videos(per_scene_outputs, str(final_file))
        print(f"\nFinal video generated at: {final_file.absolute()}"); summary["output_file"] = str(final_file)
    else:
        print("\nNo scenes were successfully rendered."); summary["output_file"] = None
        
    print("\n" + "="*60 + "\nGENERATION SUMMARY\n" + "="*60)
    print(f"Topic: {summary['topic']}")
    print(f"Total Duration: {summary['total_duration']:.2f} seconds")
    print(f"Script LLM: {'✓ Success' if summary.get('script_llm', {}).get('success') else '✗ Failed'}")
    print(f"\nScenes processed: {len(summary['scenes'])}")
    
    print(f"\nLayout Stats:")
    print(f"  Title & Main Content: {summary['layout_stats']['title_and_main_content']}")
    print(f"  Split Screen: {summary['layout_stats']['split_screen']}")
    print(f"  Custom: {summary['layout_stats']['custom']}")
    
    print(f"\nTTS Stats:")
    print(f"  Successful: {summary['tts_stats']['success']}")
    print(f"  Failed: {summary['tts_stats']['failed']}")
    
    print(f"\nManim LLM Stats:")
    print(f"  Successful: {summary['manim_stats']['success']}")
    print(f"    - With thinking: {summary['manim_stats']['thinking_success']}")
    print(f"    - Without thinking: {summary['manim_stats']['non_thinking_success']}")
    print(f"  Failed: {summary['manim_stats']['failed']}")
    print(f"  Fallback used: {summary['manim_stats']['fallback']}")
    
    print(f"\nRender Stats:")
    print(f"  Successful: {summary['render_stats']['success']}")
    print(f"  Self-corrected: {summary['render_stats']['self_corrected']}")
    print(f"  Failed: {summary['render_stats']['failed']}")
    print(f"  Fallback used: {summary['render_stats']['fallback']}")
    
    print(f"\nAudio Mux Stats:")
    print(f"  Successful: {summary['audio_mux_stats']['success']}")
    print(f"  Failed: {summary['audio_mux_stats']['failed']}")
    
    print(f"\nPer-Scene Details:")
    for i, scene in enumerate(summary['scenes'], 1):
        print(f"  Scene {i} (Duration: {scene['duration']:.2f}s, Layout: {scene['layout']}):")
        print(f"    TTS: {'✓' if scene['tts'].get('success') else '✗'}")
        print(f"    Manim: {'✓' if scene['manim_llm'].get('success') else '✗'}")
        print(f"    Render: {'✓' if scene['render'].get('success') else '✗'}")
        print(f"    Audio Mux: {'✓' if scene['audio_mux'].get('success') else '✗'}")
    
    print("="*60)
    
    # Cleanup tmpdir
    import shutil
    if tmpdir.exists():
        shutil.rmtree(tmpdir)
        print(f"Cleaned up tmpdir: {tmpdir}")
    
    return summary

if __name__ == "__main__":
    topic_arg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter topic: ").strip()
    if topic_arg: main(topic_arg)
    else: print("No topic provided.")