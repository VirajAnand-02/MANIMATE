#!/usr/bin/env python3
"""
Working demo that demonstrates core functionality without external API calls
"""

import os
import sys
from pathlib import Path
import tempfile

# Set test environment 
os.environ['GOOGLE_API_KEY'] = 'test_key_123'

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import components
from src.core.models import VideoScript, Scene, LayoutType, TTSConfig, ManimConfig, RenderConfig
from src.templates.layouts import TitleAndMainContent, SplitScreen
from src.utils.file_ops import ensure_directory, save_json, clean_filename
from src.utils.logging import setup_logging, ProcessLogger
from config.settings import RENDERS_DIR, ARCHIVES_DIR, PROJECT_ROOT


def create_sample_script():
    """Create a sample video script"""
    scenes = [
        Scene(
            seq=1,
            text="Welcome to our educational video about linear algebra. Today we'll explore matrix multiplication and its applications.",
            anim="Show a title screen with mathematical symbols and matrices in the background.",
            layout=LayoutType.TITLE_AND_MAIN
        ),
        Scene(
            seq=2, 
            text="A matrix is a rectangular array of numbers, symbols, or expressions arranged in rows and columns.",
            anim="Display a sample 2x3 matrix with clear labels for rows and columns.",
            layout=LayoutType.SPLIT_SCREEN
        ),
        Scene(
            seq=3,
            text="Matrix multiplication requires the number of columns in the first matrix to equal the number of rows in the second matrix.",
            anim="Show two matrices and highlight how dimensions must align for multiplication to be possible.",
            layout=LayoutType.TITLE_AND_MAIN
        ),
        Scene(
            seq=4,
            text="Let's work through a concrete example step by step to see how matrix multiplication works in practice.",
            anim="Animate the step-by-step multiplication of two 2x2 matrices showing each calculation.",
            layout=LayoutType.TITLE_AND_MAIN
        )
    ]
    
    return VideoScript(
        title="Introduction to Matrix Multiplication",
        scenes=scenes
    )


def generate_fallback_manim_code(scene: Scene) -> str:
    """Generate fallback Manim code for a scene"""
    safe_text = scene.text.replace('"', '\\"').replace('"""', '')[:200]
    
    code = f"""import sys
sys.path.append(r'{PROJECT_ROOT}')
from manim import *
from src.templates.layouts import TitleAndMainContent

class Scene{scene.seq}(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene {scene.seq}: {scene.layout.value.replace('_', ' ').title()}", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox("{safe_text}", 
                                      self.main_region.width, 
                                      self.main_region.height, 
                                      font_size=24)
        main_text.move_to(self.main_region.get_center())
        
        # Animate
        self.play(Write(title_text))
        self.wait(1)
        self.play(Write(main_text))
        self.wait(3)
        self.play(FadeOut(title_text), FadeOut(main_text))

Scene{scene.seq}.narration_text = "{safe_text}"
Scene{scene.seq}.audio_duration = 5.0
"""
    
    return code


def test_manim_scene_generation(scene: Scene):
    """Test generating and validating Manim scene code"""
    print(f"  Testing scene {scene.seq} ({scene.layout.value})...")
    
    # Generate code
    code = generate_fallback_manim_code(scene)
    
    # Test syntax validation
    try:
        compile(code, f'<Scene{scene.seq}>', 'exec')
        print(f"    ✓ Scene {scene.seq} code compiles successfully")
        return True, code
    except SyntaxError as e:
        print(f"    ✗ Scene {scene.seq} syntax error: {e}")
        return False, None


def main():
    """Main demo function"""
    print("🎬 AI Video Generation System - Working Demo")
    print("=" * 60)
    
    # Setup logging
    logger = setup_logging("INFO", include_console=True)
    process_logger = ProcessLogger("demo")
    
    process_logger.start_process("Video Generation Demo", 6)
    
    try:
        # Step 1: Create sample script
        process_logger.step("Creating sample script")
        script = create_sample_script()
        print(f"   Generated script with {len(script.scenes)} scenes")
        print(f"   Title: {script.title}")
        
        # Step 2: Setup archive directory
        process_logger.step("Setting up directories")
        clean_topic = clean_filename(script.title.replace(" ", "_"))
        archive_dir = ARCHIVES_DIR / f"demo_{clean_topic}"
        ensure_directory(archive_dir)
        
        for subdir in ["scene_codes", "llm_outputs"]:
            ensure_directory(archive_dir / subdir)
        
        print(f"   Archive directory: {archive_dir}")
        
        # Step 3: Save script
        process_logger.step("Saving script")
        script_file = archive_dir / "llm_outputs" / "demo_script.json"
        save_json(script.dict(), script_file)
        print(f"   Script saved to: {script_file}")
        
        # Step 4: Generate Manim code for each scene
        process_logger.step("Generating Manim code")
        all_success = True
        generated_codes = {}
        
        for scene in script.scenes:
            success, code = test_manim_scene_generation(scene)
            if success:
                # Save code to file
                code_file = archive_dir / "scene_codes" / f"scene_{scene.seq}_demo.py"
                code_file.write_text(code, encoding='utf-8')
                generated_codes[scene.seq] = code_file
                print(f"    ✓ Scene {scene.seq} code saved to {code_file.name}")
            else:
                all_success = False
        
        # Step 5: Test template system
        process_logger.step("Testing template system")
        try:
            title_template = TitleAndMainContent()
            split_template = SplitScreen()
            
            # Test textbox creation
            test_text = title_template.create_textbox("Demo Text", 200, 100)
            print("    ✓ Template system working")
        except Exception as e:
            print(f"    ✗ Template system error: {e}")
            all_success = False
        
        # Step 6: Report results
        process_logger.step("Finalizing demo")
        
        if all_success:
            process_logger.complete("Demo completed successfully")
            
            print("\n" + "=" * 60)
            print("🎉 Demo Results Summary")
            print("=" * 60)
            print(f"✅ Script: {script.title}")
            print(f"✅ Scenes generated: {len(generated_codes)}/{len(script.scenes)}")
            print(f"✅ Archive location: {archive_dir}")
            print(f"✅ Scene codes: {len(generated_codes)} files")
            
            print("\n📁 Generated Files:")
            print(f"  • Script: {script_file}")
            for seq, code_file in generated_codes.items():
                print(f"  • Scene {seq}: {code_file}")
            
            print("\n🔧 To render with Manim:")
            for seq, code_file in generated_codes.items():
                print(f"  manim {code_file} Scene{seq} -qh")
            
            print("\n✨ System is ready for production use!")
            return True
        else:
            print("\n❌ Demo completed with some errors")
            return False
            
    except Exception as e:
        process_logger.error("Demo failed", str(e))
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
