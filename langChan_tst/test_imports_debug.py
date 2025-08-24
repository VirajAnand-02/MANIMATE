"""
Debug import issues
"""

import sys
import traceback
from pathlib import Path

# Add project to path
sys.path.insert(0, '.')

print(f"Python path: {sys.path[:3]}")
print(f"Current directory: {Path.cwd()}")

try:
    print("Testing config import...")
    from config.settings import PROJECT_ROOT, validate_config
    print(f"✅ Config imported successfully")
    
    print("Testing core models...")
    from src.core.models import TTSConfig, TTSProvider
    print(f"✅ Models imported successfully")
    
    print("Testing engine import...")
    from src.core.engine import create_video_engine
    print(f"✅ Engine imported successfully")
    
    print("Testing main imports...")
    from src.core.engine import create_video_engine
    from src.core.models import TTSConfig, ManimConfig, RenderConfig
    from src.utils.logging import setup_logging
    from config.settings import validate_config, setup_directories
    print(f"✅ All main imports successful")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    traceback.print_exc()
