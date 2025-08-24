"""
File and directory utilities
"""

import json
import shutil
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, create if necessary"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_filename(filename: str) -> str:
    """Clean filename for safe file system usage"""
    # Replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename


def create_timestamped_dir(base_path: Path, prefix: str = "") -> Path:
    """Create directory with timestamp"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    if prefix:
        dir_name = f"{clean_filename(prefix)}_{timestamp}"
    else:
        dir_name = timestamp
    
    directory = base_path / dir_name
    return ensure_directory(directory)


def copy_file_safe(source: Path, destination: Path) -> bool:
    """Copy file with error handling"""
    try:
        ensure_directory(destination.parent)
        shutil.copy2(source, destination)
        logger.debug(f"Copied file: {source} -> {destination}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy file {source} to {destination}: {e}")
        return False


def move_file_safe(source: Path, destination: Path) -> bool:
    """Move file with error handling"""
    try:
        ensure_directory(destination.parent)
        shutil.move(str(source), str(destination))
        logger.debug(f"Moved file: {source} -> {destination}")
        return True
    except Exception as e:
        logger.error(f"Failed to move file {source} to {destination}: {e}")
        return False


def delete_file_safe(file_path: Path) -> bool:
    """Delete file with error handling"""
    try:
        if file_path.exists():
            file_path.unlink()
            logger.debug(f"Deleted file: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete file {file_path}: {e}")
        return False


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes"""
    try:
        return file_path.stat().st_size
    except Exception:
        return 0


def get_directory_size(directory: Path) -> int:
    """Get total size of directory in bytes"""
    total_size = 0
    try:
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                total_size += get_file_size(file_path)
    except Exception as e:
        logger.error(f"Error calculating directory size for {directory}: {e}")
    
    return total_size


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"


def save_json(data: Dict[str, Any], file_path: Path, indent: int = 2) -> bool:
    """Save data as JSON file"""
    try:
        ensure_directory(file_path.parent)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        logger.debug(f"Saved JSON: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON to {file_path}: {e}")
        return False


def load_json(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load data from JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Loaded JSON: {file_path}")
        return data
    except Exception as e:
        logger.error(f"Failed to load JSON from {file_path}: {e}")
        return None


def save_text(text: str, file_path: Path, encoding: str = 'utf-8') -> bool:
    """Save text to file"""
    try:
        ensure_directory(file_path.parent)
        file_path.write_text(text, encoding=encoding)
        logger.debug(f"Saved text file: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save text to {file_path}: {e}")
        return False


def load_text(file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
    """Load text from file"""
    try:
        text = file_path.read_text(encoding=encoding)
        logger.debug(f"Loaded text file: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Failed to load text from {file_path}: {e}")
        return None


def find_files(directory: Path, pattern: str = "*", recursive: bool = True) -> List[Path]:
    """Find files matching pattern"""
    try:
        if recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))
    except Exception as e:
        logger.error(f"Error finding files in {directory} with pattern {pattern}: {e}")
        return []


def cleanup_old_files(directory: Path, max_age_days: int = 7, pattern: str = "*") -> int:
    """Clean up old files in directory"""
    if not directory.exists():
        return 0
    
    import time
    current_time = time.time()
    max_age_seconds = max_age_days * 24 * 60 * 60
    
    removed_count = 0
    try:
        for file_path in find_files(directory, pattern):
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > max_age_seconds:
                    if delete_file_safe(file_path):
                        removed_count += 1
    except Exception as e:
        logger.error(f"Error during cleanup of {directory}: {e}")
    
    logger.info(f"Cleaned up {removed_count} old files from {directory}")
    return removed_count


def archive_directory(source: Path, archive_path: Path, 
                     compress: bool = True) -> bool:
    """Archive directory to zip or tar.gz"""
    try:
        ensure_directory(archive_path.parent)
        
        if compress:
            # Create tar.gz archive
            import tarfile
            with tarfile.open(archive_path.with_suffix('.tar.gz'), 'w:gz') as tar:
                tar.add(source, arcname=source.name)
        else:
            # Create zip archive
            import zipfile
            with zipfile.ZipFile(archive_path.with_suffix('.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in source.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(source.parent)
                        zipf.write(file_path, arcname)
        
        logger.info(f"Archived directory: {source} -> {archive_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to archive directory {source}: {e}")
        return False


def get_available_space(path: Path) -> int:
    """Get available disk space in bytes"""
    try:
        import shutil
        _, _, free = shutil.disk_usage(path)
        return free
    except Exception as e:
        logger.error(f"Error getting disk space for {path}: {e}")
        return 0


def is_space_available(path: Path, required_bytes: int) -> bool:
    """Check if enough disk space is available"""
    available = get_available_space(path)
    return available >= required_bytes


class TemporaryDirectory:
    """Context manager for temporary directory"""
    
    def __init__(self, base_path: Path = None, prefix: str = "tmp"):
        self.base_path = base_path or Path.cwd()
        self.prefix = prefix
        self.path = None
    
    def __enter__(self) -> Path:
        self.path = create_timestamped_dir(self.base_path, self.prefix)
        return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path and self.path.exists():
            try:
                shutil.rmtree(self.path)
                logger.debug(f"Cleaned up temporary directory: {self.path}")
            except Exception as e:
                logger.error(f"Failed to clean up temporary directory {self.path}: {e}")


class FileMonitor:
    """Monitor file changes"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.last_modified = 0
        if file_path.exists():
            self.last_modified = file_path.stat().st_mtime
    
    def has_changed(self) -> bool:
        """Check if file has been modified"""
        if not self.file_path.exists():
            return False
        
        current_modified = self.file_path.stat().st_mtime
        if current_modified > self.last_modified:
            self.last_modified = current_modified
            return True
        
        return False
