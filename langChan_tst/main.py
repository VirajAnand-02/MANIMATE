"""
Unified CLI and API interface for the video generation system
"""

import sys
import os
import argparse
import asyncio
import json
import uuid
import time
import copy
from pathlib import Path
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Try to import FastAPI dependencies (optional for API mode)
try:
    from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    # Create dummy classes to avoid syntax errors
    class BaseModel:
        pass
    class Field:
        pass

# Load environment variables first
load_dotenv()

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.engine import create_video_engine
from src.core.models import (
    TTSConfig, ManimConfig, RenderConfig, TTSProvider, QualityPreset,
    VideoScript, Scene, ProcessingSummary
)
from src.utils.logging import setup_logging
from config.settings import validate_config, setup_directories, TTS_VOICE_NAME, TTS_PROVIDER

import logging

logger = logging.getLogger(__name__)

# Global storage for API (only used if FastAPI is available)
scripts_storage: Dict[str, Any] = {}
generation_jobs: Dict[str, Dict[str, Any]] = {}


# ============================================================================
# API MODELS
# ============================================================================

class APIScene(BaseModel):
    seq: int
    text: str
    anim: str
    layout: Optional[str] = "title_and_main_content"

class APIVideoScript(BaseModel):
    title: str
    scenes: List[APIScene]

class GenerateVideoRequest(BaseModel):
    topic: str
    quality: Optional[str] = "high"
    tts_provider: Optional[str] = TTS_PROVIDER
    voice: Optional[str] = TTS_VOICE_NAME
    enable_parallel: Optional[bool] = True
    max_tts_workers: Optional[int] = 4
    max_render_workers: Optional[int] = 2
    use_thinking: Optional[bool] = True
    use_batch: Optional[bool] = True

class GetScriptRequest(BaseModel):
    token: str

class SetScriptRequest(BaseModel):
    token: str
    script: Dict[str, Any]

class StartGenerationRequest(BaseModel):
    token: str
    config: Optional[GenerateVideoRequest] = None

class JobStatus(BaseModel):
    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: float = 0.0
    message: str = ""
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: float
    updated_at: float

# ============================================================================
# API HELPER FUNCTIONS
# ============================================================================

def merge_scripts(existing: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge script updates into existing script without removing missing keys.
    Special handling for scenes list with seq-based merging.
    """
    if existing is None:
        existing = {}

    result = copy.deepcopy(existing)

    for k, v in updates.items():
        if k == "scenes":
            if not isinstance(v, list):
                raise ValueError("'scenes' must be a list when provided.")
            existing_scenes = {s['seq']: copy.deepcopy(s) for s in result.get('scenes', []) if 'seq' in s}
            for incoming in v:
                if 'seq' not in incoming:
                    raise ValueError("Each scene in updates must include a 'seq' integer.")
                seq = incoming['seq']
                if seq in existing_scenes:
                    existing_scenes[seq].update(incoming)
                else:
                    existing_scenes[seq] = copy.deepcopy(incoming)
            result['scenes'] = [existing_scenes[s] for s in sorted(existing_scenes.keys())]
        else:
            result[k] = copy.deepcopy(v)

    return result

def create_job(job_id: str, status: str = "pending", message: str = "") -> JobStatus:
    """Create a new job status entry"""
    current_time = time.time()
    job = JobStatus(
        job_id=job_id,
        status=status,
        progress=0.0,
        message=message,
        created_at=current_time,
        updated_at=current_time
    )
    generation_jobs[job_id] = job.dict()
    return job

def update_job(job_id: str, **updates) -> Optional[JobStatus]:
    """Update job status"""
    if job_id not in generation_jobs:
        return None
    
    generation_jobs[job_id].update(updates)
    generation_jobs[job_id]["updated_at"] = time.time()
    return JobStatus(**generation_jobs[job_id])

async def background_video_generation(job_id: str, script_data: Dict[str, Any], config: GenerateVideoRequest):
    """Background task for video generation"""
    try:
        update_job(job_id, status="running", message="Starting video generation", progress=10)
        
        # Create configurations
        tts_config = TTSConfig(
            provider=TTSProvider(config.tts_provider),
            voice=config.voice
        )
        
        manim_config = ManimConfig(
            use_thinking=config.use_thinking,
            use_batch=config.use_batch
        )
        
        render_config = RenderConfig(
            quality=QualityPreset(config.quality)
        )
        
        update_job(job_id, message="Creating video engine", progress=20)
        
        # Create engine
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=manim_config,
            render_config=render_config,
            enable_parallel=config.enable_parallel,
            max_tts_workers=config.max_tts_workers,
            max_render_workers=config.max_render_workers
        )
        
        update_job(job_id, message="Generating video", progress=30)
        
        # Convert script data to VideoScript object
        video_script = VideoScript(**script_data)
        
        # Generate video (this will take time)
        success, summary = engine.generate_video(video_script.title)
        
        if success:
            result = {
                "success": True,
                "summary": summary.dict(),
                "total_scenes": summary.total_scenes,
                "success_rates": {
                    "tts": f"{summary.tts_stats.success}/{summary.total_scenes}",
                    "code_generation": f"{summary.manim_stats.success}/{summary.total_scenes}",
                    "rendering": f"{summary.render_stats.success}/{summary.total_scenes}"
                }
            }
            update_job(job_id, 
                      status="completed", 
                      message="Video generation completed successfully", 
                      progress=100,
                      result=result)
        else:
            update_job(job_id, 
                      status="failed", 
                      message="Video generation failed", 
                      progress=100,
                      error="Generation process failed")
            
    except Exception as e:
        logger.error(f"Background generation failed for job {job_id}: {e}")
        update_job(job_id, 
                  status="failed", 
                  message=f"Generation failed: {str(e)}", 
                  progress=100,
                  error=str(e))

# ============================================================================
# FASTAPI APPLICATION (Only available if FastAPI is installed)
# ============================================================================

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="AI Video Generator API",
        description="AI-Powered Educational Video Generation API",
        version="2.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info(f"API request: {request.method} {request.url}")
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(f"API response: {response.status_code} in {process_time:.3f}s")
        return response

    # ============================================================================
    # API ENDPOINTS
    # ============================================================================

    @app.get("/")
    async def root():
        """API health check and information"""
        return {
            "name": "AI Video Generator API",
            "version": "2.0.0",
            "status": "running",
            "endpoints": {
                "generate_scripts": "POST /api/generate_scripts",
                "get_script": "GET /api/script/{token}",
                "update_script": "POST /api/script/{token}",
                "start_generation": "POST /api/generate/{token}",
                "job_status": "GET /api/job/{job_id}",
                "list_jobs": "GET /api/jobs"
            }
        }

    @app.post("/api/generate_scripts")
    async def generate_scripts(request: GenerateVideoRequest):
        """Generate multiple script variations for a topic"""
        logger.info(f"Generating scripts for topic: {request.topic}")
        
        try:
            from src.providers.llm import create_llm_provider
            
            # Create LLM provider for script generation
            llm_provider = create_llm_provider("gemini")
            
            tokens = []
            for i in range(3):  # Generate 3 variations
                logger.info(f"Generating script variation #{i+1}")
                
                try:
                    script = llm_provider.generate_script(request.topic)
                    token = uuid.uuid4().hex[:8]
                    scripts_storage[token] = script.dict()
                    tokens.append(token)
                    logger.info(f"Script #{i+1} stored with token: {token}")
                    
                except Exception as e:
                    logger.error(f"Failed to generate script #{i+1}: {e}")
                    continue
            
            if not tokens:
                raise HTTPException(status_code=500, detail="Failed to generate any scripts")
            
            return {
                "topic": request.topic,
                "tokens": tokens,
                "count": len(tokens)
            }
            
        except Exception as e:
            logger.error(f"Script generation failed: {e}")
            raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")

    @app.get("/api/script/{token}")
    async def get_script(token: str):
        """Get script by token"""
        logger.info(f"Retrieving script for token: {token}")
        
        if token not in scripts_storage:
            raise HTTPException(status_code=404, detail="Script token not found")
        
        return scripts_storage[token]

    @app.post("/api/script/{token}")
    async def update_script(token: str, script_updates: Dict[str, Any]):
        """Update script with partial or complete changes"""
        logger.info(f"Updating script for token: {token}")
        
        try:
            if token in scripts_storage:
                merged = merge_scripts(scripts_storage[token], script_updates)
            else:
                merged = copy.deepcopy(script_updates)
            
            # Validate merged script
            validated = APIVideoScript(**merged)
            scripts_storage[token] = merged
            
            logger.info(f"Script updated successfully for token: {token}")
            return {
                "token": token,
                "script": merged,
                "message": "Script updated successfully"
            }
            
        except Exception as e:
            logger.error(f"Script update failed for token {token}: {e}")
            raise HTTPException(status_code=400, detail=f"Script update failed: {str(e)}")

    @app.post("/api/generate/{token}")
    async def start_generation(token: str, config: Optional[GenerateVideoRequest] = None, background_tasks: BackgroundTasks = None):
        """Start video generation for a script"""
        logger.info(f"Starting generation for token: {token}")
        
        if token not in scripts_storage:
            raise HTTPException(status_code=404, detail="Script token not found")
        
        # Use default config if none provided
        if config is None:
            config = GenerateVideoRequest(topic="Generated Video")
        
        # Create job
        job_id = uuid.uuid4().hex[:12]
        job = create_job(job_id, status="pending", message="Generation queued")
        
        # Start background generation
        background_tasks.add_task(
            background_video_generation,
            job_id,
            scripts_storage[token],
            config
        )
        
        return {
            "job_id": job_id,
            "status": "pending",
            "message": "Video generation started",
            "token": token
        }

    @app.get("/api/job/{job_id}")
    async def get_job_status(job_id: str):
        """Get job status and progress"""
        if job_id not in generation_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return generation_jobs[job_id]

    @app.get("/api/jobs")
    async def list_jobs(limit: int = 50):
        """List recent jobs"""
        jobs = list(generation_jobs.values())
        jobs.sort(key=lambda x: x["created_at"], reverse=True)
        return {
            "jobs": jobs[:limit],
            "total": len(generation_jobs)
        }

    @app.delete("/api/job/{job_id}")
    async def delete_job(job_id: str):
        """Delete a job record"""
        if job_id not in generation_jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        
        del generation_jobs[job_id]
        return {"message": "Job deleted successfully"}

    @app.post("/api/validate_config")
    async def validate_system_config():
        """Validate system configuration"""
        try:
            errors = validate_config()
            if errors:
                return {
                    "valid": False,
                    "errors": errors
                }
            
            setup_directories()
            return {
                "valid": True,
                "message": "Configuration is valid"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "errors": [str(e)]
            }

else:
    # Dummy app object if FastAPI is not available
    app = None

# ============================================================================
# CLI FUNCTIONS (Original functionality preserved)
# ============================================================================

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AI-Powered Educational Video Generator - CLI and API modes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # CLI Mode (default)
  %(prog)s "matrix multiplication"
  %(prog)s "machine learning basics" --quality high --tts-provider dia
  %(prog)s "quantum computing" --custom-layout --no-batch
  %(prog)s "calculus introduction" --output-dir ./my_videos
  
  # API Mode
  %(prog)s api                    # Start API server on localhost:8000
        """
    )
    
    # Add API mode as a special positional argument
    parser.add_argument(
        "topic_or_mode",
        nargs='?',
        help="Topic for the educational video OR 'api' to start API server"
    )
    
    # Keep the original topic argument for backwards compatibility
    parser.add_argument(
        "--topic",
        help="Topic for the educational video (alternative to positional argument)"
    )
    
    # TTS Configuration
    tts_group = parser.add_argument_group("Text-to-Speech Options")
    tts_group.add_argument(
        "--tts-provider", 
        choices=["gemini", "gemini_batch", "openai", "dia", "mock"],
        default=TTS_PROVIDER,  # Use environment default
        help=f"TTS provider to use (default: {TTS_PROVIDER})"
    )
    tts_group.add_argument(
        "--voice", 
        default=TTS_VOICE_NAME,  # Use environment default
        help=f"Voice to use for TTS (default: {TTS_VOICE_NAME})"
    )
    tts_group.add_argument(
        "--tts-model",
        help="TTS model to use (provider-specific)"
    )
    
    # Parallel Processing Configuration
    parallel_group = parser.add_argument_group("Parallel Processing Options")
    parallel_group.add_argument(
        "--enable-parallel",
        action="store_true",
        default=True,
        help="Enable parallel processing for faster generation (default: True)"
    )
    parallel_group.add_argument(
        "--disable-parallel",
        action="store_true",
        help="Disable parallel processing"
    )
    parallel_group.add_argument(
        "--force-parallel-manim",
        action="store_true",
        help="Force parallel Manim rendering (experimental)"
    )
    parallel_group.add_argument(
        "--max-tts-workers",
        type=int,
        default=4,
        help="Maximum number of TTS workers for parallel processing (default: 4)"
    )
    parallel_group.add_argument(
        "--max-render-workers",
        type=int,
        default=2,
        help="Maximum number of render workers for parallel processing (default: 2)"
    )
    
    # Video Quality Configuration
    video_group = parser.add_argument_group("Video Quality Options")
    video_group.add_argument(
        "--quality",
        choices=["low", "medium", "high", "2k", "4k"],
        default="high",
        help="Video quality preset (default: high)"
    )
    video_group.add_argument(
        "--format",
        choices=["mp4", "gif"],
        default="mp4",
        help="Output format (default: mp4)"
    )
    
    # Generation Options
    gen_group = parser.add_argument_group("Generation Options")
    gen_group.add_argument(
        "--no-batch",
        action="store_true",
        help="Disable batch processing for Manim generation"
    )
    gen_group.add_argument(
        "--no-thinking",
        action="store_true",
        help="Disable thinking mode for LLM generation"
    )
    gen_group.add_argument(
        "--thinking-budget",
        type=int,
        default=6000,
        help="Token budget for thinking mode (default: 6000)"
    )
    gen_group.add_argument(
        "--custom-layout",
        action="store_true",
        help="Use custom layout generation instead of templates"
    )
    
    # Output Options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--output-dir",
        type=Path,
        help="Custom output directory for renders"
    )
    output_group.add_argument(
        "--archive-only",
        action="store_true",
        help="Only create archive, don't save to renders directory"
    )
    
    # Logging Options
    log_group = parser.add_argument_group("Logging Options")
    log_group.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    log_group.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console output (log to file only)"
    )
    log_group.add_argument(
        "--log-file",
        type=Path,
        help="Custom log file path"
    )
    
    # System Options
    sys_group = parser.add_argument_group("System Options")
    sys_group.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate configuration and exit"
    )
    sys_group.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up old temporary files and exit"
    )
    sys_group.add_argument(
        "--version",
        action="store_true",
        help="Show version information and exit"
    )
    
    return parser.parse_args()


def create_configs_from_args(args: argparse.Namespace) -> tuple:
    """Create configuration objects from command line arguments"""
    
    # TTS Configuration
    tts_config = TTSConfig(
        provider=TTSProvider(args.tts_provider),
        voice=args.voice,
        model=args.tts_model
    )
    
    # Manim Configuration
    manim_config = ManimConfig(
        use_thinking=not args.no_thinking,
        thinking_budget=args.thinking_budget,
        use_batch=not args.no_batch
    )
    
    # Render Configuration
    render_config = RenderConfig(
        quality=QualityPreset(args.quality),
        output_format=args.format
    )
    
    return tts_config, manim_config, render_config


def validate_environment() -> bool:
    """Validate environment and configuration"""
    try:
        errors = validate_config()
        if errors:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        setup_directories()
        logger.info("✓ Environment validation successful")
        return True
        
    except Exception as e:
        logger.error(f"Environment validation failed: {e}")
        return False


def cleanup_system():
    """Clean up old temporary files"""
    try:
        from src.utils.file_ops import cleanup_old_files
        from config.settings import TMP_DIR, LOGS_DIR
        
        logger.info("Cleaning up old files...")
        
        # Clean temporary files older than 7 days
        tmp_cleaned = cleanup_old_files(TMP_DIR, max_age_days=7)
        logger.info(f"Cleaned {tmp_cleaned} temporary files")
        
        # Clean log files older than 30 days
        log_cleaned = cleanup_old_files(LOGS_DIR, max_age_days=30, pattern="*.log")
        logger.info(f"Cleaned {log_cleaned} log files")
        
        logger.info("✓ Cleanup completed")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")


def show_version():
    """Show version information"""
    print("AI Video Generator v2.0")
    print("Restructured and modular implementation")
    print("Features: LLM Script Generation, Batch Processing, Template System")
    print("")
    print("Components:")
    print("  - Google Gemini & OpenAI LLM Integration")
    print("  - Multi-provider TTS (Gemini, OpenAI)")
    print("  - Manim Animation Framework")
    print("  - Template-based Layout System")
    print("  - Comprehensive Archiving")


def main():
    """Main entry point - supports both CLI and API modes"""
    # Parse arguments first
    args = parse_arguments()
    
    # Check if we should run in API mode
    if args.topic_or_mode == "api":
        run_api_server()
        return 0
    
    # Determine the topic for CLI mode
    topic = args.topic_or_mode or args.topic
    if not topic:
        print("Error: Topic is required for CLI mode. Use --help for usage information.")
        return 1
    
    # Set the topic in args for the CLI function
    args.topic = topic
    
    # Otherwise run CLI mode
    return run_cli(args)

def run_api_server():
    """Run the FastAPI server"""
    if not FASTAPI_AVAILABLE:
        print("Error: FastAPI is not installed. Please install with:")
        print("pip install fastapi uvicorn pydantic")
        sys.exit(1)
    
    import uvicorn
    
    # Setup basic logging for API mode
    setup_logging("INFO", include_console=True)
    
    # Validate environment
    if not validate_environment():
        logger.error("Environment validation failed. Please check your configuration.")
        sys.exit(1)
    
    logger.info("Starting AI Video Generator API server...")
    logger.info("API documentation available at: http://localhost:8001/docs")
    logger.info("API endpoints:")
    logger.info("  - POST /api/generate_scripts - Generate script variations")
    logger.info("  - GET /api/script/{token} - Get script by token")
    logger.info("  - POST /api/script/{token} - Update script")
    logger.info("  - POST /api/generate/{token} - Start video generation")
    logger.info("  - GET /api/job/{job_id} - Check generation status")
    logger.info("  - GET /api/jobs - List all jobs")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=int(os.getenv("PYTHON_API_PORT", "8001")),
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("API server stopped by user")
    except Exception as e:
        logger.error(f"API server failed: {e}")
        sys.exit(1)

def run_cli(args):
    """Run the original CLI interface"""
    # Handle special commands
    if args.version:
        show_version()
        return 0
    
    if args.cleanup:
        setup_logging(args.log_level, include_console=not args.quiet)
        cleanup_system()
        return 0
    
    if args.validate_only:
        setup_logging(args.log_level, include_console=not args.quiet)
        success = validate_environment()
        return 0 if success else 1
    
    # Setup logging
    log_file = args.log_file
    if not log_file and not args.quiet:
        from config.settings import LOGS_DIR
        from src.utils.file_ops import ensure_directory
        ensure_directory(LOGS_DIR)
        log_file = LOGS_DIR / "video_generation.log"
    
    setup_logging(args.log_level, log_file, include_console=not args.quiet)
    
    # Validate environment
    if not validate_environment():
        logger.error("Environment validation failed. Please check your configuration.")
        return 1
    
    # Create configurations
    try:
        tts_config, manim_config, render_config = create_configs_from_args(args)
    except ValueError as e:
        logger.error(f"Invalid configuration: {e}")
        return 1
    
    # Create and run video engine
    try:
        logger.info(f"Starting video generation for topic: {args.topic}")
        
        # Determine parallel processing settings
        enable_parallel = args.enable_parallel and not args.disable_parallel
        
        logger.info(f"Parallel processing: {'enabled' if enable_parallel else 'disabled'}")
        if enable_parallel:
            logger.info(f"TTS workers: {args.max_tts_workers}, Render workers: {args.max_render_workers}")
        
        engine = create_video_engine(
            tts_config=tts_config,
            manim_config=manim_config,
            render_config=render_config,
            enable_parallel=enable_parallel,
            max_tts_workers=args.max_tts_workers,
            max_render_workers=args.max_render_workers
        )
        
        success, summary = engine.generate_video(args.topic)
        
        if success:
            logger.info("🎉 Video generation completed successfully!")
            logger.info(f"📊 Generated {summary.total_scenes} scenes")
            logger.info(f"📈 Success rate: TTS {summary.tts_stats.success}/{summary.total_scenes}, "
                       f"Code Gen {summary.manim_stats.success}/{summary.total_scenes}, "
                       f"Rendering {summary.render_stats.success}/{summary.total_scenes}")
            
            # Log performance stats if available
            if hasattr(engine, 'tts_parallel') and hasattr(engine.tts_parallel, 'processor'):
                stats = engine.tts_parallel.processor.get_stats()
                if stats['total_tasks'] > 0:
                    logger.info(f"⚡ TTS Performance: {stats['avg_task_time']:.2f}s avg per task")
            
            return 0
        else:
            logger.error("❌ Video generation failed")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Video generation interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
