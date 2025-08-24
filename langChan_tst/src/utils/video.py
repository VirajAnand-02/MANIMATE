"""
Video processing utilities
"""

import subprocess
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


def get_audio_duration(audio_file: Path) -> float:
    """Get audio duration using ffprobe"""
    try:
        result = subprocess.run([
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(audio_file)
        ], capture_output=True, text=True, check=True)
        
        duration = float(result.stdout.strip())
        logger.debug(f"Audio duration for {audio_file}: {duration}s")
        return duration
        
    except (subprocess.CalledProcessError, ValueError) as e:
        logger.warning(f"Could not get audio duration for {audio_file}: {e}")
        return 5.0  # Default fallback


def combine_audio_video(video_path: Path, audio_path: Path, output_path: Path, 
                       extend_video: bool = True) -> bool:
    """Combine audio and video using ffmpeg"""
    try:
        audio_duration = get_audio_duration(audio_path)
        
        if extend_video:
            # Extend video to match audio duration by holding last frame
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-filter_complex", 
                f"[0:v]tpad=stop_mode=clone:stop_duration={audio_duration}[v]",
                "-map", "[v]",
                "-map", "1:a",
                "-shortest",
                str(output_path)
            ]
        else:
            # Simple combination without extending
            cmd = [
                "ffmpeg", "-y",
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-shortest",
                str(output_path)
            ]
        
        logger.info(f"Combining audio and video: {video_path.name} + {audio_path.name}")
        subprocess.run(cmd, check=True, capture_output=True)
        
        logger.info(f"✓ Audio-video combination successful: {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Audio-video combination failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in audio-video combination: {e}")
        return False


def concatenate_videos(video_paths: List[Path], output_path: Path, 
                      add_padding: bool = True, padding_duration: float = 3.0) -> bool:
    """Concatenate multiple videos using ffmpeg"""
    try:
        if not video_paths:
            logger.error("No video paths provided for concatenation")
            return False
        
        # Create temporary concat file
        concat_file = output_path.parent / "concat_list.txt"
        
        with open(concat_file, 'w') as f:
            for video_path in video_paths:
                if not video_path.exists():
                    logger.error(f"Video file not found: {video_path}")
                    return False
                f.write(f"file '{video_path.absolute()}'\n")
        
        if add_padding:
            # Add padding between videos
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-vf", f"tpad=stop_mode=clone:stop_duration={padding_duration}",
                "-c:a", "copy",
                str(output_path)
            ]
        else:
            # Simple concatenation
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c", "copy",
                str(output_path)
            ]
        
        logger.info(f"Concatenating {len(video_paths)} videos")
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Clean up
        concat_file.unlink()
        
        logger.info(f"✓ Video concatenation successful: {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Video concatenation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in video concatenation: {e}")
        return False
    finally:
        # Ensure cleanup
        if 'concat_file' in locals() and concat_file.exists():
            concat_file.unlink()


def convert_video_format(input_path: Path, output_path: Path, 
                        format: str = "mp4", quality: str = "high") -> bool:
    """Convert video to different format"""
    try:
        quality_settings = {
            "low": ["-crf", "28"],
            "medium": ["-crf", "23"],
            "high": ["-crf", "18"],
            "lossless": ["-crf", "0"]
        }
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-c:a", "aac"
        ]
        
        # Add quality settings
        cmd.extend(quality_settings.get(quality, quality_settings["high"]))
        
        # Add format-specific settings
        if format.lower() == "gif":
            cmd.extend([
                "-vf", "fps=10,scale=320:-1:flags=lanczos",
                "-c:v", "gif"
            ])
        
        cmd.append(str(output_path))
        
        logger.info(f"Converting video format: {input_path} -> {output_path}")
        subprocess.run(cmd, check=True, capture_output=True)
        
        logger.info(f"✓ Video conversion successful: {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Video conversion failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in video conversion: {e}")
        return False


def extract_audio_from_video(video_path: Path, audio_path: Path) -> bool:
    """Extract audio track from video"""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-vn",  # No video
            "-acodec", "copy",
            str(audio_path)
        ]
        
        logger.info(f"Extracting audio from video: {video_path}")
        subprocess.run(cmd, check=True, capture_output=True)
        
        logger.info(f"✓ Audio extraction successful: {audio_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Audio extraction failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in audio extraction: {e}")
        return False


def get_video_info(video_path: Path) -> Optional[dict]:
    """Get video information using ffprobe"""
    try:
        cmd = [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(video_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        import json
        info = json.loads(result.stdout)
        
        # Extract useful information
        video_info = {
            "duration": float(info["format"].get("duration", 0)),
            "size": int(info["format"].get("size", 0)),
            "format": info["format"].get("format_name", "unknown")
        }
        
        # Get video stream info
        for stream in info.get("streams", []):
            if stream.get("codec_type") == "video":
                video_info.update({
                    "width": stream.get("width", 0),
                    "height": stream.get("height", 0),
                    "fps": eval(stream.get("r_frame_rate", "0/1")),
                    "codec": stream.get("codec_name", "unknown")
                })
                break
        
        return video_info
        
    except (subprocess.CalledProcessError, json.JSONDecodeError, Exception) as e:
        logger.error(f"Could not get video info for {video_path}: {e}")
        return None


def create_video_thumbnail(video_path: Path, thumbnail_path: Path, 
                          timestamp: str = "00:00:01") -> bool:
    """Create thumbnail image from video"""
    try:
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-ss", timestamp,
            "-vframes", "1",
            "-q:v", "2",
            str(thumbnail_path)
        ]
        
        logger.info(f"Creating thumbnail for video: {video_path}")
        subprocess.run(cmd, check=True, capture_output=True)
        
        logger.info(f"✓ Thumbnail created: {thumbnail_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Thumbnail creation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in thumbnail creation: {e}")
        return False
