"""
Parallel processing utilities for video generation pipeline
"""

import asyncio
import concurrent.futures
import threading
import time
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional, Tuple, Union
from dataclasses import dataclass
import logging
from functools import wraps

logger = logging.getLogger(__name__)


@dataclass
class TaskResult:
    """Result of a parallel task"""
    task_id: str
    success: bool
    result: Any = None
    error: Optional[str] = None
    duration: float = 0.0


@dataclass
class ParallelConfig:
    """Configuration for parallel processing"""
    max_workers: int = 4
    timeout_per_task: float = 300.0  # 5 minutes
    chunk_size: int = 3
    use_threading: bool = True  # True for I/O bound, False for CPU bound


class ParallelProcessor:
    """Enhanced parallel processor with multiple execution strategies"""
    
    def __init__(self, config: ParallelConfig = None):
        self.config = config or ParallelConfig()
        self.stats = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_time": 0.0,
            "avg_task_time": 0.0
        }
    
    def process_tasks_threaded(self, tasks: List[Tuple[str, Callable, tuple, dict]]) -> Dict[str, TaskResult]:
        """Process tasks using ThreadPoolExecutor (I/O bound operations)"""
        results = {}
        start_time = time.time()
        
        logger.info(f"Starting threaded processing of {len(tasks)} tasks with {self.config.max_workers} workers")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            # Submit all tasks
            future_to_task = {}
            for task_id, func, args, kwargs in tasks:
                future = executor.submit(self._execute_task, task_id, func, args, kwargs)
                future_to_task[future] = task_id
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(
                future_to_task, 
                timeout=self.config.timeout_per_task * len(tasks)
            ):
                task_id = future_to_task[future]
                try:
                    result = future.result(timeout=self.config.timeout_per_task)
                    results[task_id] = result
                    if result.success:
                        self.stats["successful_tasks"] += 1
                    else:
                        self.stats["failed_tasks"] += 1
                except concurrent.futures.TimeoutError:
                    logger.error(f"Task {task_id} timed out")
                    results[task_id] = TaskResult(task_id, False, error="Timeout")
                    self.stats["failed_tasks"] += 1
                except Exception as e:
                    logger.error(f"Task {task_id} failed: {e}")
                    results[task_id] = TaskResult(task_id, False, error=str(e))
                    self.stats["failed_tasks"] += 1
        
        self.stats["total_tasks"] = len(tasks)
        self.stats["total_time"] = time.time() - start_time
        self.stats["avg_task_time"] = self.stats["total_time"] / len(tasks) if tasks else 0
        
        logger.info(f"Threaded processing completed: {self.stats['successful_tasks']}/{len(tasks)} successful")
        return results
    
    def process_tasks_multiprocess(self, tasks: List[Tuple[str, Callable, tuple, dict]]) -> Dict[str, TaskResult]:
        """Process tasks using ProcessPoolExecutor (CPU bound operations)"""
        results = {}
        start_time = time.time()
        
        logger.info(f"Starting multiprocess processing of {len(tasks)} tasks with {self.config.max_workers} workers")
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.config.max_workers) as executor:
            # Submit all tasks
            future_to_task = {}
            for task_id, func, args, kwargs in tasks:
                future = executor.submit(self._execute_task, task_id, func, args, kwargs)
                future_to_task[future] = task_id
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(
                future_to_task, 
                timeout=self.config.timeout_per_task * len(tasks)
            ):
                task_id = future_to_task[future]
                try:
                    result = future.result(timeout=self.config.timeout_per_task)
                    results[task_id] = result
                    if result.success:
                        self.stats["successful_tasks"] += 1
                    else:
                        self.stats["failed_tasks"] += 1
                except concurrent.futures.TimeoutError:
                    logger.error(f"Task {task_id} timed out")
                    results[task_id] = TaskResult(task_id, False, error="Timeout")
                    self.stats["failed_tasks"] += 1
                except Exception as e:
                    logger.error(f"Task {task_id} failed: {e}")
                    results[task_id] = TaskResult(task_id, False, error=str(e))
                    self.stats["failed_tasks"] += 1
        
        self.stats["total_tasks"] = len(tasks)
        self.stats["total_time"] = time.time() - start_time
        self.stats["avg_task_time"] = self.stats["total_time"] / len(tasks) if tasks else 0
        
        logger.info(f"Multiprocess processing completed: {self.stats['successful_tasks']}/{len(tasks)} successful")
        return results
    
    async def process_tasks_async(self, tasks: List[Tuple[str, Callable, tuple, dict]]) -> Dict[str, TaskResult]:
        """Process tasks using asyncio (async I/O operations)"""
        results = {}
        start_time = time.time()
        
        logger.info(f"Starting async processing of {len(tasks)} tasks")
        
        # Create semaphore to limit concurrent tasks
        semaphore = asyncio.Semaphore(self.config.max_workers)
        
        async def process_task(task_id: str, func: Callable, args: tuple, kwargs: dict):
            async with semaphore:
                return await self._execute_task_async(task_id, func, args, kwargs)
        
        # Create coroutines for all tasks
        coroutines = [
            process_task(task_id, func, args, kwargs)
            for task_id, func, args, kwargs in tasks
        ]
        
        # Wait for all tasks to complete
        try:
            task_results = await asyncio.wait_for(
                asyncio.gather(*coroutines, return_exceptions=True),
                timeout=self.config.timeout_per_task * len(tasks)
            )
            
            for i, result in enumerate(task_results):
                task_id = tasks[i][0]
                if isinstance(result, Exception):
                    logger.error(f"Task {task_id} failed: {result}")
                    results[task_id] = TaskResult(task_id, False, error=str(result))
                    self.stats["failed_tasks"] += 1
                else:
                    results[task_id] = result
                    if result.success:
                        self.stats["successful_tasks"] += 1
                    else:
                        self.stats["failed_tasks"] += 1
                        
        except asyncio.TimeoutError:
            logger.error("Async processing timed out")
            for task_id, _, _, _ in tasks:
                if task_id not in results:
                    results[task_id] = TaskResult(task_id, False, error="Timeout")
                    self.stats["failed_tasks"] += 1
        
        self.stats["total_tasks"] = len(tasks)
        self.stats["total_time"] = time.time() - start_time
        self.stats["avg_task_time"] = self.stats["total_time"] / len(tasks) if tasks else 0
        
        logger.info(f"Async processing completed: {self.stats['successful_tasks']}/{len(tasks)} successful")
        return results
    
    def process_tasks_chunked(self, tasks: List[Tuple[str, Callable, tuple, dict]]) -> Dict[str, TaskResult]:
        """Process tasks in chunks to manage memory and resources"""
        results = {}
        
        logger.info(f"Processing {len(tasks)} tasks in chunks of {self.config.chunk_size}")
        
        # Split tasks into chunks
        chunks = [tasks[i:i + self.config.chunk_size] for i in range(0, len(tasks), self.config.chunk_size)]
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i + 1}/{len(chunks)} with {len(chunk)} tasks")
            
            if self.config.use_threading:
                chunk_results = self.process_tasks_threaded(chunk)
            else:
                chunk_results = self.process_tasks_multiprocess(chunk)
            
            results.update(chunk_results)
            
            # Brief pause between chunks to allow system resources to recover
            if i < len(chunks) - 1:
                time.sleep(0.5)
        
        return results
    
    def _execute_task(self, task_id: str, func: Callable, args: tuple, kwargs: dict) -> TaskResult:
        """Execute a single task with timing and error handling"""
        start_time = time.time()
        
        try:
            logger.debug(f"Executing task {task_id}")
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.debug(f"Task {task_id} completed in {duration:.2f}s")
            return TaskResult(task_id, True, result, duration=duration)
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Task {task_id} failed after {duration:.2f}s: {e}")
            return TaskResult(task_id, False, error=str(e), duration=duration)
    
    async def _execute_task_async(self, task_id: str, func: Callable, args: tuple, kwargs: dict) -> TaskResult:
        """Execute a single async task with timing and error handling"""
        start_time = time.time()
        
        try:
            logger.debug(f"Executing async task {task_id}")
            
            # If function is not async, run it in thread pool
            if not asyncio.iscoroutinefunction(func):
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(None, lambda: func(*args, **kwargs))
            else:
                result = await func(*args, **kwargs)
            
            duration = time.time() - start_time
            logger.debug(f"Async task {task_id} completed in {duration:.2f}s")
            return TaskResult(task_id, True, result, duration=duration)
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Async task {task_id} failed after {duration:.2f}s: {e}")
            return TaskResult(task_id, False, error=str(e), duration=duration)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return self.stats.copy()


class TTSParallelProcessor:
    """Specialized parallel processor for TTS operations"""
    
    def __init__(self, tts_provider, max_workers: int = 3):
        self.tts_provider = tts_provider
        self.processor = ParallelProcessor(ParallelConfig(
            max_workers=max_workers,
            timeout_per_task=180.0,  # 3 minutes per TTS
            use_threading=True  # TTS is I/O bound
        ))
    
    def synthesize_batch(self, tts_requests: List[Dict]) -> Dict[int, Path]:
        """Synthesize multiple TTS requests in parallel"""
        logger.info(f"Starting parallel TTS synthesis for {len(tts_requests)} requests")
        
        # Prepare tasks
        tasks = []
        for req in tts_requests:
            scene = req["scene"]
            audio_file = req["audio_file"]
            
            tasks.append((
                f"tts_scene_{scene.seq}",
                self.tts_provider.synthesize,
                (scene.text, audio_file),
                {}
            ))
        
        # Process tasks
        results = self.processor.process_tasks_threaded(tasks)
        
        # Convert results to expected format
        audio_files = {}
        for req in tts_requests:
            scene = req["scene"]
            task_id = f"tts_scene_{scene.seq}"
            
            if task_id in results and results[task_id].success:
                audio_files[scene.seq] = req["audio_file"]
        
        logger.info(f"TTS parallel synthesis completed: {len(audio_files)}/{len(tts_requests)} successful")
        return audio_files


class ManimParallelProcessor:
    """Specialized parallel processor for Manim rendering operations"""
    
    def __init__(self, max_workers: int = 2):
        self.processor = ParallelProcessor(ParallelConfig(
            max_workers=max_workers,
            timeout_per_task=600.0,  # 10 minutes per render
            use_threading=False  # Manim rendering is CPU bound
        ))
    
    def render_scenes_batch(self, render_tasks: List[Dict]) -> Dict[str, Path]:
        """Render multiple Manim scenes in parallel"""
        logger.info(f"Starting parallel Manim rendering for {len(render_tasks)} scenes")
        
        # Log task details
        for task in render_tasks:
            task_id = task["task_id"]
            scene = task["scene"]
            class_name = task["class_name"]
            quality = task.get("quality", "unknown")
            logger.info(f"Task {task_id}: class={class_name}, seq={scene.seq}, quality={quality}")
        
        # Prepare tasks
        tasks = []
        for task in render_tasks:
            tasks.append((
                task["task_id"],
                self._render_single_scene,
                (task,),
                {}
            ))
        
        # Process tasks
        logger.info(f"Submitting {len(tasks)} tasks to process pool")
        results = self.processor.process_tasks_multiprocess(tasks)
        
        # Convert results to expected format
        scene_videos = {}
        successful_tasks = []
        failed_tasks = []
        
        for task in render_tasks:
            task_id = task["task_id"]
            
            if task_id in results and results[task_id].success:
                scene_videos[task_id] = results[task_id].result
                successful_tasks.append(task_id)
                logger.info(f"✓ Task {task_id} completed successfully")
            else:
                failed_tasks.append(task_id)
                if task_id in results:
                    error_msg = results[task_id].error
                    logger.error(f"✗ Task {task_id} failed: {error_msg}")
                else:
                    logger.error(f"✗ Task {task_id} missing from results")
        
        logger.info(f"Manim parallel rendering completed: {len(scene_videos)}/{len(render_tasks)} successful")
        logger.info(f"Successful tasks: {successful_tasks}")
        logger.info(f"Failed tasks: {failed_tasks}")
        return scene_videos
    
    def _render_single_scene(self, task: Dict) -> Path:
        """Render a single Manim scene"""
        import subprocess
        from pathlib import Path
        from src.core.models import QualityPreset, RenderConfig
        from src.utils.file_ops import ensure_directory
        
        task_id = task["task_id"]
        scene_code = task["scene_code"]
        class_name = task["class_name"]
        scene_obj = task["scene"]
        quality = task.get("quality", QualityPreset.HIGH)
        
        logger.info(f"Starting render for {task_id}")
        logger.info(f"Class name: {class_name}")
        logger.info(f"Scene sequence: {scene_obj.seq}")
        logger.info(f"Quality: {quality}")
        
        # Create proper output directory structure (similar to sequential renderer)
        from config.settings import RENDERS_DIR, TMP_DIR
        output_dir = RENDERS_DIR / "video" / f"scene_{scene_obj.seq}"
        ensure_directory(output_dir)
        logger.info(f"Output directory: {output_dir}")
        
        # Convert quality to proper format using RenderConfig
        if isinstance(quality, str):
            quality = QualityPreset(quality)
        
        render_config = RenderConfig(quality=quality)
        manim_args = render_config.get_manim_args()
        logger.info(f"Manim args: {manim_args}")
        
        # Create scene script file in tmp directory
        script_path = TMP_DIR / f"scene_{class_name}.py"
        logger.info(f"Script path: {script_path}")
        
        try:
            # Clean and validate the scene code before writing
            scene_code = self._clean_scene_code(scene_code)
            script_path.write_text(scene_code, encoding="utf-8")
            logger.info(f"✓ Scene script written successfully")
            logger.debug(f"Script content preview: {scene_code[:200]}...")
        except Exception as e:
            logger.error(f"Failed to write scene script: {e}")
            raise
    
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
        
        try:
            # Build Manim command (similar to the sequential renderer)
            cmd = [
                "manim", str(script_path.absolute()), class_name
            ] + manim_args + [
                "--media_dir", str(output_dir.absolute())
            ]
            
            logger.info(f"Running parallel manim: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes
            )
            
            logger.info(f"Manim process completed for {class_name}")
            logger.info(f"Return code: {result.returncode}")
            if result.stdout:
                logger.debug(f"Stdout: {result.stdout}")
            if result.stderr:
                logger.debug(f"Stderr: {result.stderr}")
            
            if result.returncode == 0:
                # Find generated video (similar to sequential renderer)
                mp4_candidates = sorted(
                    list(output_dir.rglob("*.mp4")), 
                    key=lambda p: p.stat().st_mtime, 
                    reverse=True
                )
                
                if mp4_candidates:
                    logger.info(f"✓ Parallel Manim render successful for {class_name}")
                    logger.info(f"Generated video: {mp4_candidates[0]}")
                    return mp4_candidates[0]
                else:
                    logger.error(f"No mp4 files found in output directory: {output_dir}")
                    logger.error(f"Directory contents: {list(output_dir.rglob('*'))}")
                    raise RuntimeError("No mp4 produced by Manim")
            else:
                logger.error(f"Manim process failed for {class_name}")
                logger.error(f"Return code: {result.returncode}")
                logger.error(f"Command: {' '.join(cmd)}")
                logger.error(f"Stdout: {result.stdout}")
                logger.error(f"Stderr: {result.stderr}")
                raise RuntimeError(f"Manim failed: {result.stderr}")
                
        except subprocess.TimeoutExpired as e:
            logger.error(f"Parallel Manim rendering timed out for {class_name} after {600}s")
            logger.error(f"Command: {' '.join(cmd)}")
            logger.error(f"Working directory: {output_dir}")
            raise RuntimeError(f"Manim timeout after 10 minutes: {e}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Parallel Manim rendering failed for {class_name}")
            logger.error(f"Command: {' '.join(cmd)}")
            logger.error(f"Return code: {e.returncode}")
            logger.error(f"Stdout: {e.stdout}")
            logger.error(f"Stderr: {e.stderr}")
            logger.error(f"Working directory: {output_dir}")
            raise RuntimeError(f"Manim subprocess failed: {e.stderr}")
        except FileNotFoundError as e:
            logger.error(f"Manim executable not found for {class_name}")
            logger.error(f"Command attempted: {' '.join(cmd)}")
            logger.error(f"Make sure 'manim' is installed and in PATH")
            raise RuntimeError(f"Manim executable not found: {e}")
        except Exception as e:
            logger.error(f"Parallel Manim rendering failed for {class_name}: {type(e).__name__}: {e}")
            logger.error(f"Command: {' '.join(cmd)}")
            logger.error(f"Script path: {script_path}")
            logger.error(f"Output directory: {output_dir}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise


def parallel_decorator(processor_config: ParallelConfig = None):
    """Decorator to make any function run in parallel for multiple inputs"""
    
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(inputs: List[Any], *args, **kwargs):
            processor = ParallelProcessor(processor_config or ParallelConfig())
            
            # Prepare tasks
            tasks = []
            for i, input_data in enumerate(inputs):
                task_id = f"task_{i}"
                tasks.append((task_id, func, (input_data, *args), kwargs))
            
            # Process tasks
            if processor_config and not processor_config.use_threading:
                results = processor.process_tasks_multiprocess(tasks)
            else:
                results = processor.process_tasks_threaded(tasks)
            
            # Return results in order
            return [results[f"task_{i}"].result if f"task_{i}" in results and results[f"task_{i}"].success else None 
                    for i in range(len(inputs))]
        
        return wrapper
    return decorator


# Utility functions for common parallel operations
def parallel_file_operations(operations: List[Tuple[str, Callable, tuple, dict]], max_workers: int = 4) -> Dict[str, bool]:
    """Execute file operations in parallel"""
    processor = ParallelProcessor(ParallelConfig(max_workers=max_workers, use_threading=True))
    results = processor.process_tasks_threaded(operations)
    return {task_id: result.success for task_id, result in results.items()}


def parallel_network_requests(requests: List[Tuple[str, Callable, tuple, dict]], max_workers: int = 8) -> Dict[str, Any]:
    """Execute network requests in parallel"""
    processor = ParallelProcessor(ParallelConfig(max_workers=max_workers, use_threading=True))
    results = processor.process_tasks_threaded(requests)
    return {task_id: result.result for task_id, result in results.items() if result.success}
