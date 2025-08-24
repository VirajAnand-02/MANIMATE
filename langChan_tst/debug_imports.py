"""
Simple debug script to test imports
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"Python path: {sys.path[:3]}")
print(f"Current directory: {Path.cwd()}")
print(f"Project root: {project_root}")

try:
    print("Testing config import...")
    from config.settings import PROJECT_ROOT, GEMINI_API_KEY
    print(f"✅ Config imported: PROJECT_ROOT = {PROJECT_ROOT}")
    
    print("Testing core models import...")
    from src.core.models import TTSProvider, QualityPreset, TTSConfig
    print(f"✅ Models imported: TTSProvider.GEMINI = {TTSProvider.GEMINI}")
    
    print("Testing engine import...")
    from src.core.engine import create_video_engine
    print("✅ Engine imported successfully")
    
    print("Testing providers import...")
    from src.providers.tts import TTSProviderFactory
    print("✅ Providers imported successfully")
    
    print("Testing config creation...")
    tts_config = TTSConfig(provider=TTSProvider.GEMINI)
    print(f"✅ Config created: {tts_config}")
    
    print("🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
