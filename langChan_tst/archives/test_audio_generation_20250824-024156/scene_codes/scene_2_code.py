import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Left side: Text to Speech
        text_tta = Text("Text-to-Audio (TTA)", font_size=36)
        text_tta.move_to(self.left_region.get_center() + UP * 3)

        text_input = Text("Hello, Manim!", font_size=24)
        text_input.move_to(self.left_region.get_center() + UP * 1.5)

        waveform = VGroup(*[
        Line(start=DOWN * np.random.rand() * 0.5, end=UP * np.random.rand() * 0.5).set_stroke(width=2)
        for _ in range(50)
        ]).arrange(RIGHT, buff=0.1)
        waveform.move_to(self.left_region.get_center() + DOWN * 0.5)

        avatars = VGroup(*[
        Circle(radius=0.3, color=color).shift(np.random.normal(0, 0.5) * RIGHT + np.random.normal(0, 0.5) * UP)
        for color in [RED, GREEN, BLUE, YELLOW]
        ]).arrange(RIGHT, buff=0.5)
        avatars.move_to(self.left_region.get_center() + DOWN * 2)

        # Right side: Text to Music
        text_ttm = Text("Text-to-Music (TTM)", font_size=36)
        text_ttm.move_to(self.right_region.get_center() + UP * 3)

        text_instruction = Text("Create a happy tune", font_size=24)
        text_instruction.move_to(self.right_region.get_center() + UP * 1.5)

        musical_score = VGroup(*[
        Dot(point=np.random.rand(2) * 2 - 1, radius=0.05).set_color(color)
        for color in [RED, GREEN, BLUE, YELLOW] for _ in range(10)
        ]).arrange_in_grid(rows=2, buff=(0.5, 1))
        musical_score.move_to(self.right_region.get_center() + DOWN * 0.5)

        self.play(Write(text_tta), Write(text_ttm))
        self.wait(0.5)
        self.play(Write(text_input), Write(text_instruction))
        self.wait(0.5)
        self.play(Transform(text_input, waveform), run_time=2)
        self.play(Transform(text_instruction, musical_score), run_time=2)
        self.wait(0.5)
        self.play(Create(avatars), run_time=2)
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''Text-to-Audio, or TTA, is a technology that converts written text into audible sound. It\'s not just about robotic voices anymore! Modern TTA can create realistic speech with different accents, emotions, and even generate music in various styles. The key is advanced AI models.'''
Scene2.audio_duration = 5.0
