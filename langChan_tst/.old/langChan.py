#!/usr/bin/env python3
"""
generate_video.py
Demo pipeline:
 - Input: topic (terminal argument or prompt)
 - Use Google GenAI (Gemini) as Script LLM with thinking to produce JSON of scenes
 - For each scene:
     - Generate TTS audio (gemini-2.5-flash-preview-tts) if narration text exists
     - Generate Manim Python code (gemini-2.5-flash) with thinking enabled
     - Render Manim scene (manim CLI) to an mp4
     - Combine audio + scene video with ffmpeg (if audio exists)
 - Concatenate scene mp4s into final output
CAVEAT: This executes model-generated Python. Run only in an isolated sandbox.
"""

import os
import sys
import json
import subprocess
import tempfile
import time
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Google genai client per user's snippet
from google import genai
from google.genai import types

load_dotenv()

GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("GENAI_API_KEY not found in environment variables. Please check your .env file.")

# load prompts + config from env
SYSTEM_PROMPT_SCRIPT = os.environ.get("SYSTEM_PROMPT_SCRIPT", "").strip()
# SYSTEM_PROMPT_MANIM = os.environ.get("SYSTEM_PROMPT_MANIM", "").strip()
SYSTEM_PROMPT_MANIM = """you are an expert developer specializing in the Manim Community Python library. Your task is to write a single, complete, and runnable Python script for one scene of an educational video.

**CRITICAL RULES:**
1.  **Output ONLY Python code.** Do not include any explanatory text, comments, or markdown fences like ```python.
2.  The code must define a single Scene subclass named with the pattern `Scene{N}` where N is the scene number.
3.  The entire script must be self-contained and use only `from manim import *`. Do not use any other imports.
4.  **Pay extreme attention to syntax.** Ensure all parentheses `()`, brackets `[]`, and braces `{}` are correctly balanced and closed. This is a common source of errors.
5.  **Correctly call methods.** When using methods like `.get_center()`, `.get_top()`, or `.next_to()`, you MUST include the parentheses `()` to execute the method. For example, use `my_mobject.get_center()` NOT `my_mobject.get_center`.
6.  Use `MathTex` for mathematical formulas (e.g., `MathTex("R_1")`) and `Text` for plain text words.
7.  Create animations that are appropriate for the content - use reasonable timing with `self.play(...)` and `self.wait(...)` calls.
8.  **Handle multiple sequences within the scene:** The JSON contains multiple sequences that should be animated in order within this single scene. Each sequence should be a distinct section of the animation with appropriate transitions.
9.  Do not include any code that writes to files or interacts with the network.
"""
TTS_VOICE_NAME = os.environ.get("TTS_VOICE_NAME", "Kore")
TTS_SPEAKING_SPEED = float(os.environ.get("TTS_SPEAKING_SPEED", "1.0"))
THINKING_BUDGET = int(os.environ.get("THINKING_BUDGET", "800"))

# Initialize the GenAI client with the API key
client = genai.Client(api_key=GENAI_API_KEY)

# Helpers

def write_bytes_to_wav(filename: str, pcm_bytes: bytes, channels=1, rate=24000, sample_width=2):
    import wave
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm_bytes)


def get_audio_duration(audio_path: Path) -> float:
    """
    Get the duration of an audio file in seconds.
    Returns 0.0 if file doesn't exist or can't be read.
    """
    if not audio_path or not audio_path.exists():
        return 0.0
    
    try:
        duration_cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(audio_path)
        ]
        result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Warning: Could not get audio duration from {audio_path}: {e}")
        return 0.0


def get_video_duration(video_path: Path) -> float:
    """
    Get the duration of a video file in seconds.
    Returns 0.0 if file doesn't exist or can't be read.
    """
    if not video_path or not video_path.exists():
        return 0.0
    
    try:
        duration_cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(video_path)
        ]
        result = subprocess.run(duration_cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, ValueError) as e:
        print(f"Warning: Could not get video duration from {video_path}: {e}")
        return 0.0


def call_script_llm(topic: str, max_retries=2):
    """
    Ask the thinking-capable model to output JSON describing scenes.
    We rely on the system prompt in env to instruct it to output only valid JSON.
    """
    user_prompt = f"""Create a JSON structure for an educational video about "{topic}".

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
- Scene duration will be automatically determined by audio and animation content"""
    
    for attempt in range(max_retries):
        try:
            # Try without thinking config first, as it might be causing issues
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=1500,
                ),
            )
            # Debug: print response structure
            print(f"Response type: {type(response)}")
            print(f"Response attributes: {dir(response)}")
            
            # Try different ways to extract text
            text = None
            if hasattr(response, 'text') and response.text:
                text = response.text
            elif hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                print(f"Candidate: {candidate}")
                if hasattr(candidate, 'content') and candidate.content:
                    print(f"Content: {candidate.content}")
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        print(f"Parts: {candidate.content.parts}")
                        if len(candidate.content.parts) > 0:
                            part = candidate.content.parts[0]
                            print(f"Part: {part}")
                            if hasattr(part, 'text'):
                                text = part.text
                    elif hasattr(candidate.content, 'text'):
                        text = candidate.content.text
            
            if not text:
                # Try accessing the text attribute of the response directly
                if hasattr(response, '_get_text'):
                    try:
                        text = response._get_text()
                    except:
                        pass
                
                if not text:
                    print(f"Full response debug: {response}")
                    raise ValueError(f"No text from script LLM. Response: {response}")
            
            print(f"Extracted text: {text[:700]}...")  # Debug print
            
            # Clean the text to extract JSON
            # Remove markdown code blocks if present
            if "```json" in text:
                # Extract content between ```json and ```
                start = text.find("```json") + 7
                end = text.find("```", start)
                if end != -1:
                    text = text[start:end].strip()
                else:
                    text = text[start:].strip()
            elif "```" in text:
                # Extract content between ``` blocks
                start = text.find("```") + 3
                end = text.find("```", start)
                if end != -1:
                    text = text[start:end].strip()
                else:
                    text = text[start:].strip()
            
            # Find JSON object boundaries
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON object found in response")
            
            json_text = text[json_start:json_end]
            print(f"Cleaned JSON text: {json_text[:300]}...")  # Debug print
            
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Problematic JSON: {json_text}")
                # Try to fix common JSON issues
                json_text = json_text.replace('\\', '\\\\')  # Escape backslashes
                json_text = json_text.replace('\n', '\\n')   # Escape newlines
                json_text = json_text.replace('\t', '\\t')   # Escape tabs
                data = json.loads(json_text)
            
            # Basic validation
            if "scenes" not in data or not isinstance(data["scenes"], list):
                raise ValueError("Script LLM did not return 'scenes' list.")
            return data
        except Exception as e:
            print(f"[script LLM] attempt {attempt+1} failed: {e}")
            time.sleep(1)
    raise RuntimeError("Script LLM failed after retries")


def generate_tts_for_text(text: str, out_path: str):
    """
    Use gemini-2.5-flash-preview-tts to generate a wav (as in user's snippet).
    """
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=TTS_VOICE_NAME
                        )
                    )
                ),
            ),
        )
        # navigation to inline bytes
        candidate = resp.candidates[0]
        part = candidate.content.parts[0]
        audio_data = part.inline_data.data  # bytes
        write_bytes_to_wav(out_path, audio_data)
        print(f"TTS audio generated successfully: {out_path}")
        return out_path
    except Exception as e:
        print(f"TTS generation error details: {e}")
        print(f"TTS generation failed for text: {text[:100]}...")
        return None


def call_manim_llm(scene_data: dict, max_retries=2):
    """
    Request Manim Python code for a single scene. We instruct the model (via SYSTEM_PROMPT_MANIM).
    The model is asked to return only Python code implementing a Scene subclass that handles all sequences in this scene.
    First tries with thinking, then falls back to without thinking on failure.
    """
    # Read the Manim reference documentation
    manim_ref_path = Path(__file__).parent / "manimRef.md"
    manim_ref_content = ""
    try:
        if manim_ref_path.exists():
            with open(manim_ref_path, 'r', encoding='utf-8') as f:
                manim_ref_content = f.read()
    except Exception as e:
        print(f"Warning: Could not read manimRef.md: {e}")
    
    # Prepare the scene data for the model
    payload = {
        "title": scene_data.get("title", "Educational Scene"),
        "scene": scene_data  # Single scene instead of multiple scenes
    }
    
    # Construct the system instruction with the Manim reference
    system_instruction = (
        f"{SYSTEM_PROMPT_MANIM}\n\n"
        f"--- MANIM COMMUNITY EDITION REFERENCE ---\n"
        f"{manim_ref_content}\n"
        f"--- END OF REFERENCE ---"
    )
    
    # Construct the user prompt (without system instruction)
    user_prompt = (
        f"Complete Video JSON: {json.dumps(payload, indent=2)}\n\n"
        "Create a single Manim scene that includes ALL sequences from the JSON in order. "
        "Each sequence should be a distinct section of the animation. "
        "Use appropriate timing and transitions between sequences. "
        "The scene class should be named 'CompleteVideoScene'.\n\n"
        "IMPORTANT: Output ONLY the Python code for the scene, no surrounding backticks, no commentary."
    )
    
    for attempt in range(max_retries):
        # First attempt: try with thinking
        use_thinking = (attempt == 0)
        
        try:
            print(f"Manim LLM attempt {attempt+1}/{max_retries} {'(with thinking)' if use_thinking else '(without thinking)'}")
            
            if use_thinking:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    thinking_config=types.ThinkingConfig(thinking_budget=THINKING_BUDGET // 2),
                    max_output_tokens=1800,
                )
            else:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    max_output_tokens=1800,
                )
            
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=config
            )
            
            # Try different ways to extract text
            text = None
            if hasattr(resp, 'text') and resp.text:
                text = resp.text
            elif hasattr(resp, 'candidates') and resp.candidates:
                candidate = resp.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        if len(candidate.content.parts) > 0:
                            part = candidate.content.parts[0]
                            if hasattr(part, 'text') and part.text:
                                text = part.text
                    elif hasattr(candidate.content, 'text'):
                        text = candidate.content.text
            
            if not text:
                raise ValueError(f"No text from Manim LLM. Response: {resp}")
            
            # Some models add Markdown fences — strip them if present
            if "```python" in text:
                text = text.split("```python")[1].split("```")[0].strip()
            elif text.strip().startswith("```"):
                # remove triple backtick fences
                parts = text.split("```")
                if len(parts) >= 2:
                    text = parts[1]
            
            print(f"✓ Manim LLM succeeded on attempt {attempt+1} {'(with thinking)' if use_thinking else '(without thinking)'}")
            return text, use_thinking  # Return both text and whether thinking was used
            
        except Exception as e:
            print(f"[manim LLM] attempt {attempt+1} failed {'(with thinking)' if use_thinking else '(without thinking)'}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    raise RuntimeError(f"Manim LLM failed after {max_retries} retries")


def generate_complete_narration(scene_data: dict) -> str:
    """
    Combine all narration text from all sequences in a single scene into a complete narration script.
    Each sequence's text becomes a paragraph.
    """
    narration_parts = []
    sequences = scene_data.get("sequences", [])
    
    for seq in sequences:
        text = seq.get("text", "").strip()
        if text:
            narration_parts.append(text)
    
    if not narration_parts:
        return ""
    
    # Join with double newlines to create paragraph breaks
    complete_narration = "\n\n".join(narration_parts)
    return complete_narration


def call_correction_llm(correction_prompt: str, max_retries=1):
    """
    Calls the LLM with a specific prompt to correct code.
    This is a simpler version of call_manim_llm without JSON wrapping.
    """
    # Read the Manim reference documentation for context
    manim_ref_path = Path(__file__).parent / "manimRef.md"
    manim_ref_content = ""
    try:
        if manim_ref_path.exists():
            with open(manim_ref_path, 'r', encoding='utf-8') as f:
                manim_ref_content = f.read()
    except Exception as e:
        print(f"Warning: Could not read manimRef.md: {e}")
    
    # System instruction for code correction
    system_instruction = (
        f"{SYSTEM_PROMPT_MANIM}\n\n"
        f"--- MANIM COMMUNITY EDITION REFERENCE ---\n"
        f"{manim_ref_content}\n"
        f"--- END OF REFERENCE ---\n\n"
        "You are correcting broken Manim code. Focus on fixing syntax errors, method calls, and ensuring the code follows Manim best practices."
    )
    
    for attempt in range(max_retries):
        try:
            print(f"Correction LLM attempt {attempt+1}/{max_retries}")
            # Use a simple config, no thinking needed for corrections
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=2000
            )
            
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=correction_prompt,
                config=config
            )
            
            # --- Text extraction logic ---
            text = None
            if hasattr(resp, 'text') and resp.text:
                text = resp.text
            elif hasattr(resp, 'candidates') and resp.candidates:
                candidate = resp.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        if len(candidate.content.parts) > 0:
                            part = candidate.content.parts[0]
                            if hasattr(part, 'text') and part.text:
                                text = part.text
                    elif hasattr(candidate.content, 'text'):
                        text = candidate.content.text
            
            if not text:
                raise ValueError(f"No text from correction LLM. Response: {resp}")

            # --- Cleaning logic ---
            if "```python" in text:
                text = text.split("```python")[1].split("```")[0].strip()
            elif text.strip().startswith("```"):
                parts = text.split("```")
                if len(parts) >= 2:
                    text = parts[1]
            
            print(f"✓ Correction LLM succeeded on attempt {attempt+1}")
            return text.strip()  # Return the cleaned code
            
        except Exception as e:
            print(f"[correction LLM] attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
    
    raise RuntimeError(f"Correction LLM failed after {max_retries} retries")


def save_and_render_manim(scene_code: str, scene_class_name: str, output_dir: Path, tmpdir: Path):
    """
    Save Python code to file and run manim to render the Scene class.
    Returns path to produced mp4.
    """
    script_path = tmpdir / f"scene_{scene_class_name}.py"
    script_path.write_text(scene_code, encoding="utf-8")
    
    # Test Python syntax first
    try:
        compile(scene_code, str(script_path), 'exec')
        print(f"✓ Code syntax is valid for {scene_class_name}")
    except SyntaxError as e:
        print(f"✗ Syntax error in generated code: {e}")
        raise

    # Run manim CLI. Use -ql (quick low quality) for speed in demo.
    # Use absolute paths to avoid path resolution issues
    script_abs = script_path.absolute()
    output_abs = output_dir.absolute()
    
    cmd = ["manim", str(script_abs), scene_class_name, "-ql", "--media_dir", str(output_abs)]
    print(f"Running manim: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)
        print(f"✓ Manim render successful for {scene_class_name}")
    except subprocess.CalledProcessError as e:
        print("Manim failed. Stderr:")
        print(e.stderr)
        print("Stdout:")
        print(e.stdout)
        raise
    except subprocess.TimeoutExpired:
        raise RuntimeError("Manim render timed out")

    # Find the produced mp4: manim writes into <media_dir>/videos/<script_name>/<resolution>/<Scene>.mp4
    # We'll search for any mp4 file in output_dir recursively that contains scene_class_name
    mp4_candidates = list(output_dir.rglob(f"*{scene_class_name}*.mp4"))
    if not mp4_candidates:
        # fallback: any mp4 in dir
        mp4_candidates = list(output_dir.rglob("*.mp4"))
    if not mp4_candidates:
        raise FileNotFoundError("No mp4 produced by Manim in output_dir")
    # Choose the newest file
    mp4_candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return mp4_candidates[0]


def mux_audio_video(video_path: Path, audio_path: Path, out_path: Path):
    """
    Use ffmpeg to mux audio and video. Extend video duration to match audio duration if needed.
    Adds 3 seconds of padding at the end of each scene.
    """
    if audio_path and audio_path.exists():
        # Get durations to determine approach
        audio_duration = get_audio_duration(audio_path)
        video_duration = get_video_duration(video_path)
        
        # Calculate target duration with 3 seconds padding
        base_duration = max(audio_duration, video_duration)
        target_duration = base_duration + 3.0
        
        print(f"Video duration: {video_duration:.2f}s, Audio duration: {audio_duration:.2f}s, Target (with 3s padding): {target_duration:.2f}s")
        
        # Always extend to target duration with padding
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",  # Loop video indefinitely
            "-i", str(video_path),
            "-i", str(audio_path),
            "-filter_complex", f"[1:a]apad=pad_dur=3[a]",  # Add 3 seconds of silence to audio
            "-map", "0:v", "-map", "[a]",  # Map video from first input, padded audio from filter
            "-c:v", "libx264",  # Re-encode video to allow looping
            "-c:a", "aac",
            "-t", str(target_duration),  # Set output duration to target with padding
            str(out_path),
        ]
    else:
        # No audio - extend video by 3 seconds
        video_duration = get_video_duration(video_path)
        target_duration = video_duration + 3.0
        
        print(f"Video duration: {video_duration:.2f}s, Target (with 3s padding): {target_duration:.2f}s")
        
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",  # Loop video indefinitely
            "-i", str(video_path),
            "-c:v", "libx264",  # Re-encode video to allow looping
            "-t", str(target_duration),  # Set output duration with padding
            str(out_path),
        ]
    
    print(f"Running ffmpeg mux: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    return out_path


def concat_videos(video_paths, out_final):
    """
    Concatenate mp4s using ffmpeg concat demuxer.
    """
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as f:
        for p in video_paths:
            f.write(f"file '{os.path.abspath(str(p))}'\n")
        listfile = f.name
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile, "-c", "copy", out_final]
    print(f"Running ffmpeg concat: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    os.unlink(listfile)
    return out_final


def simple_text_scene_template(scene_data: dict):
    """
    Fallback Manim scene generator (very small) if model produced nothing.
    """
    # Generate a unique scene name
    scene_num = scene_data.get("seq", 1)
    scene_name = f"Scene{scene_num}"
    
    # Extract text directly from the scene
    text = scene_data.get("text", "").strip()
    if not text:
        text = "No content available"
    
    # Create a simple scene that shows the text
    safe_text = text.replace('"""', '').replace('"', '\\"')[:100]  # Limit length and escape quotes
    code = f"""from manim import *
class {scene_name}(Scene):
    def construct(self):
        txt = Text(r\"\"\"{safe_text}\"\"\")
        txt.scale(0.7)
        self.play(Write(txt))
        self.wait(3)
        self.play(FadeOut(txt))"""
    
    code += "\n        self.wait(1)\n"
    
    return code, scene_name


def main(topic: str):
    # create workspace
    out_root = Path("renders")
    out_root.mkdir(exist_ok=True)
    workspace = tempfile.TemporaryDirectory(prefix="manim_mvp_")
    tmpdir = Path(workspace.name)
    print(f"Using tmpdir: {tmpdir}")

    # Summary tracking
    # NEW, CORRECTED BLOCK
    summary = {
        "topic": topic,
        "total_scenes": 0,
        "script_llm": {"success": True, "attempts": 0},
        "scenes": [],
        "tts_stats": {"success": 0, "failed": 0},
        "manim_stats": {
            "success": 0,
            "failed": 0,
            "fallback": 0,
            "thinking_success": 0,      # Corrected key
            "non_thinking_success": 0,  # Corrected key
        },
        "render_stats": {"success": 0, "failed": 0, "fallback": 0, "self_corrected": 0},
        "audio_mux_stats": {"success": 0, "failed": 0}, # Corrected keys
        "total_duration": 0
    }

    # 1) call script LLM to produce scenes JSON
    print("Calling Script LLM to generate scenes...")
    try:
        data = call_script_llm(topic)
        summary["script_llm"]["success"] = True
    except Exception as e:
        print(f"Script LLM failed: {e}")
        summary["script_llm"]["success"] = False
        summary["script_llm"]["error"] = str(e)
        return summary
    
    scenes = data.get("scenes", [])
    summary["total_scenes"] = len(scenes)
    if not scenes:
        print("No scenes generated. Exiting.")
        return summary

    print(f"Generated {len(scenes)} scenes for the video")

    # Prepare output folders
    video_out_dir = out_root / "video"
    video_out_dir.mkdir(parents=True, exist_ok=True)

    # Process each scene individually
    per_scene_outputs = []
    
    for i, scene in enumerate(scenes):
        seq = i + 1
        print(f"\n{'='*20} Processing Scene {seq} {'='*20}")
        
        scene_out_dir = video_out_dir / f"scene_{seq}"
        scene_out_dir.mkdir(exist_ok=True)
        
        scene_summary = {
            "scene_number": seq,
            "duration": 0.0,
            "tts": {"success": False, "error": None},
            "manim_llm": {"success": False, "thinking_used": False, "fallback": None, "error": None},
            "render": {"success": False, "fallback": None, "error": None, "output_file": None},
            "audio_mux": {"success": False, "error": None, "output_file": None}
        }
        
        # 1) Generate narration for this scene
        print(f"Generating narration for scene {seq}...")
        narration = generate_complete_narration(scene)
        scene_summary["has_narration"] = bool(narration)
        
        if narration:
            print(f"Scene {seq} narration: {narration[:100]}...")
        else:
            print(f"Warning: No narration generated for scene {seq}")
        
        print(f"---\nScene {seq}: has_narration={bool(narration)}")
        
        # 2) TTS for this scene (if text exists)
        audio_file = None
        if narration:
            audio_path = tmpdir / f"scene_{seq}_narration.wav"
            print(f"Generating TTS audio for scene {seq}...")
            try:
                audio_result = generate_tts_for_text(narration, str(audio_path))
                if audio_result and Path(audio_result).exists():
                    audio_file = audio_path
                    print(f"Scene {seq} TTS audio file created: {audio_file}")
                    scene_summary["tts"]["success"] = True
                    summary["tts_stats"]["success"] += 1
                else:
                    print(f"Scene {seq} TTS generation returned None or file doesn't exist")
                    scene_summary["tts"]["error"] = "TTS returned None or file doesn't exist"
                    summary["tts_stats"]["failed"] += 1
                    audio_file = None
            except Exception as e:
                print(f"Scene {seq} TTS generation failed: {e}")
                scene_summary["tts"]["error"] = str(e)
                summary["tts_stats"]["failed"] += 1
                audio_file = None
        else:
            print(f"No narration text for scene {seq}, skipping TTS")

        # 3) Manim generation for this scene
        print(f"Requesting Manim code for scene {seq}...")
        scene_class_name = f"Scene{seq}"
        manim_code = None
        
        try:
            manim_code, thinking_used = call_manim_llm(scene)
            
            if not manim_code:
                print(f"Scene {seq} Manim LLM returned empty code")
                scene_summary["manim_llm"]["error"] = "Empty code returned"
                summary["manim_stats"]["failed"] += 1
            else:
                scene_summary["manim_llm"]["success"] = True
                scene_summary["manim_llm"]["thinking_used"] = thinking_used
                summary["manim_stats"]["success"] += 1
                if thinking_used:
                    summary["manim_stats"]["thinking_success"] += 1
                else:
                    summary["manim_stats"]["non_thinking_success"] += 1
                
                # Ensure the class name exists
                if scene_class_name not in manim_code:
                    print(f"Scene {seq} model output didn't contain expected class name {scene_class_name}.")
                    print("Generated code:")
                    print("-" * 40)
                    print(manim_code[:1000])  # Show first 1000 chars
                    print("-" * 40)
                else:
                    print(f"✓ Scene {seq} generated valid Manim code for {scene_class_name} (thinking={thinking_used})")
                    print(f"Code length: {len(manim_code)} characters")
        except Exception as e:
            print(f"Scene {seq} Manim LLM failed: {e}. Using fallback simple text scene.")
            scene_summary["manim_llm"]["error"] = str(e)
            summary["manim_stats"]["failed"] += 1
            manim_code = None
        
        # Use fallback if generation failed or no code
        if not manim_code:
            manim_code, scene_class_name = simple_text_scene_template(scene)
            print(f"Scene {seq} using fallback scene: {scene_class_name}")
            scene_summary["manim_llm"]["fallback"] = "Used text fallback"
            summary["manim_stats"]["fallback"] += 1    

        # 4) Save and render manim for this scene
        try:
            rendered_mp4 = save_and_render_manim(manim_code, scene_class_name, scene_out_dir, tmpdir)
            print(f"Scene {seq} rendered video: {rendered_mp4}")
            scene_summary["render"]["success"] = True
            scene_summary["render"]["output_file"] = str(rendered_mp4)
            summary["render_stats"]["success"] += 1
        except Exception as e:
            print(f"Scene {seq} render failed: {e}")
            
            # --- START OF NEW SELF-CORRECTION CODE ---
            print(f"Attempting self-correction with LLM for scene {seq}...")
            
            error_message = str(e)
            # For subprocess errors, the stderr is more useful
            if isinstance(e, subprocess.CalledProcessError):
                error_message = e.stderr if e.stderr else str(e)

            correction_prompt = f"""The following Manim code failed to render.
            
--- ORIGINAL SCENE DESCRIPTION (JSON) ---
{json.dumps(scene)}

--- FAILED PYTHON CODE ---
{manim_code}

--- ERROR MESSAGE ---
{error_message}

--- YOUR TASK ---
Analyze the error message and the code, then provide a corrected, complete version of the Python script.
Focus on fixing the specific error mentioned. For example, if the error is "parenthesis was never closed", find the line and add the missing parenthesis.
Output ONLY the corrected Python code, with no explanation or markdown formatting.
"""
            try:
                # Use the correction LLM
                corrected_code = call_correction_llm(correction_prompt)
                print(f"✓ Scene {seq} self-correction LLM returned code. Retrying render...")
                rendered_mp4 = save_and_render_manim(corrected_code, scene_class_name, scene_out_dir, tmpdir)
                print(f"✓ Scene {seq} self-correction successful! Rendered video: {rendered_mp4}")
                scene_summary["render"]["success"] = True
                scene_summary["render"]["output_file"] = str(rendered_mp4)
                scene_summary["render"]["self_corrected"] = True
                summary["render_stats"]["success"] += 1
                summary["render_stats"]["self_corrected"] = summary["render_stats"].get("self_corrected", 0) + 1
            except Exception as correction_e:
                print(f"✗ Scene {seq} self-correction also failed: {correction_e}")
                # Now, proceed with the original fallback logic
                scene_summary["render"]["error"] = str(e)
                summary["render_stats"]["failed"] += 1
                
                # fallback to text-only scene if possible
                if narration:
                    try:
                        manim_code, scene_class_name = simple_text_scene_template(scene)
                        rendered_mp4 = save_and_render_manim(manim_code, scene_class_name, scene_out_dir, tmpdir)
                        print(f"Scene {seq} fallback render succeeded: {rendered_mp4}")
                        scene_summary["render"]["fallback"] = "Used text fallback after render failure"
                        scene_summary["render"]["output_file"] = str(rendered_mp4)
                        summary["render_stats"]["fallback"] += 1
                    except Exception as fallback_error:
                        print(f"Scene {seq} fallback render also failed: {fallback_error}")
                        scene_summary["render"]["fallback_error"] = str(fallback_error)
                        # Skip to next scene, will add scene_summary at end of loop
                        summary["scenes"].append(scene_summary)
                        continue
                else:
                    # Skip to next scene, will add scene_summary at end of loop
                    summary["scenes"].append(scene_summary)
                    continue
            # --- END OF NEW SELF-CORRECTION CODE ---

        # 5) mux audio & video and calculate final duration for this scene
        final_scene_mp4 = scene_out_dir / f"scene_{seq}_final.mp4"
        print(f"Audio file for scene {seq}: {audio_file}")
        print(f"Audio file exists: {audio_file and audio_file.exists() if audio_file else 'N/A'}")
        
        try:
            muxed = mux_audio_video(rendered_mp4, audio_file, final_scene_mp4)
            print(f"Scene {seq} final: {muxed}")
            scene_summary["audio_mux"]["success"] = True
            scene_summary["audio_mux"]["output_file"] = str(muxed)
            summary["audio_mux_stats"]["success"] += 1
            per_scene_outputs.append(muxed)
            
            # Calculate the actual scene duration as max of audio and video + 3 seconds padding
            audio_duration = get_audio_duration(audio_file) if audio_file else 0.0
            video_duration = get_video_duration(Path(rendered_mp4))
            base_duration = max(audio_duration, video_duration, 1.0)  # Minimum 1 second
            scene_duration = base_duration + 3.0  # Add 3 seconds padding
            scene_summary["duration"] = scene_duration
            summary["total_duration"] += scene_duration
            
            print(f"Scene {seq} duration: {scene_duration:.2f}s (base: {base_duration:.2f}s + 3s padding, audio: {audio_duration:.2f}s, video: {video_duration:.2f}s)")
            
        except Exception as e:
            print(f"Audio muxing failed for scene {seq}: {e}")
            scene_summary["audio_mux"]["error"] = str(e)
            summary["audio_mux_stats"]["failed"] += 1
            # Use video-only as fallback
            per_scene_outputs.append(rendered_mp4)
            
            # Calculate duration from video only + 3 seconds padding
            video_duration = get_video_duration(Path(rendered_mp4))
            base_duration = max(video_duration, 1.0)  # Minimum 1 second
            scene_duration = base_duration + 3.0  # Add 3 seconds padding
            scene_summary["duration"] = scene_duration
            summary["total_duration"] += scene_duration
            
            print(f"Scene {seq} duration: {scene_duration:.2f}s (base: {base_duration:.2f}s + 3s padding, video only)")
        
        # Add this scene's summary to the overall summary
        summary["scenes"].append(scene_summary)

    # 6) concatenate all scenes
    final_file = out_root / f"{topic.replace(' ','_')}_final.mp4"
    print("Concatenating scenes into final video...")
    
    # Filter out any None entries from failed renders
    valid_scene_outputs = [p for p in per_scene_outputs if p is not None]
    if valid_scene_outputs:
        concat_videos(valid_scene_outputs, str(final_file))
        print(f"Final video generated at: {final_file}")
    else:
        print("No scenes were successfully rendered. Final video not created.")
        final_file = None

    # Print comprehensive summary
    print("\n" + "="*60)
    print("GENERATION SUMMARY")
    print("="*60)
    
    print(f"Topic: {topic}")
    print(f"Total Duration: {summary['total_duration']:.2f} seconds")
    print(f"Script LLM: {'✓ Success' if summary['script_llm']['success'] else '✗ Failed'}")
    if not summary['script_llm']['success']:
        print(f"  Error: {summary['script_llm'].get('error', 'Unknown')}")
    
    print(f"\nScenes processed: {len(summary['scenes'])}")
    
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
        print(f"  Scene {i} (Duration: {scene['duration']:.2f}s):")
        print(f"    TTS: {'✓' if scene['tts']['success'] else '✗' + (' (' + scene['tts'].get('error', '') + ')' if scene['tts'].get('error') else '')}")
        manim_status = "✓" if scene['manim_llm']['success'] else "✗"
        if scene['manim_llm']['success']:
            manim_status += f" ({'thinking' if scene['manim_llm']['thinking_used'] else 'non-thinking'})"
        elif scene['manim_llm'].get('fallback'):
            manim_status += f" (fallback: {scene['manim_llm']['fallback']})"
        elif scene['manim_llm'].get('error'):
            manim_status += f" ({scene['manim_llm']['error']})"
        print(f"    Manim: {manim_status}")
        
        render_status = "✓" if scene['render']['success'] else "✗"
        if scene['render'].get('fallback'):
            render_status += f" (fallback used)"
        elif scene['render'].get('error'):
            render_status += f" ({scene['render']['error']})"
        print(f"    Render: {render_status}")
        
        mux_status = "✓" if scene['audio_mux']['success'] else "✗"
        if scene['audio_mux'].get('error'):
            mux_status += f" ({scene['audio_mux']['error']})"
        print(f"    Audio Mux: {mux_status}")
    
    print("="*60)
    if 'final_file' in locals() and final_file:
        print(f"Final output: {final_file}")
    else:
        print("Final output: No video created (all scenes failed)")

    # cleanup tmpdir if desired
    workspace.cleanup()
    
    # Return the summary of the entire pipeline run
    summary["output_file"] = str(final_file) if 'final_file' in locals() and final_file else None
    return summary


if __name__ == "__main__":
    if len(sys.argv) > 1:
        topic_arg = " ".join(sys.argv[1:])
    else:
        topic_arg = input("Enter topic to generate lecture for: ").strip()
    main(topic_arg)
