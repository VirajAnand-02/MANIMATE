import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Text-to-Audio Generation", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())

        self.play(Write(title_text))
        self.wait(1)

        # Sound waves emanating from text
        sound_waves = VGroup(*[
        Circle(radius=0.5 + i * 0.2, color=BLUE, stroke_width=2, fill_opacity=0)
        for i in range(5)
        ])
        sound_waves.move_to(title_text.get_center()).shift(DOWN * 1.5)

        self.play(*[Create(wave) for wave in sound_waves])
        self.wait(0.5)
        self.play(*[FadeOut(wave) for wave in sound_waves])

        # Montage of applications
        voice_assistant = ImageMobject("voice_assistant.png").scale(0.7)
        music = ImageMobject("music.png").scale(0.7)
        audiobook = ImageMobject("audiobook.png").scale(0.7)

        voice_assistant.move_to(self.main_region.get_center()).shift(LEFT * 3)
        music.move_to(self.main_region.get_center())
        audiobook.move_to(self.main_region.get_center()).shift(RIGHT * 3)

        self.play(FadeIn(voice_assistant), FadeIn(music), FadeIn(audiobook))
        self.wait(2)

        self.play(FadeOut(voice_assistant), FadeOut(music), FadeOut(audiobook))
        self.play(FadeOut(title_text))
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome! Have you ever wondered how computers can \'speak\' or create music from just text? We\'re diving into the fascinating world of Text-to-Audio generation! We\'ll explore what it is, how it works, and its amazing applications.'''
Scene1.audio_duration = 5.0
