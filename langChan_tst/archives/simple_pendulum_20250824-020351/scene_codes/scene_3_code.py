import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene3(SplitScreen):
    def construct_scene(self):
        # Title Text
                title = self.create_textbox("Period of a Pendulum", width=self.left_region.width, height=1)
                title.move_to(self.left_region.get_center())

                # Pendulum Animation
                pendulum_length = 3
                bob_radius = 0.2
                pivot_point = np.array([0, 2, 0])
                bob_initial_position = pivot_point + np.array([pendulum_length * np.sin(PI / 4), -pendulum_length * np.cos(PI / 4), 0])

                line = Line(pivot_point, bob_initial_position, color=WHITE)
                bob = Circle(radius=bob_radius, color=RED, fill_opacity=1).move_to(bob_initial_position)
                pendulum = VGroup(line, bob).move_to(self.right_region.get_center())

                def update_pendulum(obj, alpha):
                    angle = PI / 4 * np.sin(alpha * TAU)
                    new_bob_position = pivot_point + np.array([pendulum_length * np.sin(angle), -pendulum_length * np.cos(angle), 0])
                    obj[0].become(Line(pivot_point, new_bob_position, color=WHITE))
                    obj[1].move_to(new_bob_position)

                timer = DecimalNumber(0, num_decimal_places=2).scale(0.7).to_corner(UL)
                timer.add_updater(lambda t: t.increment_value(self.dt))

                self.add(pendulum, timer)
                self.play(UpdateFromAlphaFunc(pendulum, update_pendulum), run_time=2, rate_func=linear)
                self.wait(0.5)
                self.play(UpdateFromAlphaFunc(pendulum, update_pendulum), run_time=2, rate_func=linear)
                self.wait(0.5)

                # Two Pendulums
                pendulum2_length = 5
                bob2_initial_position = pivot_point + np.array([pendulum2_length * np.sin(PI / 4), -pendulum2_length * np.cos(PI / 4), 0])

                line2 = Line(pivot_point, bob2_initial_position, color=WHITE)
                bob2 = Circle(radius=bob_radius, color=BLUE, fill_opacity=1).move_to(bob2_initial_position)
                pendulum2 = VGroup(line2, bob2).move_to(self.right_region.get_center()).shift(RIGHT * 3)
                pendulum.shift(LEFT * 3)

                def update_pendulum2(obj, alpha):
                    angle = PI / 4 * np.sin(alpha * TAU * np.sqrt(pendulum_length/pendulum2_length))
                    new_bob_position = pivot_point + np.array([pendulum2_length * np.sin(angle), -pendulum2_length * np.cos(angle), 0])
                    obj[0].become(Line(pivot_point, new_bob_position, color=WHITE))
                    obj[1].move_to(new_bob_position)

                self.play(
                    Create(pendulum2),
                    TransformMatchingShapes(pendulum, pendulum.copy().set_opacity(0.5)),
                    TransformMatchingShapes(timer, timer.copy().set_opacity(0.5)),
                    run_time=0.5
                )

                self.play(UpdateFromAlphaFunc(pendulum, update_pendulum), UpdateFromAlphaFunc(pendulum2, update_pendulum2), run_time=4, rate_func=linear)
                self.wait(1)

                length_label = Text("Length").scale(0.6).next_to(pendulum, UP)
                gravity_label = Text("Gravity").scale(0.6).next_to(pendulum, DOWN)

                self.play(Write(length_label), Write(gravity_label))
                self.wait(2)

# Set narration and duration
Scene3.narration_text = '''The time it takes for one complete swing, from one side to the other and back again, is called the period. The period of a simple pendulum depends primarily on two things: the length of the pendulum and the acceleration due to gravity.'''
Scene3.audio_duration = 5.0
