#!/usr/bin/env python3
"""Test script to verify parallel processing fixes"""

import sys
from pathlib import Path
from src.utils.parallel import ManimParallelProcessor
from src.core.models import QualityPreset

# Simple test scene code
TEST_SCENE_CODE = '''
import sys
sys.path.append(r'E:\\programming\\Notes2Manim\\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent

class TestScene(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("Test Title", width=self.title_region.width, height=1)
        title.move_to(self.title_region.get_center())
        
        content = self.create_textbox("Simple test content", width=self.main_region.width, height=2)
        content.move_to(self.main_region.get_center())
        
        self.play(Write(title))
        self.play(FadeIn(content))
        self.wait(2)

# Set narration and duration
TestScene.narration_text = "This is a simple test scene."
TestScene.audio_duration = 5.0
'''

def main():
    print("Testing parallel processor fixes...")
    
    # Create processor
    processor = ManimParallelProcessor(max_workers=1)
    
    # Create test tasks
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    render_tasks = [{
        "scene_code": TEST_SCENE_CODE,
        "class_name": "TestScene", 
        "output_dir": output_dir,
        "quality": QualityPreset.HIGH
    }]
    
    try:
        print("Running parallel render test...")
        results = processor.render_scenes(render_tasks)
        
        print(f"Render results: {len(results)} scenes processed")
        for scene_id, video_path in results.items():
            print(f"  Scene {scene_id}: {video_path}")
            
        print("✓ Parallel processing test successful!")
        
    except Exception as e:
        print(f"✗ Parallel processing test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
