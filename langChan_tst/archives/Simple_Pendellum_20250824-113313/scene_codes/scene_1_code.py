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
        title_text = self.create_textbox("The Simple Pendulum", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Pendulum animation
        fixed_point = Dot(point=[0, 2, 0], color=RED)
        string = Line(start=fixed_point.get_center(), end=[0, 0, 0], color=BLUE)
        bob = Dot(point=[0, 0, 0], color=GREEN)

        fixed_point_label = Tex("Fixed Point").next_to(fixed_point, UP)
        string_label = Tex("String").next_to(string, LEFT)
        bob_label = Tex("Bob").next_to(bob, DOWN)

        pendulum = VGroup(fixed_point, string, bob, fixed_point_label, string_label, bob_label)
        pendulum.move_to(self.main_region.get_center())

        self.play(Create(fixed_point), Write(fixed_point_label))
        self.play(Create(string), Write(string_label))
        self.play(Create(bob), Write(bob_label))
        self.wait(1)

        # Swing animation
        angle = 0.5  # Radians
        swing_duration = 2

        def update_pendulum(mob, alpha):
        new_bob_x = np.sin(angle * np.sin(alpha * PI - PI/2)) * 2
        new_bob_y = -np.cos(angle * np.sin(alpha * PI - PI/2)) * 2
        new_bob_pos = np.array([new_bob_x, new_bob_y, 0])

        new_string = Line(start=fixed_point.get_center(), end=fixed_point.get_center() + new_bob_pos, color=BLUE)
        new_bob = Dot(point=fixed_point.get_center() + new_bob_pos, color=GREEN)

        mob[1].become(new_string) #string
        mob[2].become(new_bob) #bob

        self.play(UpdateFromAlphaFunc(pendulum, update_pendulum), run_time=swing_duration, rate_func=linear)
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to the fascinating world of the Simple Pendulum! At its core, a simple pendulum is just a point mass, often called a \'bob,\' suspended from a fixed point by a light, inextensible string. When displaced from its resting position and released, it swings back and forth, exhibiting what we call periodic motion. This simple setup has profound implications for understanding fundamental physics.'''
Scene1.audio_duration = 5.0
