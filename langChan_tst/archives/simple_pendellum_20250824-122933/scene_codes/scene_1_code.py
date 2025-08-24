import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text and place it in the title region
        title_text = "The Simple Pendulum"
        title = self.create_textbox(title_text, width=self.title_region.width, height=self.title_region.height)
        title.move_to(self.title_region.get_center())
        self.play(Write(title), run_time=2)
        self.wait(4) # Wait for initial narration

        # 2. Create the fixed support at the top of the main region
        support_width = self.main_region.width * 0.3
        support_height = 0.3
        support = Rectangle(width=support_width, height=support_height, color=WHITE, fill_opacity=1)
        # Position support horizontally centered at the very top of main_region
        support.move_to(self.main_region.get_center()[0] * RIGHT + self.main_region.get_top()[1] * UP)
        support.shift(DOWN * support_height / 2) # Shift down by half its height to sit on the top edge
        self.play(Create(support), run_time=2)

        # 3. A string appears hanging vertically from the support
        string_start_point = support.get_bottom()
        string_length = self.main_region.height * 0.5 # Make string length relative to main_region height
        string_end_point = string_start_point + DOWN * string_length
        string = Line(string_start_point, string_end_point, color=GRAY, stroke_width=3)
        self.play(Create(string), run_time=2)

        # 4. A small, spherical bob attaches to the end of the string
        bob_radius = 0.4
        bob = Circle(radius=bob_radius, color=RED, fill_opacity=1)
        bob.move_to(string.get_end())
        self.play(GrowFromCenter(bob), run_time=2)
        self.wait(2) # Pause after bob appears, before labels

        # 5. Labels appear for each component
        # Fixed Support Label
        support_label = Text("Fixed Support", font_size=28, color=YELLOW)
        support_label.next_to(support, UP, buff=0.3)
        support_arrow = Arrow(support_label.get_bottom(), support.get_top(), buff=0.1, color=YELLOW, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)
        self.play(Write(support_label), Create(support_arrow), run_time=2)

        # String Label
        string_label = Text("String", font_size=28, color=BLUE)
        string_label.next_to(string, LEFT, buff=0.3)
        string_arrow = Arrow(string_label.get_right(), string.get_center(), buff=0.1, color=BLUE, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)
        self.play(Write(string_label), Create(string_arrow), run_time=2)

        # Bob Label
        bob_label = Text("Bob", font_size=28, color=GREEN)
        bob_label.next_to(bob, DOWN, buff=0.3)
        bob_arrow = Arrow(bob_label.get_top(), bob.get_bottom(), buff=0.1, color=GREEN, max_stroke_width_to_length_ratio=0.5, max_tip_length_to_length_ratio=0.3)
        self.play(Write(bob_label), Create(bob_arrow), run_time=2)

        self.wait(8) # Final wait for the rest of the narration

# Set narration and duration
Scene1.narration_text = '''Have you ever wondered how a grandfather clock keeps time? Or how a swing set moves back and forth? The answer often lies with a simple pendulum! A simple pendulum is a fundamental concept in physics, typically consisting of a small, heavy mass, called a \'bob\', suspended from a fixed point by a light, inextensible string or rod. When displaced from its resting position and released, it swings back and forth under the influence of gravity. It\'s a classic example of periodic motion, which we\'ll explore in this video.'''
Scene1.audio_duration = 5.0
