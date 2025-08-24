# layouts.py
import sys
from pathlib import Path

# Add project root to path for layout manager import
sys.path.append(str(Path(__file__).parent.parent.parent))

from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False


class TemplateScene(Scene):
    """
    Base class for video templates. Provides helpers for fitted textboxes and narration display.
    """
    def create_textbox(self, text_str: str, width: float, height: float, font_size: int = 48) -> VGroup:
        text = Text(text_str, font_size=font_size)
        if text.width > width or text.height > height:
            scale_factor = min(width / text.width, height / text.height)
            text.scale(scale_factor)
        return text

    def display_narration(self, narration_text: str, audio_duration: float) -> None:
        narration_box = Rectangle(
            width=self.camera.frame_width * 0.9,
            height=self.camera.frame_height * 0.2,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0
        ).to_edge(DOWN, buff=0.2)
        narration_content = self.create_textbox(
            narration_text,
            width=narration_box.width * 0.95,
            height=narration_box.height * 0.9
        ).move_to(narration_box.get_center())
        narration_group = VGroup(narration_box, narration_content)
        self.play(FadeIn(narration_group))
        self.wait(audio_duration)
        self.play(FadeOut(narration_group))

    def construct_scene(self, **kwargs) -> None:
        raise NotImplementedError("This method should be filled by the LLM.")

    def construct(self) -> None:
        narration_text = getattr(self, 'narration_text', "")
        audio_duration = getattr(self, 'audio_duration', 0)
        self.construct_scene()
        if narration_text and audio_duration > 0:
            self.display_narration(narration_text, audio_duration)
        else:
            self.wait(1)



class TitleAndMainContent(TemplateScene):
    def setup(self) -> None:
        super().setup()
        self.title_region = Rectangle(
            width=self.camera.frame_width * 0.9,
            height=self.camera.frame_height * 0.15,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(UP, buff=0.3)
        self.main_region = Rectangle(
            width=self.camera.frame_width * 0.9,
            height=self.camera.frame_height * 0.6,
            stroke_opacity=0,
            fill_opacity=0
        ).next_to(self.title_region, DOWN, buff=0.2)
        
        # Create BoundingBox objects for LayoutManager compatibility
        if LAYOUT_MANAGER_AVAILABLE:
            self.title_bbox = BoundingBox(
                self.title_region.get_left()[0], self.title_region.get_bottom()[1],
                self.title_region.get_right()[0], self.title_region.get_top()[1]
            )
            self.main_bbox = BoundingBox(
                self.main_region.get_left()[0], self.main_region.get_bottom()[1],
                self.main_region.get_right()[0], self.main_region.get_top()[1]
            )
        else:
            self.title_bbox = None
            self.main_bbox = None



class SplitScreen(TemplateScene):
    def setup(self) -> None:
        super().setup()
        self.left_region = Rectangle(
            width=self.camera.frame_width * 0.45,
            height=self.camera.frame_height * 0.8,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(LEFT, buff=0.2)
        self.right_region = Rectangle(
            width=self.camera.frame_width * 0.45,
            height=self.camera.frame_height * 0.8,
            stroke_opacity=0,
            fill_opacity=0
        ).to_edge(RIGHT, buff=0.2)
        
        # Create BoundingBox objects for LayoutManager compatibility
        if LAYOUT_MANAGER_AVAILABLE:
            self.left_bbox = BoundingBox(
                self.left_region.get_left()[0], self.left_region.get_bottom()[1],
                self.left_region.get_right()[0], self.left_region.get_top()[1]
            )
            self.right_bbox = BoundingBox(
                self.right_region.get_left()[0], self.right_region.get_bottom()[1],
                self.right_region.get_right()[0], self.right_region.get_top()[1]
            )
        else:
            self.left_bbox = None
            self.right_bbox = None
