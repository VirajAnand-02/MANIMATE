#!/usr/bin/env python3
"""
Test direct model import without going through __init__.py files
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    print("Testing direct models import...")
    # Import the models module directly, bypassing __init__.py files
    import importlib.util
    models_path = Path(__file__).parent / "src" / "core" / "models.py"
    spec = importlib.util.spec_from_file_location("models", models_path)
    models_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models_module)
    
    print("✓ Direct models import successful")
    print(f"Available classes: {[name for name in dir(models_module) if name[0].isupper()]}")
    
except Exception as e:
    print(f"❌ Direct models import error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed!")
