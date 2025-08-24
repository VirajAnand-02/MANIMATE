"""
Main video generation engine with parallel processing optimizations
"""

import subprocess
import time
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import sys
import concurrent.futures

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.models import (
    VideoScript, Scene, ProcessingSummary, RenderConfig, 
    TTSConfig, ManimConfig, ArchiveMetadata
)
# Avoid circular imports by importing providers lazily inside functions
# from src.providers.llm import create_llm_provider, BatchManimLLM
# from src.providers.tts import create_tts_provider

from src.utils.video import combine_audio_video, concatenate_videos, get_audio_duration
from src.utils.file_ops import (
    ensure_directory, create_timestamped_dir, save_json, 
    copy_file_safe, clean_filename
)
from src.utils.logging import setup_logging, ProcessLogger, StatsLogger
from src.utils.parallel import ParallelProcessor, ParallelConfig, TTSParallelProcessor, ManimParallelProcessor
import sys
from pathlib import Path
# Add project root to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import (
    PROJECT_ROOT, RENDERS_DIR, ARCHIVES_DIR, TMP_DIR, 
    DEFAULT_QUALITY, QUALITY_PRESETS, SCRIPT_MODEL, MANIM_MODEL, FINAL_PADDING
)
from src.providers.llm import get_max_output_tokens

import logging

logger = logging.getLogger(__name__)


class VideoGenerationEngine:
    """Main engine for video generation pipeline with parallel processing"""
    
    def __init__(self, 
                 tts_config: TTSConfig = None,
                 manim_config: ManimConfig = None,
                 render_config: RenderConfig = None,
                 enable_parallel: bool = True,
                 max_tts_workers: int = 4,
                 max_render_workers: int = 2):
        
        # Import providers inside __init__ to avoid circular imports
        from src.providers.llm import create_llm_provider, BatchManimLLM
        from src.providers.tts import create_tts_provider
        
        self.tts_config = tts_config or TTSConfig()
        self.manim_config = manim_config or ManimConfig()
        self.render_config = render_config or RenderConfig()
        
        # Parallel processing configuration
        self.enable_parallel = enable_parallel
        self.max_tts_workers = max_tts_workers
        self.max_render_workers = max_render_workers
        
        # Initialize providers
        self.llm_provider = create_llm_provider("gemini", model=SCRIPT_MODEL)
        self.tts_provider = create_tts_provider(
            self.tts_config.provider.value,
            **self.tts_config.get_provider_config()
        )
        
        # Setup batch processing if enabled
        self.batch_manim = None
        if self.manim_config.use_batch:
            try:
                self.batch_manim = BatchManimLLM(model=MANIM_MODEL)
            except ValueError as e:
                if "Google GenAI package not available" in str(e):
                    logger.warning("Google GenAI not available, disabling batch Manim processing")
                    self.batch_manim = None
                else:
                    raise
        
        # Initialize parallel processors
        if self.enable_parallel:
            self.tts_parallel = TTSParallelProcessor(self.tts_provider, max_workers=self.max_tts_workers)
            self.manim_parallel = ManimParallelProcessor(max_workers=self.max_render_workers)
        else:
            self.tts_parallel = None
            self.manim_parallel = None
        
        # Initialize loggers
        self.process_logger = ProcessLogger("video_generation")
        self.stats_logger = StatsLogger("video_generation")
        
        # Setup directories
        ensure_directory(RENDERS_DIR)
        ensure_directory(ARCHIVES_DIR)
        ensure_directory(TMP_DIR)
        
        logger.info(f"VideoGenerationEngine initialized with parallel processing: {self.enable_parallel}")
        if self.enable_parallel:
            logger.info(f"TTS workers: {self.max_tts_workers}, Render workers: {self.max_render_workers}")
    
    def generate_video(self, topic: str) -> Tuple[bool, ProcessingSummary]:
        """Generate complete video from topic"""
        self.process_logger.start_process(f"Video Generation: {topic}", 6)
        
        # Initialize summary
        summary = ProcessingSummary(topic=topic)
        self.stats_logger.record("topic", topic)
        
        try:
            # Step 1: Generate script
            self.process_logger.step("Generating script")
            script = self._generate_script(topic, summary)
            summary.total_scenes = len(script.scenes)
            
            # Step 2: Create archive directory
            self.process_logger.step("Setting up archive")
            archive_dir = self._setup_archive(topic)
            self._save_script(script, archive_dir)
            
            # Step 3: Process scenes
            self.process_logger.step("Processing scenes")
            scene_videos = self._process_scenes(script, archive_dir, summary)
            
            # Step 4: Generate final video
            self.process_logger.step("Creating final video")
            final_video = self._create_final_video(scene_videos, topic, archive_dir)
            
            # Step 5: Archive results
            self.process_logger.step("Archiving results")
            self._archive_results(archive_dir, final_video, summary)
            
            # Step 6: Cleanup
            self.process_logger.step("Cleanup")
            self._cleanup_temporary_files()
            
            # Report completion
            self.process_logger.complete(f"Video created: {final_video}")
            self.stats_logger.report("Generation Statistics")
            
            return True, summary
            
        except Exception as e:
            self.process_logger.error("Video generation failed", str(e))
            logger.error(f"Video generation failed: {e}")
            return False, summary
    
    def _generate_script(self, topic: str, summary: ProcessingSummary) -> VideoScript:
        """Generate video script"""
        try:
            script = self.llm_provider.generate_script(topic)
            summary.script_llm = {"success": True}
            self.stats_logger.record("script_scenes", len(script.scenes))
            return script
        except Exception as e:
            summary.script_llm = {"success": False, "error": str(e)}
            raise
    
    def _setup_archive(self, topic: str) -> Path:
        """Setup archive directory"""
        clean_topic = clean_filename(topic.replace(" ", "_"))
        archive_dir = create_timestamped_dir(ARCHIVES_DIR, clean_topic)
        
        # Create subdirectories
        for subdir in ["audio_files", "scene_codes", "final_videos", "llm_outputs", "layouts"]:
            ensure_directory(archive_dir / subdir)
        
        return archive_dir
    
    def _save_script(self, script: VideoScript, archive_dir: Path):
        """Save script to archive"""
        script_file = archive_dir / "llm_outputs" / "script_generation.json"
        save_json(script.dict(), script_file)
    
    def _process_scenes(self, script: VideoScript, archive_dir: Path, 
                       summary: ProcessingSummary) -> List[Path]:
        """Process all scenes in the script"""
        scene_videos = []
        
        # Setup batch processing
        tts_requests = []
        manim_requests = []
        
        # Prepare all requests
        for scene in script.scenes:
            scene_summary = {
                "seq": scene.seq,
                "layout": scene.layout.value
            }
            
            # Add to batches
            tts_requests.append({
                "scene": scene,
                "audio_file": TMP_DIR / f"scene_{scene.seq}_audio.wav"
            })
            
            if self.batch_manim:
                self.batch_manim.add_to_batch(
                    scene.dict(), 
                    scene.layout.value, 
                    f"scene_{scene.seq}"
                )
                manim_requests.append({
                    "scene": scene,
                    "request_id": f"scene_{scene.seq}"
                })
        
        # Process TTS batch
        audio_files = self._process_tts_batch(tts_requests, archive_dir, summary)
        
        # Process Manim batch
        scene_codes = self._process_manim_batch(manim_requests, archive_dir, summary)
        
        # Render scenes - Use parallel or sequential based on configuration
        if self.enable_parallel and self.manim_parallel and len(script.scenes) > 1:
            logger.info("Using parallel rendering for Manim scenes")
            scene_videos = self._render_scenes_parallel(script.scenes, scene_codes, audio_files, archive_dir, summary)
        else:
            logger.info("Using sequential rendering for Manim scenes")
            scene_videos = self._render_scenes_sequential(script.scenes, scene_codes, audio_files, archive_dir, summary)
        
        return scene_videos
    
    def _render_scenes_parallel(self, scenes: List[Scene], scene_codes: Dict[str, Tuple[str, str]], 
                               audio_files: Dict[int, Path], archive_dir: Path, 
                               summary: ProcessingSummary) -> List[Path]:
        """Render scenes in parallel"""
        logger.info(f"Rendering {len(scenes)} scenes in parallel with {self.max_render_workers} workers")
        
        scene_videos = []
        
        # Prepare render tasks
        render_tasks = []
        for scene in scenes:
            scene_code_data = scene_codes.get(f"scene_{scene.seq}")
            audio_file = audio_files.get(scene.seq)
            
            logger.info(f"Preparing render task for scene {scene.seq}")
            logger.info(f"Scene code available: {scene_code_data is not None}")
            logger.info(f"Audio file available: {audio_file is not None}")
            if audio_file:
                logger.info(f"Audio file path: {audio_file}")
                logger.info(f"Audio file exists: {audio_file.exists()}")
            
            if scene_code_data:
                scene_code, class_name = scene_code_data
                logger.info(f"Scene {scene.seq}: class_name = {class_name}")
                
                render_task = {
                    "task_id": f"render_scene_{scene.seq}",
                    "scene": scene,  # Pass the scene object
                    "scene_code": scene_code,
                    "class_name": class_name,
                    "audio_file": audio_file,
                    "quality": self.render_config.quality
                }
                render_tasks.append(render_task)
                logger.info(f"✓ Render task created for scene {scene.seq}")
            else:
                logger.error(f"No scene code available for scene {scene.seq}, skipping render task")
        
        logger.info(f"Created {len(render_tasks)} render tasks out of {len(scenes)} scenes")
        
        if render_tasks:
            # Use parallel Manim processor
            logger.info(f"Starting parallel rendering of {len(render_tasks)} tasks")
            try:
                results = self.manim_parallel.render_scenes_batch(render_tasks)
                logger.info(f"Parallel rendering completed with {len(results)} successful results")
            except Exception as e:
                logger.error(f"Parallel rendering batch failed: {type(e).__name__}: {e}")
                import traceback
                logger.error(f"Full traceback: {traceback.format_exc()}")
                results = {}
            
            # Process results and combine with audio
            for task in render_tasks:
                task_id = task["task_id"]
                scene = task["scene"]
                audio_file = task["audio_file"]
                
                logger.info(f"Processing results for {task_id}")
                
                if task_id in results:
                    scene_video = results[task_id]
                    logger.info(f"✓ Render successful for {task_id}: {scene_video}")
                    
                    # Combine with audio if available
                    if audio_file and audio_file.exists():
                        final_video = RENDERS_DIR / "video" / f"scene_{scene.seq}" / f"scene_{scene.seq}_final.mp4"
                        ensure_directory(final_video.parent)
                        
                        logger.info(f"Combining audio and video for scene {scene.seq}")
                        if combine_audio_video(scene_video, audio_file, final_video):
                            scene_videos.append(final_video)
                            summary.render_stats.success += 1
                            summary.audio_mux_stats.success += 1
                            logger.info(f"✓ Audio-video combination successful for scene {scene.seq}")
                        else:
                            scene_videos.append(scene_video)  # Use video without audio
                            summary.render_stats.success += 1
                            summary.audio_mux_stats.failed += 1
                            logger.warning(f"Audio-video combination failed for scene {scene.seq}, using video only")
                    else:
                        scene_videos.append(scene_video)
                        summary.render_stats.success += 1
                        if audio_file:
                            logger.warning(f"Audio file not found for scene {scene.seq}: {audio_file}")
                        else:
                            logger.info(f"No audio file for scene {scene.seq}")
                else:
                    logger.error(f"Parallel rendering failed for scene {scene.seq}")
                    logger.error(f"Task ID {task_id} not found in results")
                    logger.error(f"Available results: {list(results.keys())}")
                    summary.render_stats.failed += 1
        
        logger.info(f"Parallel scene rendering completed: {len(scene_videos)}/{len(scenes)} successful")
        return scene_videos
    
    def _render_scenes_sequential(self, scenes: List[Scene], scene_codes: Dict[str, Tuple[str, str]], 
                                 audio_files: Dict[int, Path], archive_dir: Path, 
                                 summary: ProcessingSummary) -> List[Path]:
        """Render scenes sequentially (fallback)"""
        logger.info(f"Rendering {len(scenes)} scenes sequentially")
        
        scene_videos = []
        
        for scene in scenes:
            try:
                scene_video = self._render_scene(
                    scene, 
                    scene_codes.get(f"scene_{scene.seq}"),
                    audio_files.get(scene.seq),
                    archive_dir,
                    summary
                )
                if scene_video:
                    scene_videos.append(scene_video)
                    summary.render_stats.success += 1
                else:
                    summary.render_stats.failed += 1
                    
            except Exception as e:
                logger.error(f"Failed to render scene {scene.seq}: {e}")
                summary.render_stats.failed += 1
        
        return scene_videos
    
    def _combine_scene_audio_video(self, video_path: Path, audio_path: Path, 
                                  archive_dir: Path, scene_seq: int) -> Optional[Path]:
        """Combine scene video with audio"""
        try:
            final_video = archive_dir / "final_videos" / f"scene_{scene_seq}_final.mp4"
            
            success = combine_audio_video(
                video_path=video_path,
                audio_path=audio_path,
                output_path=final_video,
                extend_video=True
            )
            
            if success:
                return final_video
            else:
                logger.warning(f"Failed to combine audio/video for scene {scene_seq}, using video only")
                return video_path
                
        except Exception as e:
            logger.error(f"Error combining audio/video for scene {scene_seq}: {e}")
            return video_path
    
    def _process_tts_batch(self, tts_requests: List[Dict], archive_dir: Path, 
                          summary: ProcessingSummary) -> Dict[int, Path]:
        """Process TTS requests with parallel optimization"""
        if self.enable_parallel and len(tts_requests) > 1:
            return self._process_tts_batch_parallel(tts_requests, archive_dir, summary)
        else:
            return self._process_tts_batch_sequential(tts_requests, archive_dir, summary)
    
    def _process_tts_batch_parallel(self, tts_requests: List[Dict], archive_dir: Path, 
                                   summary: ProcessingSummary) -> Dict[int, Path]:
        """Process TTS requests in parallel"""
        logger.info(f"Processing {len(tts_requests)} TTS requests in parallel with {self.max_tts_workers} workers")
        
        audio_files = {}
        
        # Check if the provider supports optimized batch processing
        if hasattr(self.tts_provider, 'synthesize_batch_optimized'):
            # Use provider's optimized batch method
            request_tuples = [(req["scene"].text, req["audio_file"]) for req in tts_requests]
            results = self.tts_provider.synthesize_batch_optimized(request_tuples, max_workers=self.max_tts_workers)
            
            # Process results
            for i, req in enumerate(tts_requests):
                scene = req["scene"]
                audio_file = req["audio_file"]
                request_id = f"dia_batch_{i}"
                
                if results.get(request_id, False):
                    summary.tts_stats.success += 1
                    audio_files[scene.seq] = audio_file
                    
                    # Archive audio
                    archive_audio = archive_dir / "audio_files" / f"scene_{scene.seq}_audio.wav"
                    copy_file_safe(audio_file, archive_audio)
                else:
                    summary.tts_stats.failed += 1
                    logger.warning(f"TTS failed for scene {scene.seq}")
        
        else:
            # Use general parallel processor
            audio_files = self.tts_parallel.synthesize_batch(tts_requests)
            
            # Update summary and archive files
            for req in tts_requests:
                scene = req["scene"]
                if scene.seq in audio_files:
                    summary.tts_stats.success += 1
                    # Archive audio
                    archive_audio = archive_dir / "audio_files" / f"scene_{scene.seq}_audio.wav"
                    copy_file_safe(audio_files[scene.seq], archive_audio)
                else:
                    summary.tts_stats.failed += 1
        
        logger.info(f"Parallel TTS processing completed: {len(audio_files)}/{len(tts_requests)} successful")
        return audio_files
    
    def _process_tts_batch_sequential(self, tts_requests: List[Dict], archive_dir: Path, 
                                     summary: ProcessingSummary) -> Dict[int, Path]:
        """Process TTS requests sequentially (fallback)"""
        logger.info(f"Processing {len(tts_requests)} TTS requests sequentially")
        
        audio_files = {}
        
        for req in tts_requests:
            scene = req["scene"]
            audio_file = req["audio_file"]
            
            try:
                success = self.tts_provider.synthesize(scene.text, audio_file)
                
                if success:
                    summary.tts_stats.success += 1
                    audio_files[scene.seq] = audio_file
                    
                    # Archive audio
                    archive_audio = archive_dir / "audio_files" / f"scene_{scene.seq}_audio.wav"
                    copy_file_safe(audio_file, archive_audio)
                else:
                    summary.tts_stats.failed += 1
                    
            except Exception as e:
                logger.error(f"TTS failed for scene {scene.seq}: {e}")
                summary.tts_stats.failed += 1
        
        return audio_files
    
    def _process_manim_batch(self, manim_requests: List[Dict], archive_dir: Path,
                           summary: ProcessingSummary) -> Dict[str, Tuple[str, str]]:
        """Process Manim code generation requests"""
        scene_codes = {}
        
        if self.batch_manim:
            # Process batch
            batch_results = self.batch_manim.process_batch()
            
            for req in manim_requests:
                scene = req["scene"]
                request_id = req["request_id"]
                
                if request_id in batch_results:
                    result = batch_results[request_id]
                    
                    if result.success:
                        code_content = result.content
                        full_code, class_name = self._create_full_scene_code(
                            scene, code_content
                        )
                        scene_codes[request_id] = (full_code, class_name)
                        summary.manim_stats.success += 1
                    else:
                        # Use fallback
                        fallback_code, class_name = self._generate_fallback_scene(scene)
                        scene_codes[request_id] = (fallback_code, class_name)
                        summary.manim_stats.fallback += 1
                else:
                    # Missing result, use fallback
                    fallback_code, class_name = self._generate_fallback_scene(scene)
                    scene_codes[request_id] = (fallback_code, class_name)
                    summary.manim_stats.failed += 1
        else:
            # Individual processing
            for req in manim_requests:
                scene = req["scene"]
                request_id = req["request_id"]
                
                try:
                    full_code, class_name = self.llm_provider.generate_manim_code(
                        scene.dict(), scene.layout.value
                    )
                    scene_codes[request_id] = (full_code, class_name)
                    summary.manim_stats.success += 1
                except Exception as e:
                    logger.error(f"Manim generation failed for scene {scene.seq}: {e}")
                    fallback_code, class_name = self._generate_fallback_scene(scene)
                    scene_codes[request_id] = (fallback_code, class_name)
                    summary.manim_stats.fallback += 1
        
        # Archive scene codes
        for request_id, (code, class_name) in scene_codes.items():
            code_file = archive_dir / "scene_codes" / f"{request_id}_code.py"
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(code)
        
        return scene_codes
    
    def _create_full_scene_code(self, scene: Scene, code_content: str) -> Tuple[str, str]:
        """Create full scene code from LLM content"""
        if scene.layout == "custom":
            return code_content, f"Scene{scene.seq}"
        
        # Clean up code content (remove markdown formatting)
        cleaned_content = code_content.strip()
        if cleaned_content.startswith("```python"):
            cleaned_content = cleaned_content[9:]  # Remove ```python
        if cleaned_content.endswith("```"):
            cleaned_content = cleaned_content[:-3]  # Remove closing ```
        cleaned_content = cleaned_content.strip()
        
        template_map = {
            "title_and_main_content": "TitleAndMainContent",
            "split_screen": "SplitScreen"
        }
        
        template_class = template_map.get(scene.layout.value, "TitleAndMainContent")
        
        full_code = f"""import sys
sys.path.append(r'{PROJECT_ROOT}')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import {template_class}
import numpy as np

class Scene{scene.seq}({template_class}):
    def construct_scene(self):
{self._indent_code(cleaned_content)}

# Set narration and duration
Scene{scene.seq}.narration_text = '''{scene.text.replace("'", "\\'")}'''
Scene{scene.seq}.audio_duration = 5.0
"""
        
        return full_code, f"Scene{scene.seq}"
    
    def _indent_code(self, code: str) -> str:
        """Indent code for class method"""
        lines = code.strip().split('\n')
        
        # Completely strip all leading whitespace and rebuild indentation
        # This handles mixed indentation scenarios better
        normalized_lines = []
        for line in lines:
            if line.strip():  # Non-empty line
                # Remove all leading whitespace
                normalized_lines.append(line.lstrip())
            else:  # Empty line
                normalized_lines.append('')
        
        # Now add proper method-level indentation (8 spaces)
        indented_lines = ['        ' + line if line.strip() else line for line in normalized_lines]
        return '\n'.join(indented_lines)
    
    def _generate_fallback_scene(self, scene: Scene) -> Tuple[str, str]:
        """Generate fallback scene code"""
        safe_text = scene.text.replace('"', '\\"').replace('"""', '')[:200]
        
        code = f"""import sys
sys.path.append(r'{PROJECT_ROOT}')
from src.templates.layouts import TitleAndMainContent

class Scene{scene.seq}(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene {scene.seq}", 
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

Scene{scene.seq}.narration_text = \"{safe_text}\"
Scene{scene.seq}.audio_duration = 5.0"""
        
        return code, f"Scene{scene.seq}"
    
    def _render_scene(self, scene: Scene, scene_code_data: Optional[Tuple[str, str]], 
                     audio_file: Optional[Path], archive_dir: Path,
                     summary: ProcessingSummary) -> Optional[Path]:
        """Render individual scene"""
        if not scene_code_data:
            return None
        
        scene_code, class_name = scene_code_data
        
        try:
            # Save and render Manim with scene data for corrections
            video_path = self._save_and_render_manim(
                scene_code, class_name, scene.seq, scene.dict(), summary
            )
            
            # Combine with audio if available
            if audio_file and audio_file.exists():
                final_video = RENDERS_DIR / "video" / f"scene_{scene.seq}" / f"scene_{scene.seq}_final.mp4"
                ensure_directory(final_video.parent)
                
                if combine_audio_video(video_path, audio_file, final_video):
                    summary.audio_mux_stats.success += 1
                    return final_video
                else:
                    summary.audio_mux_stats.failed += 1
                    return video_path
            else:
                return video_path
                
        except Exception as e:
            logger.error(f"Scene rendering failed for scene {scene.seq}: {e}")
            return None
    
    def _validate_scene_code(self, scene_code: str, class_name: str) -> Tuple[bool, str]:
        """Validate scene code for common issues before rendering"""
        issues = []
        
        # Check for markdown formatting
        if scene_code.strip().startswith('```'):
            issues.append("Code starts with markdown code blocks")
        if '```' in scene_code:
            issues.append("Code contains markdown formatting")
        
        # Check for nested function definitions
        lines = scene_code.split('\n')
        in_construct_scene = False
        for i, line in enumerate(lines):
            if 'def construct_scene(self):' in line:
                if in_construct_scene:
                    issues.append(f"Duplicate construct_scene method definition at line {i+1}")
                in_construct_scene = True
            elif in_construct_scene and line.strip().startswith('def '):
                issues.append(f"Nested function definition at line {i+1}: {line.strip()}")
        
        # Check for invalid color constants
        invalid_colors = ['BLUE_C', 'GREEN_C', 'ORANGE_C', 'RED_C', 'PURPLE_C', 'YELLOW_C']
        for color in invalid_colors:
            if color in scene_code:
                issues.append(f"Invalid color constant: {color} (use {color[:-2]} instead)")
        
        # Check for basic syntax issues
        try:
            compile(scene_code, f'{class_name}.py', 'exec')
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")
        except IndentationError as e:
            issues.append(f"Indentation error: {e}")
        
        if issues:
            return False, "; ".join(issues)
        return True, ""

    def _clean_scene_code(self, scene_code: str) -> str:
        """Clean common issues in scene code"""
        # Remove markdown formatting
        cleaned = scene_code.strip()
        if cleaned.startswith('```python'):
            cleaned = cleaned[9:]
        if cleaned.startswith('```'):
            cleaned = cleaned[3:]
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        
        # Fix invalid color constants
        color_fixes = {
            'BLUE_C': 'BLUE',
            'GREEN_C': 'GREEN', 
            'ORANGE_C': 'ORANGE',
            'RED_C': 'RED',
            'PURPLE_C': 'PURPLE',
            'YELLOW_C': 'YELLOW'
        }
        
        for invalid, valid in color_fixes.items():
            cleaned = cleaned.replace(invalid, valid)
        
        # Remove duplicate construct_scene definitions
        lines = cleaned.split('\n')
        result_lines = []
        found_construct_scene = False
        skip_nested_function = False
        nested_indent_level = 0
        
        for line in lines:
            if 'def construct_scene(self):' in line:
                if found_construct_scene:
                    # This is a duplicate - skip it and its body
                    skip_nested_function = True
                    nested_indent_level = len(line) - len(line.lstrip())
                    continue
                else:
                    found_construct_scene = True
                    result_lines.append(line)
            elif skip_nested_function:
                # Skip lines that are part of the nested function
                current_indent = len(line) - len(line.lstrip()) if line.strip() else 0
                if line.strip() and current_indent <= nested_indent_level:
                    # End of nested function
                    skip_nested_function = False
                    nested_indent_level = 0
                    result_lines.append(line)
                # Otherwise skip the line (it's part of the nested function)
            else:
                result_lines.append(line)
        
        return '\n'.join(result_lines)

    def _save_and_render_manim(self, scene_code: str, class_name: str, 
                              scene_num: int, scene_data: dict = None,
                              summary: ProcessingSummary = None,
                              max_correction_attempts: int = 2) -> Path:
        """Save and render Manim scene with error correction"""
        script_path = TMP_DIR / f"scene_{class_name}.py"
        
        # Clean the code first
        scene_code = self._clean_scene_code(scene_code)
        
        # Validate the code
        is_valid, validation_error = self._validate_scene_code(scene_code, class_name)
        if not is_valid:
            logger.warning(f"Code validation issues found: {validation_error}")
            logger.info("Attempting automatic fixes...")
        
        original_code = scene_code
        
        for attempt in range(max_correction_attempts + 1):
            current_code = scene_code if attempt == 0 else scene_code  # Will be updated in correction attempts
            script_path.write_text(current_code, encoding="utf-8")
            
            # Validate syntax
            try:
                compile(current_code, str(script_path), 'exec')
                logger.info(f"✓ Code syntax is valid for {class_name} (attempt {attempt + 1})")
            except SyntaxError as e:
                logger.error(f"✗ Syntax error in generated code (attempt {attempt + 1}): {e}")
                if attempt < max_correction_attempts:
                    # Try to correct the syntax error
                    logger.info(f"Attempting syntax error correction...")
                    try:
                        corrected_code = self._correct_manim_code(current_code, str(e), scene_data)
                        scene_code = corrected_code  # Update for next iteration
                        continue
                    except Exception as correction_e:
                        logger.error(f"Code correction failed: {correction_e}")
                raise
            
            # Setup output directory
            output_dir = RENDERS_DIR / "video" / f"scene_{scene_num}"
            ensure_directory(output_dir)
            
            # Build Manim command using RenderConfig's get_manim_args method
            manim_args = self.render_config.get_manim_args()
            cmd = [
                "manim", str(script_path.absolute()), class_name
            ] + manim_args + [
                "--media_dir", str(output_dir.absolute())
            ]
            
            logger.info(f"Running manim: {' '.join(cmd)}")
            
            try:
                result = subprocess.run(
                    cmd, 
                    check=True, 
                    capture_output=True, 
                    text=True, 
                    timeout=self.render_config.timeout
                )
                logger.info(f"✓ Manim render successful for {class_name} (attempt {attempt + 1})")
                
                # Find generated video
                mp4_candidates = sorted(
                    list(output_dir.rglob("*.mp4")), 
                    key=lambda p: p.stat().st_mtime, 
                    reverse=True
                )
                
                if not mp4_candidates:
                    raise FileNotFoundError("No mp4 produced by Manim")
                
                # Track if self-correction was used
                if attempt > 0:
                    logger.info(f"✓ Self-correction successful after {attempt} attempt(s)")
                    if summary:
                        summary.render_stats.self_corrected += 1
                        summary.render_stats.correction_attempts += attempt
                
                return mp4_candidates[0]
                
            except subprocess.CalledProcessError as e:
                logger.error(f"Manim failed (attempt {attempt + 1}). Stderr:\n{e.stderr}")
                if attempt < max_correction_attempts:
                    # Try to correct the runtime error
                    logger.info(f"Attempting runtime error correction...")
                    try:
                        corrected_code = self._correct_manim_code(current_code, e.stderr, scene_data)
                        scene_code = corrected_code  # Update for next iteration
                        continue
                    except Exception as correction_e:
                        logger.error(f"Code correction failed: {correction_e}")
                raise
        
        # If we get here, all attempts failed
        raise RuntimeError(f"Failed to render scene {scene_num} after {max_correction_attempts + 1} attempts")
    
    def _create_final_video(self, scene_videos: List[Path], topic: str, 
                           archive_dir: Path) -> Optional[Path]:
        """Create final concatenated video"""
        if not scene_videos:
            logger.error("No scene videos to concatenate")
            return None
        
        clean_topic = clean_filename(topic.replace(" ", "_"))
        final_output = RENDERS_DIR / f"{clean_topic}_final.mp4"
        
        success = concatenate_videos(scene_videos, final_output)
        
        if success:
            # Archive final video
            archive_video = archive_dir / "final_videos" / final_output.name
            copy_file_safe(final_output, archive_video)
            return final_output
        
        return None
    
    def _archive_results(self, archive_dir: Path, final_video: Optional[Path],
                        summary: ProcessingSummary):
        """Archive generation results"""
        # Save summary
        summary_file = archive_dir / "generation_summary.json"
        save_json(summary.dict(), summary_file)
        
        # Create metadata
        metadata = ArchiveMetadata(
            topic=summary.topic,
            timestamp=archive_dir.name.split('_')[-1],
            total_scenes=summary.total_scenes,
            generation_stats=summary,
            archive_path=str(archive_dir)
        )
        
        # List archived files
        metadata.audio_files = [f.name for f in (archive_dir / "audio_files").glob("*.wav")]
        metadata.scene_codes = [f.name for f in (archive_dir / "scene_codes").glob("*.py")]
        metadata.final_videos = [f.name for f in (archive_dir / "final_videos").glob("*.mp4")]
        metadata.llm_outputs = [f.name for f in (archive_dir / "llm_outputs").glob("*.json")]
        
        # Save metadata
        metadata_file = archive_dir / "archive_metadata.json"
        save_json(metadata.dict(), metadata_file)
    
    def _correct_manim_code(self, failed_code: str, error_message: str, scene_data: dict = None) -> str:
        """Use LLM to correct failed Manim code"""
        try:
            from google.genai import types
            
            system_instruction = """You are an expert Manim developer specializing in fixing broken Python code.

CRITICAL RULES:
1. Output ONLY the corrected Python code, no explanations or markdown
2. Fix syntax errors, runtime errors, and logic issues
3. Ensure proper indentation and parentheses/bracket balancing
4. Use proper imports with error handling:
   ```python
   import sys
   from pathlib import Path
   sys.path.append(str(Path(__file__).parent.parent))
   from manim import *
   try:
       from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
       LAYOUT_MANAGER_AVAILABLE = True
   except ImportError:
       LAYOUT_MANAGER_AVAILABLE = False
   ```
5. Make sure all method calls include parentheses (e.g., `.get_center()` not `.get_center`)
6. The code must define the complete class and method structure
7. Use conditional LayoutManager with fallback positioning when LAYOUT_MANAGER_AVAILABLE is False
8. Fix any Python version compatibility issues (use string type annotations)"""
            
            scene_info = ""
            if scene_data:
                scene_info = f"\nOriginal scene data:\n{scene_data}"
            
            correction_prompt = f"""The following Manim code failed with an error. Please provide the corrected code.

FAILED CODE:
{failed_code}

ERROR MESSAGE:
{error_message}{scene_info}

Provide the complete corrected Python code:"""
            
            logger.info("Requesting code correction from LLM...")
            
            response = self.llm_provider.client.models.generate_content(
                model=MANIM_MODEL,
                contents=correction_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,  # Low temperature for precise corrections
                    max_output_tokens=get_max_output_tokens(MANIM_MODEL)
                )
            )
            
            corrected_code = response.text.strip()
            
            # Clean up response (remove markdown if present)
            if corrected_code.startswith("```python"):
                corrected_code = corrected_code[9:]
            if corrected_code.endswith("```"):
                corrected_code = corrected_code[:-3]
            corrected_code = corrected_code.strip()
            
            logger.info("✓ Code correction received from LLM")
            return corrected_code
            
        except Exception as e:
            logger.error(f"LLM code correction failed: {e}")
            raise RuntimeError(f"Code correction failed: {e}")
    
    def _cleanup_temporary_files(self):
        """Clean up temporary files"""
        try:
            # Clean up old temporary files (keep last 3 days)
            from src.utils.file_ops import cleanup_old_files
            cleanup_old_files(TMP_DIR, max_age_days=3)
        except Exception as e:
            logger.warning(f"Cleanup failed: {e}")


def create_video_engine(**config) -> VideoGenerationEngine:
    """Factory function to create video generation engine"""
    return VideoGenerationEngine(**config)
