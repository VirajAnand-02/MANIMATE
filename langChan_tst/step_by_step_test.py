#!/usr/bin/env python3
"""
Step by step import test to find the hanging import
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("Step 1: Testing basic imports...")
try:
    from google import genai
    print("✓ Google genai imported")
except Exception as e:
    print(f"❌ Google genai import error: {e}")

try:
    from openai import OpenAI
    print("✓ OpenAI imported")
except Exception as e:
    print(f"❌ OpenAI import error: {e}")

print("\nStep 2: Testing models import...")
try:
    from src.core.models import VideoScript, Scene, ManimConfig, BatchRequest, BatchResponse, LayoutType, ProcessingSummary
    print("✓ Models imported")
except Exception as e:
    print(f"❌ Models import error: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 3: Testing config import...")
try:
    from config.settings import GOOGLE_API_KEY, OPENAI_API_KEY, SYSTEM_PROMPT_SCRIPT, SYSTEM_PROMPT_MANIM, MANIM_REF_PATH
    print("✓ Config imported")
except Exception as e:
    print(f"❌ Config import error: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")
