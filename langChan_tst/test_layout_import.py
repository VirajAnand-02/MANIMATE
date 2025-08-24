#!/usr/bin/env python3
"""
Test the manim_layout_manager import fix
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
    print("✓ LayoutManager import successful")
    print(f"  Available strategies: {list(LayoutStrategy)}")
    print(f"  Available positions: {list(PreferredPosition)}")
except ImportError as e:
    LAYOUT_MANAGER_AVAILABLE = False
    print(f"✗ LayoutManager import failed: {e}")

if LAYOUT_MANAGER_AVAILABLE:
    try:
        # Test basic functionality
        region = BoundingBox(-5, -3, 5, 3)
        layout_manager = LayoutManager(region, padding=0.1)
        print("✓ LayoutManager creation successful")
        print(f"  Region: {region}")
        print(f"  Strategy: {layout_manager.strategy}")
    except Exception as e:
        print(f"✗ LayoutManager creation failed: {e}")

print(f"\nLAYOUT_MANAGER_AVAILABLE = {LAYOUT_MANAGER_AVAILABLE}")
