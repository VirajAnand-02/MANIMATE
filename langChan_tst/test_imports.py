#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("Testing core engine import...")
    from src.core.engine import create_video_engine
    print("✓ Core engine import successful")
    
    print("Testing providers import...")
    from src.providers.llm import create_llm_provider
    print("✓ Providers import successful")
    
    print("Testing config import...")
    from config.settings import GOOGLE_API_KEY
    print("✓ Config import successful")
    
    print("Testing models import...")
    from src.core.models import VideoScript
    print("✓ Models import successful")
    
    print("\n✓ All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
