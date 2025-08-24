import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Simple Pendulum", width=self.title_region.width, height=self.title_region.height)
        title.move_to(self.title_region.get_center())

        bob_radius = 0.2
        string_length = 2
        fixed_point = UP * 2
        bob_initial_angle = PI / 4

        # Create pendulum parts
        bob = Circle(radius=bob_radius, color=BLUE, fill_opacity=1)
        string = Line(fixed_point, fixed_point + DOWN * string_length, color=WHITE)
        bob.move_to(string.get_end())

        # Rotate the pendulum to the initial angle
        bob.rotate(bob_initial_angle, about_point=fixed_point)
        string.rotate(bob_initial_angle, about_point=fixed_point)

        # Create labels
        bob_label = Tex("Bob").next_to(bob, DOWN)
        string_label = Tex("String").next_to(string, LEFT)
        fixed_point_label = Tex("Fixed Point").next_to(fixed_point, UP)
        angle_theta = Angle(Line(fixed_point, fixed_point + RIGHT), string, radius=0.5)
        angle_label = MathTex("\\theta").next_to(angle_theta, RIGHT)

        # Add everything to a group for easy positioning
        pendulum = VGroup(bob, string, bob_label, string_label, fixed_point_label, angle_theta, angle_label)
        pendulum.move_to(self.diagram_region.get_center())

        self.add(title)
        self.add(pendulum)

        # Animation
        def pendulum_updater(mob, alpha):
        angle = bob_initial_angle * np.cos(alpha * PI)
        new_bob_position = fixed_point + string_length * np.array([np.sin(angle), -np.cos(angle), 0])
        mob[0].move_to(new_bob_position)  # Bob
        mob[1].become(Line(fixed_point, new_bob_position, color=WHITE)) # String

        pendulum_animation = AnimationGroup(
        UpdateFromAlphaFunc(VGroup(bob, string), pendulum_updater),
        run_time=5,
        rate_func=linear
        )

        self.play(pendulum_animation)
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''A simple pendulum consists of a mass, often called a \'bob\', suspended from a fixed point by a light string or rod. We assume the string is massless and doesn\'t stretch. When the bob is pulled back and released, gravity pulls it downwards, causing it to swing back and forth. This motion is called oscillation.'''
Scene2.audio_duration = 5.0
