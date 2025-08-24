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
        title_text = self.create_textbox(
        "The Simple Pendulum",
        self.title_region.width * 0.9,
        self.title_region.height * 0.8
        )
        title_text.move_to(self.title_region.get_center())

        self.play(FadeIn(title_text), run_time=1)
        self.wait(6) # Narration: "Welcome to the fascinating world of physics! Today, we're exploring the simple pendulum – a fundamental concept that helps us understand oscillations and time itself."
        self.play(FadeOut(title_text), run_time=1)

        # 2. Create the main animation: Simple Pendulum
        # Define pendulum properties
        string_length = self.main_region.height * 0.4
        pivot_point_pos = self.main_region.get_center() + UP * self.main_region.height / 2 * 0.8

        # Mobjects for the pendulum
        pivot_point = Dot(pivot_point_pos, color=WHITE)
        string = Line(pivot_point_pos, pivot_point_pos + DOWN * string_length, stroke_width=3, color=WHITE)
        bob = Circle(radius=0.2, color=BLUE, fill_opacity=1).move_to(string.get_end())

        # Labels for the pendulum components
        pivot_label = Text("Pivot Point", font_size=24).next_to(pivot_point, UP)
        # Use always_redraw for labels that need to follow moving objects
        string_label = always_redraw(lambda: Text("String", font_size=24).next_to(string, LEFT))
        bob_label = always_redraw(lambda: Text("Bob", font_size=24).next_to(bob, RIGHT))

        # Add initial components to the scene (labels will appear with their respective mobjects)
        self.add(pivot_point, pivot_label, string, bob, string_label, bob_label)

        # Animation sequence for setting up the pendulum and labels
        self.play(FadeIn(pivot_point), Write(pivot_label), run_time=1)
        self.play(Create(string), run_time=1) # string_label appears with string
        self.play(Create(bob), run_time=1) # bob_label appears with bob
        self.wait(7) # Narration: "A simple pendulum is essentially a point mass, called a bob, suspended from a fixed point by a light, inextensible string."

        # Displace the pendulum from equilibrium
        initial_angle = 30 * DEGREES
        # Temporarily group string and bob to rotate them together
        temp_pendulum_group = VGroup(string, bob)
        self.play(
        Rotate(temp_pendulum_group, angle=initial_angle, about_point=pivot_point_pos, rate_func=ease_out_sine),
        run_time=2
        )

        # Prepare for continuous oscillation using a ValueTracker and updater
        angle_tracker = ValueTracker(initial_angle)

        # Define the updater function to continuously update the pendulum's position
        def update_pendulum_components(dt):
        current_angle = angle_tracker.get_value()
        # Reset string to vertical, then rotate it
        string.put_start_and_end_on(pivot_point_pos, pivot_point_pos + DOWN * string_length)
        string.rotate(current_angle, about_point=pivot_point_pos)
        # Move the bob to the new end of the string
        bob.move_to(string.get_end())

        self.add_updater(update_pendulum_components)

        # Animate the oscillation
        self.play(angle_tracker.animate.set_value(-initial_angle), run_time=3, rate_func=there_and_back)
        self.play(angle_tracker.animate.set_value(initial_angle), run_time=3, rate_func=there_and_back)
        self.play(angle_tracker.animate.set_value(0), run_time=2, rate_func=ease_in_out_sine)
        self.wait(2) # Narration: "When displaced from its resting position and released, it swings back and forth due to gravity. This repetitive motion is called oscillation."

        # Remove the updater to stop the continuous motion
        self.remove_updater(update_pendulum_components)

# Set narration and duration
Scene1.narration_text = '''Welcome to the fascinating world of physics! Today, we\'re exploring the simple pendulum – a fundamental concept that helps us understand oscillations and time itself. A simple pendulum is essentially a point mass, called a bob, suspended from a fixed point by a light, inextensible string. When displaced from its resting position and released, it swings back and forth due to gravity. This repetitive motion is called oscillation.'''
Scene1.audio_duration = 5.0
