"""
Logging utilities and configuration
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

import sys
from pathlib import Path
# Add project root to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import LOG_LEVEL, LOG_FORMAT, LOGS_DIR


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m'  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)


class ProcessLogger:
    """Logger for tracking process steps"""
    
    def __init__(self, name: str, log_file: Optional[Path] = None):
        self.logger = logging.getLogger(name)
        self.log_file = log_file
        self.steps_completed = 0
        self.total_steps = 0
        self.current_step = ""
        
    def start_process(self, process_name: str, total_steps: int = 0):
        """Start a new process"""
        self.current_step = process_name
        self.total_steps = total_steps
        self.steps_completed = 0
        
        self.logger.info(f"🚀 Starting: {process_name}")
        if total_steps > 0:
            self.logger.info(f"📊 Total steps: {total_steps}")
    
    def step(self, step_name: str, details: str = ""):
        """Log a step completion"""
        self.steps_completed += 1
        
        if self.total_steps > 0:
            progress = (self.steps_completed / self.total_steps) * 100
            self.logger.info(f"✓ [{self.steps_completed}/{self.total_steps}] {step_name} ({progress:.1f}%)")
        else:
            self.logger.info(f"✓ {step_name}")
        
        if details:
            self.logger.debug(f"   {details}")
    
    def error(self, error_name: str, details: str = ""):
        """Log an error"""
        self.logger.error(f"✗ {error_name}")
        if details:
            self.logger.error(f"   {details}")
    
    def warning(self, warning_name: str, details: str = ""):
        """Log a warning"""
        self.logger.warning(f"⚠️  {warning_name}")
        if details:
            self.logger.warning(f"   {details}")
    
    def complete(self, summary: str = ""):
        """Mark process as complete"""
        self.logger.info(f"🎉 Completed: {self.current_step}")
        if summary:
            self.logger.info(f"📋 Summary: {summary}")


class StatsLogger:
    """Logger for collecting and reporting statistics"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(f"{name}.stats")
        self.stats: Dict[str, Any] = {}
        self.start_time = datetime.now()
    
    def record(self, key: str, value: Any):
        """Record a statistic"""
        self.stats[key] = value
        self.logger.debug(f"Stat recorded: {key} = {value}")
    
    def increment(self, key: str, amount: int = 1):
        """Increment a counter statistic"""
        self.stats[key] = self.stats.get(key, 0) + amount
        self.logger.debug(f"Stat incremented: {key} = {self.stats[key]}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get all statistics"""
        elapsed = datetime.now() - self.start_time
        self.stats['elapsed_time_seconds'] = elapsed.total_seconds()
        return self.stats.copy()
    
    def report(self, title: str = "Statistics"):
        """Report all statistics"""
        self.logger.info(f"📈 {title}")
        stats = self.get_stats()
        
        for key, value in stats.items():
            if isinstance(value, float):
                self.logger.info(f"   {key}: {value:.2f}")
            else:
                self.logger.info(f"   {key}: {value}")


def setup_logging(log_level: str = None, log_file: Path = None, 
                 include_console: bool = True) -> logging.Logger:
    """Setup logging configuration"""
    # Use provided level or default from settings
    level = getattr(logging, (log_level or LOG_LEVEL).upper(), logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    colored_formatter = ColoredFormatter(LOG_FORMAT)
    
    # Console handler
    if include_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(colored_formatter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        from src.utils.file_ops import ensure_directory
        ensure_directory(log_file.parent)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Add default file handler if none specified
    elif LOGS_DIR:
        from src.utils.file_ops import ensure_directory, create_timestamped_dir
        
        logs_dir = ensure_directory(LOGS_DIR)
        log_file = logs_dir / f"video_generation_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get logger with specified name"""
    return logging.getLogger(name)


class LogCapture:
    """Context manager to capture log messages"""
    
    def __init__(self, logger: logging.Logger, level: int = logging.INFO):
        self.logger = logger
        self.level = level
        self.handler = None
        self.messages = []
    
    def __enter__(self):
        # Create custom handler to capture messages
        class ListHandler(logging.Handler):
            def __init__(self, message_list):
                super().__init__()
                self.messages = message_list
            
            def emit(self, record):
                self.messages.append(self.format(record))
        
        self.handler = ListHandler(self.messages)
        self.handler.setLevel(self.level)
        self.logger.addHandler(self.handler)
        
        return self.messages
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.handler:
            self.logger.removeHandler(self.handler)


def log_function_call(func):
    """Decorator to log function calls"""
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise
    
    return wrapper


def log_execution_time(func):
    """Decorator to log function execution time"""
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            elapsed = datetime.now() - start_time
            logger.info(f"{func.__name__} completed in {elapsed.total_seconds():.2f}s")
            return result
        except Exception as e:
            elapsed = datetime.now() - start_time
            logger.error(f"{func.__name__} failed after {elapsed.total_seconds():.2f}s: {e}")
            raise
    
    return wrapper
