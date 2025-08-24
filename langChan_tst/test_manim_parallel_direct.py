#!/usr/bin/env python3
"""
Direct test of ManimParallelProcessor functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.parallel import ManimParallelProcessor
from src.core.models import QualityPreset, Scene, LayoutType
from src.utils.logging import setup_logging
from config.settings import TMP_DIR, RENDERS_DIR
from src.utils.file_ops import ensure_directory

def test_manim_parallel_processor():
    """Test the ManimParallelProcessor directly"""
    
    setup_logging("INFO", include_console=True)
    
    print("🧪 Testing ManimParallelProcessor directly")
    print("-" * 50)
    
    # Create processor
    processor = ManimParallelProcessor(max_workers=2)
    print(f"✓ ManimParallelProcessor created with 2 workers")
    
    # Create test scenes
    test_scenes = [
        Scene(seq=1, text="Test scene 1", anim="Simple animation", layout=LayoutType.TITLE_AND_MAIN),
        Scene(seq=2, text="Test scene 2", anim="Another animation", layout=LayoutType.TITLE_AND_MAIN)
    ]
    
    # Create simple test code for each scene
    simple_scene_template = """import sys
sys.path.append(r'{project_root}')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene{seq}(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Test Scene {seq}", 
                                       self.title_region.width, 
                                       self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        
        main_text = self.create_textbox("{text}", 
                                      self.main_region.width, 
                                      self.main_region.height)
        main_text.move_to(self.main_region.get_center())
        
        self.play(Write(title_text))
        self.wait(1)
        self.play(Write(main_text))
        self.wait(2)
        self.play(FadeOut(title_text), FadeOut(main_text))

Scene{seq}.narration_text = '''{text}'''
Scene{seq}.audio_duration = 5.0
"""
    
    # Prepare render tasks
    render_tasks = []
    for scene in test_scenes:
        scene_code = simple_scene_template.format(
            project_root=Path(__file__).parent.absolute(),
            seq=scene.seq,
            text=scene.text
        )
        
        render_task = {
            "task_id": f"render_scene_{scene.seq}",
            "scene": scene,
            "scene_code": scene_code,
            "class_name": f"Scene{scene.seq}",
            "quality": QualityPreset.LOW
        }
        render_tasks.append(render_task)
    
    print(f"✓ Created {len(render_tasks)} render tasks")
    
    # Run parallel rendering
    try:
        print("🚀 Starting parallel rendering...")
        results = processor.render_scenes_batch(render_tasks)
        
        print(f"📊 Results: {len(results)} out of {len(render_tasks)} scenes rendered")
        
        success_count = 0
        for task in render_tasks:
            task_id = task["task_id"]
            if task_id in results:
                video_path = results[task_id]
                print(f"✅ {task_id}: {video_path}")
                success_count += 1
            else:
                print(f"❌ {task_id}: Failed")
        
        print(f"\n📈 Success rate: {success_count}/{len(render_tasks)}")
        
        if success_count == len(render_tasks):
            print("🎉 All scenes rendered successfully!")
            return True
        else:
            print("⚠️  Some scenes failed to render")
            return False
            
    except Exception as e:
        print(f"❌ Parallel rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_manim_parallel_processor()
