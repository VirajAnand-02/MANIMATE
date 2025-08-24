import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Understanding the Simple Pendulum", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Pendulum animation
        pivot = Dot(self.main_region.get_center() + UP * 2)
        length = 2
        bob_radius = 0.2
        bob = Circle(radius=bob_radius, color=BLUE, fill_opacity=1)
        string = Line(pivot.get_center(), pivot.get_center() + DOWN * length, color=WHITE)

        def get_bob_position(angle):
        return pivot.get_center() + length * np.array([np.sin(angle), -np.cos(angle), 0])

        bob.move_to(get_bob_position(PI / 4))
        string.become(Line(pivot.get_center(), bob.get_center(), color=WHITE))

        def update_bob(mob, angle):
        mob.move_to(get_bob_position(angle))

        def update_string(mob, angle):
        mob.become(Line(pivot.get_center(), get_bob_position(angle), color=WHITE))

        bob.add_updater(update_bob)
        string.add_updater(update_string)

        self.add(pivot, string, bob)

        amplitude = PI / 4
        swing_duration = 2
        num_swings = 2

        def swing(angle):
        return amplitude * np.sin(angle)

        for i in range(num_swings):
        self.play(
        UpdateFromFunc(bob, lambda mob: update_bob(mob, swing(TAU * self.renderer.time / swing_duration))),
        UpdateFromFunc(string, lambda mob: update_string(mob, swing(TAU * self.renderer.time / swing_duration))),
        run_time=swing_duration
        )

        bob.remove_updater(update_bob)
        string.remove_updater(update_string)

        self.wait(2)

# Set narration and duration
Scene1.narration_text = '''Hello and welcome! Today, we\'re diving into the fascinating world of physics to explore a fundamental concept: the simple pendulum. We\'ll uncover what it is, how it works, and some of the key factors that influence its behavior. Get ready for a swinging good time!'''
Scene1.audio_duration = 5.0
