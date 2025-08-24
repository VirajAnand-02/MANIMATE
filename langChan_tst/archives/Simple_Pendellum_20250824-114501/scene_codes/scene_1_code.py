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
        title_text = self.create_textbox("The Simple Pendulum", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text), run_time=2.5)
        self.wait(1.5)

        # Define pendulum parameters relative to main_region
        # Pivot point is slightly above the center of the main_region
        pivot_point = self.main_region.get_center() + UP * self.main_region.height * 0.3
        string_length = self.main_region.height * 0.45 # Make string a bit longer to fill space
        bob_radius = 0.3

        # Mobjects for the pendulum components
        pivot = Dot(pivot_point, radius=0.08, color=WHITE)
        string = Line(pivot.get_center(), pivot.get_center() + DOWN * string_length, color=WHITE, stroke_width=3)
        bob = Circle(radius=bob_radius, color=BLUE, fill_opacity=1).move_to(string.get_end())

        # Labels for the components
        pivot_label = Text("Pivot", font_size=28).next_to(pivot, UP, buff=0.2)
        string_label = Text("String", font_size=28).next_to(string, LEFT, buff=0.2)
        bob_label = Text("Bob", font_size=28).next_to(bob, RIGHT, buff=0.2)

        # Length (L) label with a brace
        length_brace = Brace(string, RIGHT)
        length_label = MathTex("L", font_size=36).next_to(length_brace, RIGHT, buff=0.1)

        # Equilibrium position: a dashed line and its label
        equilibrium_line = DashedLine(
        pivot.get_center(),
        pivot.get_center() + DOWN * (string_length + bob_radius + 0.5), # Extend slightly below bob
        dash_length=0.1,
        color=YELLOW
        )
        equilibrium_label = Text("Equilibrium Position", font_size=24, color=YELLOW).next_to(equilibrium_line, DOWN, buff=0.2)

        # Group all pendulum elements for potential scaling/positioning if needed
        pendulum_group = VGroup(
        pivot, string, bob,
        pivot_label, string_label, bob_label,
        length_brace, length_label,
        equilibrium_line, equilibrium_label
        )

        # Ensure the entire pendulum group fits within the main_region
        # This scales it down if it's too large, maintaining aspect ratio
        if pendulum_group.height > self.main_region.height * 0.9:
        pendulum_group.set_height(self.main_region.height * 0.9)
        pendulum_group.move_to(self.main_region.get_center())

        # Re-extract individual mobjects after grouping and potential scaling/moving
        # This is important because move_to/set_height on a VGroup changes its sub-mobjects' positions
        pivot, string, bob, pivot_label, string_label, bob_label, length_brace, length_label, equilibrium_line, equilibrium_label = pendulum_group.submobjects

        # Animation sequence for the pendulum diagram
        self.play(FadeIn(pivot, scale=0.5), run_time=1.5)
        self.play(Create(string), run_time=2.5)
        self.play(Create(bob), run_time=2)
        self.wait(2) # Pause after basic pendulum is formed

        self.play(
        Write(pivot_label),
        Write(string_label),
        Write(bob_label),
        run_time=3
        )
        self.wait(1.5)

        self.play(
        GrowFromCenter(length_brace),
        Write(length_label),
        run_time=2.5
        )
        self.wait(1.5)

        self.play(
        Create(equilibrium_line),
        Write(equilibrium_label),
        run_time=3
        )
        self.wait(5) # Long wait to emphasize the equilibrium position

        # Fade out everything to prepare for the next scene
        self.play(FadeOut(title_text), run_time=1.5)
        self.play(FadeOut(pendulum_group), run_time=2)
        self.wait(0.5)

# Set narration and duration
Scene1.narration_text = '''Ever wondered how some clocks keep perfect time, or how a simple swing moves back and forth? The secret lies in the Simple Pendulum! At its core, a simple pendulum is just a point mass, called the \'bob,\' suspended from a fixed pivot by a massless, inextensible string. When it\'s not moving, it rests at its \'equilibrium position,\' hanging straight down due to gravity.'''
Scene1.audio_duration = 5.0
