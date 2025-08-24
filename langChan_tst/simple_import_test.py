#!/usr/bin/env python3
"""
Simple import test to identify the problematic import
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("Testing config import...")
    from config.settings import GOOGLE_API_KEY
    print("✓ Config import successful")
except Exception as e:
    print(f"❌ Config import error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Testing models import...")
    from src.core.models import VideoScript
    print("✓ Models import successful")
except Exception as e:
    print(f"❌ Models import error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Testing LLM provider import...")
    from src.providers.llm import create_llm_provider
    print("✓ LLM import successful")
except Exception as e:
    print(f"❌ LLM import error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Testing TTS provider import...")
    from src.providers.tts import create_tts_provider
    print("✓ TTS import successful")
except Exception as e:
    print(f"❌ TTS import error: {e}")
    import traceback
    traceback.print_exc()

try:
    print("Testing engine import...")
    from src.core.engine import create_video_engine
    print("✓ Engine import successful")
except Exception as e:
    print(f"❌ Engine import error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed!")
