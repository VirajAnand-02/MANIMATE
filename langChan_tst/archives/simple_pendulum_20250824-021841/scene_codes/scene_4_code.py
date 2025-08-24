import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene4(SplitScreen):
    def construct_scene(self):
        # Pendulum parameters
        length = 3
        angle = 10 * DEGREES  # Small angle approximation

        # Create pendulums with different masses
        mass1 = 1
        mass2 = 5
        pendulum1 = self.create_pendulum(length, angle, mass1, color=BLUE)
        pendulum2 = self.create_pendulum(length, angle, mass2, color=RED)

        # Position pendulums side by side
        pendulum1.move_to(self.left_region.get_center() + 2 * LEFT)
        pendulum2.move_to(self.right_region.get_center() + 2 * RIGHT)

        # Add pendulums to the scene
        self.add(pendulum1, pendulum2)

        # Animate the pendulums swinging
        duration = 5  # Animation duration
        num_swings = 2  # Number of swings

        self.play(
        self.swing(pendulum1, angle, duration / num_swings),
        self.swing(pendulum2, angle, duration / num_swings),
        run_time=duration
        )

        # Create graph of angle vs period
        axes = Axes(
        x_range=[0, 90, 15],
        y_range=[1, 1.5, 0.1],
        x_length=self.left_region.width * 0.8,
        y_length=self.left_region.height * 0.5,
        axis_config={"include_numbers": True}
        ).move_to(DOWN * 1.5)

        # Define function for period vs angle (approximation)
        def period_vs_angle(theta):
        theta_rad = theta * DEGREES
        return 2 * np.pi * np.sqrt(length / 9.8) * (1 + (1/16) * (np.sin(theta_rad/2))**2)

        # Plot the function
        graph = axes.plot(period_vs_angle, x_range=[0, 90], color=GREEN)

        # Add labels
        x_label = axes.get_x_axis_label(Tex("Angle (degrees)"))
        y_label = axes.get_y_axis_label(Tex("Period (s)"))

        # Add graph to scene
        self.play(Create(axes), Create(graph), Write(x_label), Write(y_label))

        # Highlight deviation at larger angles
        dot = Dot(axes.c2p(60, period_vs_angle(60)), color=YELLOW)
        label = Tex("Deviation increases").next_to(dot, UP)
        self.play(Create(dot), Write(label))

        self.wait(2)

        def create_pendulum(self, length, angle, mass, color):
        # Create pendulum components
        pivot = Dot(ORIGIN, color=GRAY)
        string = Line(pivot.get_center(), [0, -length, 0], color=GRAY)
        bob = Circle(radius=0.2, color=color, fill_color=color, fill_opacity=1)
        bob.shift(string.get_vector())

        # Group components
        pendulum = VGroup(pivot, string, bob)

        # Rotate to initial angle
        pendulum.rotate(angle, about_point=pivot.get_center())

        return pendulum

        def swing(self, pendulum, angle, duration):
        # Define swing animation
        return pendulum.animate(run_time=duration, rate_func=there_and_back).rotate(
        -2 * angle, about_point=pendulum[0].get_center()
        )

# Set narration and duration
Scene4.narration_text = '''Interestingly, the mass of the bob itself doesn\'t significantly affect the period of a *simple* pendulum, assuming the angle of swing is small. This is a key characteristic. The angle of swing also plays a role; the formula we showed is most accurate for small angles, typically less than 15 degrees.'''
Scene4.audio_duration = 5.0
