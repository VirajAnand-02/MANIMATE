import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        from manim import *
        import numpy as np

        def construct_scene(self):
        # --- Configuration ---
        pivot_point = self.left_region.get_center() + UP * self.left_region.height / 2 * 0.8
        string_length = self.left_region.height * 0.35
        bob_radius = 0.25
        max_angle = 30 * DEGREES # For amplitude

        # --- Left Side: Pendulum Animation ---
        angle_tracker = ValueTracker(0) # Start at equilibrium

        # Pendulum components
        pivot = Dot(pivot_point, color=WHITE)

        string = always_redraw(
        lambda: Line(pivot_point, pivot_point + DOWN * string_length).rotate(
        angle_tracker.get_value(), about_point=pivot_point
        )
        )
        bob = always_redraw(
        lambda: Circle(radius=bob_radius, color=BLUE, fill_opacity=1)
        .move_to(string.get_end())
        )
        pendulum_mobjects = VGroup(string, bob)

        # Equilibrium line and label
        equilibrium_line = DashedLine(pivot_point, pivot_point + DOWN * string_length * 1.2, color=GRAY)
        equilibrium_label = Text("Equilibrium", font_size=24).next_to(equilibrium_line, DOWN, buff=0.2)
        equilibrium_group = VGroup(equilibrium_line, equilibrium_label).set_opacity(0)

        # Amplitude arc and label
        amplitude_arc = always_redraw(
        lambda: Arc(
        start_angle=PI/2,
        angle=-angle_tracker.get_value(),
        radius=string_length * 0.3,
        arc_center=pivot_point,
        color=YELLOW,
        stroke_width=5
        ).set_opacity(1 if abs(angle_tracker.get_value()) > 0.01 else 0)
        )
        # Position amplitude label when angle is max_angle
        amplitude_label_pos = pivot_point + rotate_vector(DOWN * string_length * 0.5, -max_angle / 2) + RIGHT * 0.5
        amplitude_label = Text("Amplitude", font_size=24, color=YELLOW).move_to(amplitude_label_pos).set_opacity(0)

        # Path for period tracing
        bob_path = VMobject(color=RED, stroke_width=4)
        bob_path.set_points_as_corners([bob.get_center()]) # Initialize path
        def update_bob_path(path):
        if path.get_opacity() > 0: # Only update if visible
        path.add_points_as_corners([bob.get_center()])
        bob_path.add_updater(update_bob_path)
        bob_path.set_opacity(0) # Start invisible

        # Restoring force arrow and label
        restoring_force_arrow = always_redraw(
        lambda: (
        Arrow(
        bob.get_center(),
        bob.get_center() + rotate_vector(bob.get_center() - pivot_point, -PI/2 if angle_tracker.get_value() > 0 else PI/2).normalize() * 0.7,
        buff=0,
        max_stroke_width_to_length_ratio=0.1,
        max_tip_length_to_length_ratio=0.3,
        color=RED
        ).set_opacity(1)
        if abs(angle_tracker.get_value()) > 0.05 else Arrow(ORIGIN, ORIGIN).set_opacity(0)
        )
        )
        restoring_force_label = Text("Restoring Force", font_size=20, color=RED).next_to(restoring_force_arrow, DOWN, buff=0.1).set_opacity(0)

        # Add initial mobjects to scene
        self.add(pivot, pendulum_mobjects, equilibrium_group, amplitude_arc, amplitude_label, bob_path, restoring_force_arrow, restoring_force_label)

        # --- Right Side: Text Definitions ---
        text_definitions = VGroup()

        eq_pos_text = self.create_textbox("Equilibrium Position: Where the bob rests when not moving, directly below the pivot.", self.right_region.width * 0.9, self.right_region.height * 0.15)
        amplitude_text = self.create_textbox("Amplitude: The maximum displacement from the equilibrium position.", self.right_region.width * 0.9, self.right_region.height * 0.15)
        period_text = self.create_textbox("Period: The time for one complete back-and-forth swing.", self.right_region.width * 0.9, self.right_region.height * 0.15)
        frequency_text = self.create_textbox("Frequency: The number of complete swings per second.", self.right_region.width * 0.9, self.right_region.height * 0.15)
        restoring_force_text = self.create_textbox("Restoring Force: A component of gravity that pulls the bob back towards equilibrium when displaced.", self.right_region.width * 0.9, self.right_region.height * 0.2)

        text_definitions.add(eq_pos_text, amplitude_text, period_text, frequency_text, restoring_force_text)
        text_definitions.arrange(DOWN, buff=0.5).move_to(self.right_region.get_center())
        text_definitions.set_opacity(0) # Start all text invisible

        # --- Animations ---

        # Initial state: Pendulum at equilibrium, no text
        self.wait(1) # "Let's define some key terms."

        # Equilibrium Position (Narration: ~8s)
        self.play(
        FadeIn(equilibrium_group, shift=UP),
        FadeIn(text_definitions[0], shift=UP),
        run_time=7
        )
        self.wait(1) # Hold for narration

        # Amplitude (Narration: ~7s)
        self.play(
        angle_tracker.animate.set_value(max_angle),
        FadeIn(amplitude_label, shift=UP),
        FadeIn(text_definitions[1], shift=UP),
        run_time=5
        )
        self.wait(0.5)
        self.play(angle_tracker.animate.set_value(0), run_time=1.5) # Return to equilibrium briefly

        # Period (Narration: ~10s)
        # Reset path for tracing
        bob_path.clear_points() # Clear previous path
        bob_path.set_points_as_corners([bob.get_center()]) # Start new path from current position

        self.play(FadeIn(bob_path), FadeIn(text_definitions[2], shift=UP), run_time=2)

        # Swing one full period
        self.play(
        angle_tracker.animate.set_value(max_angle), # Swing right
        run_time=2,
        rate_func=rate_functions.ease_in_sine
        )
        self.play(
        angle_tracker.animate.set_value(-max_angle), # Swing left
        run_time=4,
        rate_func=rate_functions.linear
        )
        self.play(
        angle_tracker.animate.set_value(0), # Return to equilibrium
        run_time=2,
        rate_func=rate_functions.ease_out_sine
        )
        self.wait(0.5)
        self.play(FadeOut(bob_path), run_time=0.5) # Fade out path

        # Frequency (Narration: ~5s)
        self.play(FadeIn(text_definitions[3], shift=UP), run_time=5)

        # Restoring Force (Narration: ~13s)
        self.play(
        angle_tracker.animate.set_value(max_angle / 2), # Displace slightly to show force
        FadeIn(restoring_force_label, shift=UP),
        FadeIn(text_definitions[4], shift=UP),
        run_time=3
        )
        self.wait(10) # Hold to show restoring force and text

        # Clean up
        self.play(
        FadeOut(equilibrium_group),
        FadeOut(amplitude_label),
        FadeOut(restoring_force_label),
        FadeOut(text_definitions),
        FadeOut(pendulum_mobjects),
        FadeOut(pivot),
        FadeOut(amplitude_arc),
        FadeOut(restoring_force_arrow),
        run_time=2
        )
        self.wait(0.5)

# Set narration and duration
Scene2.narration_text = '''Let\'s define some key terms. The \'equilibrium position\' is where the bob rests when not moving – directly below the pivot. When we pull the bob to the side, the maximum displacement from equilibrium is called the \'amplitude\'. The time it takes for one complete back-and-forth swing, returning to its starting point, is the \'period\' of the pendulum. And the number of complete swings per second is its \'frequency\'. Gravity pulls the bob down, but the tension in the string keeps it from falling straight. When displaced, a component of gravity acts as a \'restoring force\', pulling the bob back towards equilibrium.'''
Scene2.audio_duration = 5.0
