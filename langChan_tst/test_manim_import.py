#!/usr/bin/env python3
"""
Simple test to check if manim can be imported and used directly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

def test_manim_import():
    """Test if manim can be imported"""
    print("🧪 Testing Manim Import")
    print("-" * 30)
    
    try:
        import manim
        print(f"✅ Manim imported successfully")
        print(f"📦 Manim version: {manim.__version__}")
        
        # Try to create a simple scene
        from manim import Scene, Circle, Write
        
        class TestScene(Scene):
            def construct(self):
                circle = Circle()
                self.play(Write(circle))
                self.wait(1)
        
        print("✅ Simple scene created successfully")
        
        # Test layout imports
        try:
            from src.templates.layouts import TitleAndMainContent
            print("✅ Layout manager imported successfully")
        except ImportError as e:
            print(f"⚠️  Layout manager import failed: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Manim import failed: {e}")
        return False

if __name__ == "__main__":
    test_manim_import()
