# Enhanced Logging for Parallel Manim Rendering

## Overview
Added comprehensive logging to diagnose rendering failures in the parallel Manim processing system.

## Enhanced Logging Features

### 1. Task Preparation Logging (engine.py)
```python
# For each scene preparation:
logger.info(f"Preparing render task for scene {scene.seq}")
logger.info(f"Scene code available: {scene_code_data is not None}")
logger.info(f"Audio file available: {audio_file is not None}")
logger.info(f"Audio file path: {audio_file}")
logger.info(f"Audio file exists: {audio_file.exists()}")
logger.info(f"Scene {scene.seq}: class_name = {class_name}")
```

### 2. Batch Processing Logging (parallel.py)
```python
# Before starting parallel processing:
for task in render_tasks:
    task_id = task["task_id"]
    scene = task["scene"]
    class_name = task["class_name"]
    quality = task.get("quality", "unknown")
    logger.info(f"Task {task_id}: class={class_name}, seq={scene.seq}, quality={quality}")

logger.info(f"Submitting {len(tasks)} tasks to process pool")
```

### 3. Individual Scene Rendering Logging
```python
# Detailed task execution logging:
logger.info(f"Starting render for {task_id}")
logger.info(f"Class name: {class_name}")
logger.info(f"Scene sequence: {scene_obj.seq}")
logger.info(f"Quality: {quality}")
logger.info(f"Output directory: {output_dir}")
logger.info(f"Manim args: {manim_args}")
logger.info(f"Script path: {script_path}")
logger.info(f"✓ Scene script written successfully")
```

### 4. Subprocess Execution Logging
```python
# Before and after subprocess execution:
logger.info(f"Running parallel manim: {' '.join(cmd)}")
logger.info(f"Manim process completed for {class_name}")
logger.info(f"Return code: {result.returncode}")
if result.stdout:
    logger.debug(f"Stdout: {result.stdout}")
if result.stderr:
    logger.debug(f"Stderr: {result.stderr}")
```

### 5. Enhanced Error Logging
```python
# Specific error types with detailed information:

# Timeout errors:
except subprocess.TimeoutExpired as e:
    logger.error(f"Parallel Manim rendering timed out for {class_name} after {600}s")
    logger.error(f"Command: {' '.join(cmd)}")
    logger.error(f"Working directory: {output_dir}")

# Process errors:
except subprocess.CalledProcessError as e:
    logger.error(f"Parallel Manim rendering failed for {class_name}")
    logger.error(f"Command: {' '.join(cmd)}")
    logger.error(f"Return code: {e.returncode}")
    logger.error(f"Stdout: {e.stdout}")
    logger.error(f"Stderr: {e.stderr}")
    logger.error(f"Working directory: {output_dir}")

# File not found errors:
except FileNotFoundError as e:
    logger.error(f"Manim executable not found for {class_name}")
    logger.error(f"Command attempted: {' '.join(cmd)}")
    logger.error(f"Make sure 'manim' is installed and in PATH")

# General errors:
except Exception as e:
    logger.error(f"Parallel Manim rendering failed for {class_name}: {type(e).__name__}: {e}")
    logger.error(f"Command: {' '.join(cmd)}")
    logger.error(f"Script path: {script_path}")
    logger.error(f"Output directory: {output_dir}")
    logger.error(f"Full traceback: {traceback.format_exc()}")
```

### 6. File Output Validation Logging
```python
# When checking for generated videos:
if mp4_candidates:
    logger.info(f"✓ Parallel Manim render successful for {class_name}")
    logger.info(f"Generated video: {mp4_candidates[0]}")
else:
    logger.error(f"No mp4 files found in output directory: {output_dir}")
    logger.error(f"Directory contents: {list(output_dir.rglob('*'))}")
```

### 7. Results Processing Logging
```python
# When processing batch results:
logger.info(f"Processing results for {task_id}")
logger.info(f"✓ Render successful for {task_id}: {scene_video}")
logger.info(f"Combining audio and video for scene {scene.seq}")
logger.info(f"✓ Audio-video combination successful for scene {scene.seq}")

# For failures:
logger.error(f"Parallel rendering failed for scene {scene.seq}")
logger.error(f"Task ID {task_id} not found in results")
logger.error(f"Available results: {list(results.keys())}")
```

### 8. Summary Logging
```python
# Final batch processing summary:
logger.info(f"Manim parallel rendering completed: {len(scene_videos)}/{len(render_tasks)} successful")
logger.info(f"Successful tasks: {successful_tasks}")
logger.info(f"Failed tasks: {failed_tasks}")
```

## Benefits of Enhanced Logging

### ✅ **Failure Point Identification**
- Pinpoints exactly where in the pipeline failures occur
- Distinguishes between different types of errors (timeout, subprocess, file not found, etc.)
- Shows command-line arguments passed to Manim subprocess

### ✅ **Resource Tracking**
- Logs file paths, directory structures, and file existence
- Shows script content preview for debugging generated code
- Tracks output directory contents when videos aren't found

### ✅ **Process Flow Visibility**
- Shows task preparation, submission, and completion status
- Tracks individual scene processing through the pipeline
- Provides clear success/failure indicators for each step

### ✅ **Debugging Information**
- Full subprocess command lines for manual reproduction
- Return codes, stdout, and stderr from failed processes
- Complete tracebacks for unexpected errors
- Working directory and environment context

## Usage

The enhanced logging will automatically provide detailed information when:
- Any scene fails to render
- Subprocess execution encounters errors
- File operations fail
- Audio-video combination fails
- Task preparation encounters issues

This comprehensive logging makes it much easier to diagnose and fix parallel rendering issues without needing to modify code for debugging.
