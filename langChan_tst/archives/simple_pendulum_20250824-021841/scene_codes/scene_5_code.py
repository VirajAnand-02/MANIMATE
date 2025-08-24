import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Pendulums in Action", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Grandfather Clock
        clock_text = Text("Grandfather Clock", font_size=24)
        clock = Rectangle(width=2, height=4)
        pendulum = Line(clock.get_center(), clock.get_center() + DOWN * 1.5)
        bob = Dot(pendulum.get_end(), radius=0.15)
        clock_group = VGroup(clock, pendulum, bob, clock_text).scale(0.5)
        clock_group.move_to(self.main_region.get_center() + LEFT * 3)
        clock_text.next_to(clock, UP)
        self.play(Create(clock_group))

        # Metronome
        metronome_text = Text("Metronome", font_size=24)
        metronome = Triangle(color=BLUE, fill_opacity=0.5)
        arm = Line(metronome.get_center(), metronome.get_center() + UP * 1.5)
        metronome_group = VGroup(metronome, arm, metronome_text).scale(0.5)
        metronome_group.move_to(self.main_region.get_center())
        metronome_text.next_to(metronome, UP)
        self.play(Create(metronome_group))

        # Seismometer
        seismometer_text = Text("Seismometer", font_size=24)
        base = Rectangle(width=3, height=0.5)
        support = Line(base.get_center() + UP * 0.25, base.get_center() + UP * 2)
        pen = Dot(support.get_end(), radius=0.1)
        paper = Rectangle(width=4, height=2).next_to(base, DOWN)
        seismometer_group = VGroup(base, support, pen, paper, seismometer_text).scale(0.5)
        seismometer_group.move_to(self.main_region.get_center() + RIGHT * 3)
        seismometer_text.next_to(support, UP)
        self.play(Create(seismometer_group))

        self.wait(2)

        # End Screen
        end_text = Text("Learn More:", font_size=36)
        link1 = Text("Wikipedia: Simple Pendulum", font_size=24)
        link2 = Text("MIT Physics Lectures", font_size=24)
        end_group = VGroup(end_text, link1, link2).arrange(DOWN)
        end_group.move_to(self.main_region.get_center())

        self.play(FadeOut(clock_group, metronome_group, seismometer_group))
        self.play(Write(end_group))
        self.wait(3)

# Set narration and duration
Scene5.narration_text = '''The simple pendulum is a powerful tool for understanding fundamental physics concepts like simple harmonic motion, gravity, and energy conservation. While real-world pendulums might have some friction or air resistance, the simple pendulum model provides a valuable approximation for many situations. Thanks for joining us on this swinging adventure!'''
Scene5.audio_duration = 5.0
