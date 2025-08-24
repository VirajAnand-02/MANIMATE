#!/usr/bin/env python3
"""Check project dependencies"""

import importlib.util
import sys

def check_module(module_name, import_name=None):
    """Check if a module can be imported"""
    try:
        if import_name:
            __import__(import_name)
        else:
            __import__(module_name)
        return True
    except ImportError:
        return False

modules = [
    ('manim', None),
    ('openai', None),
    ('pydantic', None),
    ('python-dotenv', 'dotenv'),
    ('google-genai', 'google.genai'),
]

print("=== Dependency Check ===")
all_good = True
for module, import_name in modules:
    if check_module(module, import_name):
        print(f"✓ {module}")
    else:
        print(f"✗ {module}")
        all_good = False

print(f"\nPython version: {sys.version}")
print(f"All dependencies satisfied: {'Yes' if all_good else 'No'}")

# Check if we can import our own modules
print("\n=== Project Imports ===")
try:
    from config.settings import validate_config
    print("✓ config.settings")
except ImportError as e:
    print(f"✗ config.settings: {e}")
    all_good = False

try:
    from src.core.models import VideoScript, Scene
    print("✓ src.core.models")
except ImportError as e:
    print(f"✗ src.core.models: {e}")
    all_good = False

try:
    from src.templates.layouts import TitleAndMainContent
    print("✓ src.templates.layouts")
except ImportError as e:
    print(f"✗ src.templates.layouts: {e}")
    all_good = False

print(f"\nProject ready: {'Yes' if all_good else 'No'}")
