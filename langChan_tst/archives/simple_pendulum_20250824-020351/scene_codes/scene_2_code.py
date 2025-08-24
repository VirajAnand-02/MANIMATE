import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Simple Pendulum", width=self.left_region.width, height=1)
                title.move_to(self.left_region.get_center())

                bob_radius = 0.2
                string_length = 2
                pivot_point = UP * 2
                bob_initial_position = pivot_point + DOWN * string_length + LEFT * 1.5

                # Create pendulum components
                bob = Circle(radius=bob_radius, color=BLUE, fill_opacity=1)
                bob.move_to(bob_initial_position)
                string = Line(pivot_point, bob.get_center(), color=WHITE)

                # Gravity arrow
                gravity_arrow = Arrow(bob.get_center(), bob.get_center() + DOWN * 0.5, color=YELLOW)
                gravity_label = MathTex("mg", color=YELLOW).next_to(gravity_arrow, RIGHT)

                # Group for easy animation
                pendulum = VGroup(bob, string)
                gravity = VGroup(gravity_arrow, gravity_label)

                # Initial state
                self.add(pivot_point, pendulum, gravity)
                self.wait(1)

                # Animate the pendulum swinging
                swing_angle = 30 * DEGREES
                swing_duration = 2

                # Define the target position
                bob_final_position = pivot_point + DOWN * string_length + RIGHT * 1.5
                string_final = Line(pivot_point, bob_final_position, color=WHITE)
                pendulum_final = VGroup(
                    Circle(radius=bob_radius, color=BLUE, fill_opacity=1).move_to(bob_final_position),
                    string_final
                )

                self.play(
                    Rotate(
                        pendulum,
                        angle=-swing_angle,
                        about_point=pivot_point,
                        run_time=swing_duration / 2
                    )
                )
                self.wait(0.5)

                self.play(
                    Rotate(
                        pendulum,
                        angle=2 * swing_angle,
                        about_point=pivot_point,
                        run_time=swing_duration
                    )
                )
                self.wait(0.5)

                self.play(
                    Rotate(
                        pendulum,
                        angle=-swing_angle,
                        about_point=pivot_point,
                        run_time=swing_duration / 2
                    )
                )

                self.wait(2)

# Set narration and duration
Scene2.narration_text = '''A simple pendulum is, well, simple! It consists of a mass, called the bob, suspended from a fixed point by a light string or rod. When displaced from its resting position and released, gravity pulls it back, causing it to swing. This back-and-forth motion is called oscillation.'''
Scene2.audio_duration = 5.0
