import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene3(SplitScreen):
    def construct_scene(self):
        # Title Text
        title_text = self.create_textbox("Pendulum Period", width=self.left_region.width, height=self.left_region.height/4)
        title_text.move_to(self.left_region.get_center() + UP * self.left_region.height/3)
        self.add(title_text)

        description_text = self.create_textbox(
        "The period of a pendulum, represented by 'T', is the time it takes for one complete swing – from one extreme position back to the same extreme position. A key factor influencing the period is the length of the pendulum, 'L'. Longer pendulums have longer periods. Another crucial factor is the acceleration due to gravity, 'g'.",
        width=self.left_region.width * 0.9,
        height=self.left_region.height * 0.6
        )
        description_text.move_to(self.left_region.get_center() + DOWN * self.left_region.height/6)
        self.add(description_text)

        # Pendulums
        l1 = 2  # Short pendulum length
        l2 = 4  # Long pendulum length
        g = 9.81
        theta = PI / 4

        def pendulum_pos(length, angle):
        return [length * np.sin(angle), -length * np.cos(angle), 0]

        # Short Pendulum
        p1_pivot = np.array([-3, 1, 0])
        p1_bob_pos = p1_pivot + pendulum_pos(l1, theta)
        p1_string = Line(p1_pivot, p1_bob_pos)
        p1_bob = Dot(p1_bob_pos, radius=0.2)
        p1 = VGroup(p1_string, p1_bob)

        # Long Pendulum
        p2_pivot = np.array([3, 1, 0])
        p2_bob_pos = p2_pivot + pendulum_pos(l2, theta)
        p2_string = Line(p2_pivot, p2_bob_pos)
        p2_bob = Dot(p2_bob_pos, radius=0.2)
        p2 = VGroup(p2_string, p2_bob)

        p1.move_to(self.right_region.get_center())
        p2.move_to(self.right_region.get_center())

        self.add(p1, p2)

        # Animation
        def update_pendulum(pendulum, length, time, pivot):
        angle = theta * np.cos(np.sqrt(g / length) * time)
        bob_pos = pivot + pendulum_pos(length, angle)
        pendulum[0].become(Line(pivot, bob_pos))
        pendulum[1].move_to(bob_pos)

        p1.add_updater(lambda m, dt: update_pendulum(m, l1, self.time, p1_pivot))
        p2.add_updater(lambda m, dt: update_pendulum(m, l2, self.time, p2_pivot))

        # Formula
        formula = MathTex(r"T = 2\pi\sqrt{\frac{L}{g}}")
        formula.move_to(self.right_region.get_center() + DOWN * 2)
        L_in_formula = formula[0][5]
        g_in_formula = formula[0][7]
        L_in_formula.set_color(YELLOW)
        g_in_formula.set_color(GREEN)

        self.add(formula)

        self.wait(5)

        p1.remove_updater(lambda m, dt: update_pendulum(m, l1, self.time, p1_pivot))
        p2.remove_updater(lambda m, dt: update_pendulum(m, l2, self.time, p2_pivot))

# Set narration and duration
Scene3.narration_text = '''The period of a pendulum, represented by \'T\', is the time it takes for one complete swing – from one extreme position back to the same extreme position. A key factor influencing the period is the length of the pendulum, \'L\'. Longer pendulums have longer periods. Another crucial factor is the acceleration due to gravity, \'g\'.'''
Scene3.audio_duration = 5.0
