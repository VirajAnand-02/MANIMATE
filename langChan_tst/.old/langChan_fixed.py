#!/usr/bin/env python3
"""
Video generation pipeline using Google's GenAI API for educational content.
Enhanced with smart retry logic, self-correction, and comprehensive logging.
"""

import os
import json
import subprocess
import tempfile
import shutil
import time
import re
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

import google.generativeai as genai
import requests
from dotenv import load_dotenv

# Environment setup
script_dir = Path(__file__).parent
parent_dir = script_dir.parent
os.chdir(parent_dir)

# Load environment variables from .env file
load_dotenv()

GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in environment variables. Please check your .env file.")

# load prompts + config from env
SYSTEM_PROMPT_SCRIPT = os.environ.get("SYSTEM_PROMPT_SCRIPT", "").strip()

def get_manim_prompt():
    """Generate the complete SYSTEM_PROMPT_MANIM with dynamic reference loading."""
    base_prompt = """You are an expert developer specializing in the Manim Community Edition Python library. Your task is to write a single, complete, and runnable Python script for a Manim scene based on the provided scene description.

"""
    reference_content = load_manim_reference()
    
    closing_rules = """

- All method calls include parentheses
- LaTeX strings use raw string format r"..."
- Class name exactly matches GeneratedScene_{seq} format
- Only using `from manim import *` for imports"""
    
    return base_prompt + reference_content + closing_rules

TTS_VOICE_NAME = os.environ.get("TTS_VOICE_NAME", "Kore")
TTS_SPEAKING_SPEED = float(os.environ.get("TTS_SPEAKING_SPEED", "1.0"))
THINKING_BUDGET = int(os.environ.get("THINKING_BUDGET", "800"))

# Initialize the GenAI client with the API key
client = genai.Client(api_key=GENAI_API_KEY)

# Helpers

def load_manim_reference():
    """Load the Manim reference guide from external file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        ref_file = os.path.join(parent_dir, "manimRef.md")
        
        with open(ref_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Warning: manimRef.md not found, using basic prompt")
        return "Basic Manim reference not available."

def write_bytes_to_wav(filename: str, pcm_bytes: bytes, channels=1, rate=24000, sample_width=2):
    import wave
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_bytes)

def clean_filename(name: str) -> str:
    """Clean filename to be safe for filesystem"""
    # Remove or replace problematic characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Remove extra whitespace and replace with underscores
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    # Limit length
    if len(cleaned) > 100:
        cleaned = cleaned[:100]
    return cleaned

# Stats tracking
@dataclass
class ProcessingStats:
    """Track comprehensive processing statistics"""
    script_generations: int = 0
    script_successes: int = 0
    script_failures: int = 0
    
    manim_generations: int = 0
    manim_thinking_attempts: int = 0
    manim_non_thinking_attempts: int = 0
    manim_successes: int = 0
    manim_failures: int = 0
    
    correction_attempts: int = 0
    correction_successes: int = 0
    correction_failures: int = 0
    
    render_attempts: int = 0
    render_successes: int = 0
    render_failures: int = 0
    
    tts_generations: int = 0
    tts_successes: int = 0
    tts_failures: int = 0
    
    total_scenes_processed: int = 0
    total_scenes_successful: int = 0
    
    processing_times: Dict[str, List[float]] = field(default_factory=lambda: {
        'script_generation': [],
        'manim_generation': [],
        'correction_attempts': [],
        'render_times': [],
        'tts_generation': []
    })
    
    def add_time(self, category: str, duration: float):
        """Add processing time for a category"""
        if category in self.processing_times:
            self.processing_times[category].append(duration)
    
    def get_avg_time(self, category: str) -> float:
        """Get average time for a category"""
        times = self.processing_times.get(category, [])
        return sum(times) / len(times) if times else 0.0
    
    def print_summary(self):
        """Print comprehensive processing summary"""
        print("\n" + "="*60)
        print("PROCESSING SUMMARY")
        print("="*60)
        
        print(f"\nScript Generation:")
        print(f"  Attempts: {self.script_generations}")
        print(f"  Successes: {self.script_successes}")
        print(f"  Failures: {self.script_failures}")
        print(f"  Success Rate: {(self.script_successes/max(1,self.script_generations))*100:.1f}%")
        print(f"  Avg Time: {self.get_avg_time('script_generation'):.2f}s")
        
        print(f"\nManim Code Generation:")
        print(f"  Total Attempts: {self.manim_generations}")
        print(f"  Thinking Mode: {self.manim_thinking_attempts}")
        print(f"  Non-thinking Mode: {self.manim_non_thinking_attempts}")
        print(f"  Successes: {self.manim_successes}")
        print(f"  Failures: {self.manim_failures}")
        print(f"  Success Rate: {(self.manim_successes/max(1,self.manim_generations))*100:.1f}%")
        print(f"  Avg Time: {self.get_avg_time('manim_generation'):.2f}s")
        
        print(f"\nError Correction:")
        print(f"  Attempts: {self.correction_attempts}")
        print(f"  Successes: {self.correction_successes}")
        print(f"  Failures: {self.correction_failures}")
        print(f"  Success Rate: {(self.correction_successes/max(1,self.correction_attempts))*100:.1f}%")
        print(f"  Avg Time: {self.get_avg_time('correction_attempts'):.2f}s")
        
        print(f"\nManim Rendering:")
        print(f"  Attempts: {self.render_attempts}")
        print(f"  Successes: {self.render_successes}")
        print(f"  Failures: {self.render_failures}")
        print(f"  Success Rate: {(self.render_successes/max(1,self.render_attempts))*100:.1f}%")
        print(f"  Avg Time: {self.get_avg_time('render_times'):.2f}s")
        
        print(f"\nTTS Generation:")
        print(f"  Attempts: {self.tts_generations}")
        print(f"  Successes: {self.tts_successes}")
        print(f"  Failures: {self.tts_failures}")
        print(f"  Success Rate: {(self.tts_successes/max(1,self.tts_generations))*100:.1f}%")
        print(f"  Avg Time: {self.get_avg_time('tts_generation'):.2f}s")
        
        print(f"\nOverall Performance:")
        print(f"  Scenes Processed: {self.total_scenes_processed}")
        print(f"  Scenes Successful: {self.total_scenes_successful}")
        print(f"  Overall Success Rate: {(self.total_scenes_successful/max(1,self.total_scenes_processed))*100:.1f}%")
        
        print("="*60)

# Global stats instance
stats = ProcessingStats()

def call_llm_for_script(user_message: str) -> str:
    """Generate educational script using GenAI with comprehensive tracking"""
    start_time = time.time()
    stats.script_generations += 1
    
    try:
        print(f"[Script] Generating educational script...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                {"role": "system", "parts": [{"text": SYSTEM_PROMPT_SCRIPT}]},
                {"role": "user", "parts": [{"text": user_message}]}
            ],
            config={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_output_tokens": 2048,
                "response_mime_type": "text/plain"
            }
        )
        
        result = response.text.strip()
        duration = time.time() - start_time
        
        stats.script_successes += 1
        stats.add_time('script_generation', duration)
        
        print(f"[Script] ✓ Generated successfully in {duration:.2f}s")
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        stats.script_failures += 1
        stats.add_time('script_generation', duration)
        
        print(f"[Script] ✗ Failed after {duration:.2f}s: {e}")
        raise

def call_manim_llm(scene_description: str, seq: int, use_thinking: bool = True) -> str:
    """Generate Manim code with smart retry logic and comprehensive tracking"""
    start_time = time.time()
    stats.manim_generations += 1
    
    if use_thinking:
        stats.manim_thinking_attempts += 1
        model_name = "gemini-2.0-flash-thinking-exp"
        print(f"[Manim] Generating code for scene {seq} (thinking mode)...")
    else:
        stats.manim_non_thinking_attempts += 1
        model_name = "gemini-2.0-flash-exp"
        print(f"[Manim] Generating code for scene {seq} (non-thinking mode)...")
    
    try:
        system_prompt = get_manim_prompt()
        
        config = {
            "temperature": 0.3,
            "top_p": 0.9,
            "max_output_tokens": 4096,
            "response_mime_type": "text/plain"
        }
        
        # Add thinking budget for thinking models
        if use_thinking:
            config["thinking_budget"] = THINKING_BUDGET
        
        response = client.models.generate_content(
            model=model_name,
            contents=[
                {"role": "system", "parts": [{"text": system_prompt}]},
                {"role": "user", "parts": [{"text": f"Scene {seq}: {scene_description}"}]}
            ],
            config=config
        )
        
        result = response.text.strip()
        duration = time.time() - start_time
        
        stats.manim_successes += 1
        stats.add_time('manim_generation', duration)
        
        mode = "thinking" if use_thinking else "non-thinking"
        print(f"[Manim] ✓ Generated successfully in {duration:.2f}s ({mode})")
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        stats.manim_failures += 1
        stats.add_time('manim_generation', duration)
        
        mode = "thinking" if use_thinking else "non-thinking"
        print(f"[Manim] ✗ Failed after {duration:.2f}s ({mode}): {e}")
        raise

def call_correction_llm(original_code: str, error_message: str, scene_description: str, seq: int) -> str:
    """Generate corrected Manim code using error feedback"""
    start_time = time.time()
    stats.correction_attempts += 1
    
    try:
        print(f"[Correction] Analyzing error for scene {seq}...")
        
        correction_prompt = """You are an expert Manim developer tasked with fixing broken code. 

Analyze the error message and fix the provided Manim code. Return ONLY the complete, corrected Python code without any explanation or markdown formatting.

The code must:
- Use only `from manim import *` for imports
- Have proper class structure inheriting from Scene
- Use correct Manim CE syntax and methods
- Fix the specific error mentioned
- Maintain the original intent of the animation

Here is the broken code:
```python
{original_code}
```

Error message:
{error_message}

Scene description: {scene_description}

Return the complete corrected code:"""
        
        system_prompt = get_manim_prompt()
        user_prompt = correction_prompt.format(
            original_code=original_code,
            error_message=error_message,
            scene_description=scene_description
        )
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                {"role": "system", "parts": [{"text": system_prompt}]},
                {"role": "user", "parts": [{"text": user_prompt}]}
            ],
            config={
                "temperature": 0.1,  # Lower temperature for corrections
                "top_p": 0.9,
                "max_output_tokens": 4096,
                "response_mime_type": "text/plain"
            }
        )
        
        result = response.text.strip()
        duration = time.time() - start_time
        
        stats.correction_successes += 1
        stats.add_time('correction_attempts', duration)
        
        print(f"[Correction] ✓ Generated correction in {duration:.2f}s")
        return result
        
    except Exception as e:
        duration = time.time() - start_time
        stats.correction_failures += 1
        stats.add_time('correction_attempts', duration)
        
        print(f"[Correction] ✗ Failed after {duration:.2f}s: {e}")
        raise

def parse_scenes_from_script(script: str) -> List[str]:
    """Extract scenes from the educational script"""
    print("[Parser] Extracting scenes from script...")
    
    # Look for numbered scenes or sections
    scene_patterns = [
        r'(?:Scene|SCENE)\s*(\d+)[:\-\s]*(.+?)(?=(?:Scene|SCENE)\s*\d+|$)',
        r'(\d+)[\.\)\-\s]*(.+?)(?=\d+[\.\)\-\s]|$)',
        r'(?:^|\n)([^\n]+)(?=\n|$)'
    ]
    
    scenes = []
    found = False
    
    for pattern in scene_patterns:
        matches = re.findall(pattern, script, re.IGNORECASE | re.DOTALL)
        if matches:
            if isinstance(matches[0], tuple):
                scenes = [match[1].strip() if len(match) > 1 else match[0].strip() for match in matches]
            else:
                scenes = [match.strip() for match in matches]
            scenes = [scene for scene in scenes if len(scene) > 20]  # Filter out very short segments
            if len(scenes) >= 2:  # Need at least 2 substantial scenes
                found = True
                break
    
    if not found or len(scenes) < 2:
        # Fallback: split by paragraphs
        paragraphs = [p.strip() for p in script.split('\n\n') if p.strip()]
        scenes = [p for p in paragraphs if len(p) > 30]
        
        if len(scenes) < 2:
            # Final fallback: split by sentences
            sentences = re.split(r'[.!?]+', script)
            scenes = [s.strip() for s in sentences if len(s.strip()) > 30]
    
    # Limit to reasonable number of scenes
    scenes = scenes[:8]
    
    print(f"[Parser] ✓ Extracted {len(scenes)} scenes")
    for i, scene in enumerate(scenes, 1):
        preview = scene[:100] + "..." if len(scene) > 100 else scene
        print(f"  Scene {i}: {preview}")
    
    return scenes

def render_manim_scene(code: str, seq: int, output_dir: str, max_retries: int = 2) -> Optional[str]:
    """Render a Manim scene with error correction and comprehensive tracking"""
    stats.render_attempts += 1
    start_time = time.time()
    
    print(f"[Render] Starting render for scene {seq}...")
    
    # Create temporary directory for this scene
    scene_dir = os.path.join(output_dir, f"scene_{seq}")
    os.makedirs(scene_dir, exist_ok=True)
    
    # Write the code to a file
    scene_file = os.path.join(scene_dir, f"scene_{seq}.py")
    
    for attempt in range(max_retries + 1):
        try:
            print(f"[Render] Scene {seq}, attempt {attempt + 1}/{max_retries + 1}")
            
            # Clean and prepare the code
            cleaned_code = clean_manim_code(code, seq)
            
            with open(scene_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_code)
            
            # Run manim command
            scene_name = f"GeneratedScene_{seq}"
            cmd = [
                "manim", scene_file, scene_name,
                "--format", "mp4",
                "--media_dir", scene_dir,
                "-ql"  # Low quality for faster rendering
            ]
            
            print(f"[Render] Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=scene_dir,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                # Find the generated video file
                video_files = list(Path(scene_dir).rglob("*.mp4"))
                if video_files:
                    video_path = str(video_files[0])
                    duration = time.time() - start_time
                    
                    stats.render_successes += 1
                    stats.add_time('render_times', duration)
                    
                    print(f"[Render] ✓ Scene {seq} rendered successfully in {duration:.2f}s")
                    return video_path
                else:
                    raise Exception("No video file generated")
            else:
                error_output = result.stderr + result.stdout
                print(f"[Render] ✗ Scene {seq} render failed:")
                print(f"  Error: {error_output}")
                
                # Try error correction on the last attempt
                if attempt < max_retries:
                    print(f"[Render] Attempting error correction...")
                    try:
                        corrected_code = call_correction_llm(
                            code, error_output, f"Scene {seq}", seq
                        )
                        code = corrected_code  # Use corrected code for next attempt
                        print(f"[Render] Trying corrected code...")
                    except Exception as correction_error:
                        print(f"[Render] Correction failed: {correction_error}")
                        # Continue with original code
                
                if attempt == max_retries:
                    raise Exception(f"Render failed after {max_retries + 1} attempts: {error_output}")
                    
        except subprocess.TimeoutExpired:
            print(f"[Render] ✗ Scene {seq} render timed out")
            if attempt == max_retries:
                raise Exception("Render timed out")
        except Exception as e:
            print(f"[Render] ✗ Scene {seq} render error: {e}")
            if attempt == max_retries:
                duration = time.time() - start_time
                stats.render_failures += 1
                stats.add_time('render_times', duration)
                raise
    
    return None

def clean_manim_code(code: str, seq: int) -> str:
    """Clean and prepare Manim code for rendering"""
    # Remove markdown code blocks if present
    if "```python" in code:
        code = re.sub(r'```python\s*\n', '', code)
        code = re.sub(r'\n```', '', code)
    elif "```" in code:
        code = re.sub(r'```\s*\n', '', code)
        code = re.sub(r'\n```', '', code)
    
    # Ensure proper imports
    if "from manim import *" not in code:
        code = "from manim import *\n\n" + code
    
    # Fix class name to match expected pattern
    expected_class_name = f"GeneratedScene_{seq}"
    
    # Find existing class definition
    class_match = re.search(r'class\s+(\w+)\s*\([^)]*\):', code)
    if class_match:
        old_class_name = class_match.group(1)
        code = code.replace(f"class {old_class_name}", f"class {expected_class_name}")
    else:
        # No class found, wrap in a basic scene
        code = f"""from manim import *

class {expected_class_name}(Scene):
    def construct(self):
{chr(10).join('        ' + line for line in code.split(chr(10)) if line.strip())}
"""
    
    return code

def generate_tts_audio(text: str, output_path: str) -> bool:
    """Generate TTS audio using Google's Gemini TTS with comprehensive tracking"""
    start_time = time.time()
    stats.tts_generations += 1
    
    try:
        print(f"[TTS] Generating audio... (speed: {TTS_SPEAKING_SPEED}x)")
        
        # Clean text for TTS
        clean_text = re.sub(r'[*_#`]', '', text)  # Remove markdown
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Normalize whitespace
        
        if not clean_text:
            raise ValueError("No valid text content for TTS")
        
        # Generate audio using Gemini TTS
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[{
                "role": "user",
                "parts": [{"text": clean_text}]
            }],
            config={
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {
                            "voice_name": TTS_VOICE_NAME
                        }
                    }
                }
            }
        )
        
        # Get audio data
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content.parts:
                for part in candidate.content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        audio_data = part.inline_data.data
                        
                        # Write to temporary file
                        temp_path = output_path + ".temp"
                        with open(temp_path, 'wb') as f:
                            f.write(audio_data)
                        
                        # Adjust speed if needed
                        if TTS_SPEAKING_SPEED != 1.0:
                            speed_cmd = [
                                "ffmpeg", "-i", temp_path,
                                "-filter:a", f"atempo={TTS_SPEAKING_SPEED}",
                                "-y", output_path
                            ]
                        else:
                            speed_cmd = ["ffmpeg", "-i", temp_path, "-y", output_path]
                        
                        subprocess.run(speed_cmd, capture_output=True, check=True)
                        
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        
                        duration = time.time() - start_time
                        stats.tts_successes += 1
                        stats.add_time('tts_generation', duration)
                        
                        print(f"[TTS] ✓ Generated audio in {duration:.2f}s")
                        return True
        
        raise Exception("No audio data in response")
        
    except Exception as e:
        duration = time.time() - start_time
        stats.tts_failures += 1
        stats.add_time('tts_generation', duration)
        
        print(f"[TTS] ✗ Failed after {duration:.2f}s: {e}")
        return False

def combine_video_audio(video_path: str, audio_path: str, output_path: str) -> bool:
    """Combine video and audio using ffmpeg"""
    try:
        print(f"[Combine] Merging video and audio...")
        
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",  # Use shortest stream
            "-y",  # Overwrite output
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[Combine] ✓ Successfully combined video and audio")
            return True
        else:
            print(f"[Combine] ✗ Failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[Combine] ✗ Error: {e}")
        return False

def process_video_request(user_message: str, max_scenes: int = 5) -> str:
    """Main processing pipeline with comprehensive tracking and smart retry logic"""
    print("\n" + "="*60)
    print("STARTING VIDEO GENERATION PIPELINE")
    print("="*60)
    
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Create output directory
    output_dir = os.path.join("outputs", f"video_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Generate educational script
        print(f"\n[Pipeline] Step 1: Generating educational script")
        script = call_llm_for_script(user_message)
        
        # Save script
        script_file = os.path.join(output_dir, "script.txt")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script)
        print(f"[Pipeline] ✓ Script saved to {script_file}")
        
        # Step 2: Parse scenes
        print(f"\n[Pipeline] Step 2: Parsing scenes from script")
        scenes = parse_scenes_from_script(script)
        
        if not scenes:
            raise Exception("No scenes could be extracted from script")
        
        # Limit scenes
        scenes = scenes[:max_scenes]
        print(f"[Pipeline] ✓ Processing {len(scenes)} scenes")
        
        # Step 3: Generate and render each scene
        print(f"\n[Pipeline] Step 3: Generating and rendering scenes")
        successful_scenes = []
        
        for i, scene_desc in enumerate(scenes, 1):
            stats.total_scenes_processed += 1
            scene_success = False
            
            try:
                print(f"\n--- Processing Scene {i}/{len(scenes)} ---")
                
                # Try with thinking model first, fallback to non-thinking
                manim_code = None
                for use_thinking in [True, False]:
                    try:
                        manim_code = call_manim_llm(scene_desc, i, use_thinking)
                        break
                    except Exception as e:
                        if not use_thinking:  # Last attempt failed
                            raise e
                        print(f"[Pipeline] Thinking model failed, trying non-thinking...")
                        continue
                
                if not manim_code:
                    print(f"[Pipeline] ✗ Failed to generate code for scene {i}")
                    continue
                
                # Save generated code
                code_file = os.path.join(output_dir, f"scene_{i}_code.py")
                with open(code_file, 'w', encoding='utf-8') as f:
                    f.write(manim_code)
                
                # Render the scene
                video_path = render_manim_scene(manim_code, i, output_dir)
                
                if video_path and os.path.exists(video_path):
                    # Generate TTS audio
                    audio_file = os.path.join(output_dir, f"scene_{i}_audio.wav")
                    tts_success = generate_tts_audio(scene_desc, audio_file)
                    
                    if tts_success and os.path.exists(audio_file):
                        # Combine video and audio
                        final_video = os.path.join(output_dir, f"scene_{i}_final.mp4")
                        combine_success = combine_video_audio(video_path, audio_file, final_video)
                        
                        if combine_success and os.path.exists(final_video):
                            successful_scenes.append(final_video)
                            scene_success = True
                            stats.total_scenes_successful += 1
                            print(f"[Pipeline] ✓ Scene {i} completed successfully")
                        else:
                            # Use video without audio as fallback
                            successful_scenes.append(video_path)
                            scene_success = True
                            stats.total_scenes_successful += 1
                            print(f"[Pipeline] ⚠ Scene {i} completed (video only, no audio)")
                    else:
                        # Use video without audio as fallback
                        successful_scenes.append(video_path)
                        scene_success = True
                        stats.total_scenes_successful += 1
                        print(f"[Pipeline] ⚠ Scene {i} completed (video only, TTS failed)")
                else:
                    print(f"[Pipeline] ✗ Scene {i} render failed")
                    
            except Exception as e:
                print(f"[Pipeline] ✗ Scene {i} failed: {e}")
                # Continue with next scene
                continue
        
        # Step 4: Create final compilation if we have successful scenes
        if successful_scenes:
            print(f"\n[Pipeline] Step 4: Creating final video compilation")
            final_output = os.path.join("outputs", f"FinalVideo_{timestamp}.mp4")
            
            if len(successful_scenes) == 1:
                # Just copy the single video
                shutil.copy2(successful_scenes[0], final_output)
                print(f"[Pipeline] ✓ Single scene video saved as {final_output}")
            else:
                # Concatenate multiple videos
                concat_file = os.path.join(output_dir, "concat_list.txt")
                with open(concat_file, 'w') as f:
                    for video in successful_scenes:
                        f.write(f"file '{os.path.abspath(video)}'\n")
                
                concat_cmd = [
                    "ffmpeg",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", concat_file,
                    "-c", "copy",
                    "-y",
                    final_output
                ]
                
                result = subprocess.run(concat_cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"[Pipeline] ✓ Final video saved as {final_output}")
                else:
                    print(f"[Pipeline] ⚠ Concatenation failed, using first scene")
                    shutil.copy2(successful_scenes[0], final_output)
            
            # Print completion summary
            total_time = time.time() - start_time
            print(f"\n[Pipeline] ✓ PIPELINE COMPLETED in {total_time:.2f}s")
            print(f"[Pipeline] Successful scenes: {len(successful_scenes)}/{len(scenes)}")
            print(f"[Pipeline] Final video: {final_output}")
            
            # Print comprehensive stats
            stats.print_summary()
            
            return final_output
        else:
            raise Exception("No scenes were successfully processed")
            
    except Exception as e:
        total_time = time.time() - start_time
        print(f"\n[Pipeline] ✗ PIPELINE FAILED after {total_time:.2f}s: {e}")
        print(f"[Pipeline] Check output directory: {output_dir}")
        
        # Print stats even on failure
        stats.print_summary()
        
        raise

def main():
    """Main entry point"""
    if len(os.sys.argv) < 2:
        print("Usage: python langChan.py <topic>")
        print("Example: python langChan.py 'Explain the Pythagorean theorem'")
        return
    
    topic = ' '.join(os.sys.argv[1:])
    
    try:
        result = process_video_request(topic)
        print(f"\n🎉 Success! Video generated: {result}")
    except Exception as e:
        print(f"\n💥 Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
