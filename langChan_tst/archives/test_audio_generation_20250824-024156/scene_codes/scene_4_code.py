import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene4(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Vast Applications", width=6, height=1)
        title.move_to(self.title_region.get_center())

        speaker = ImageMobject("speaker.png")
        audiobook = ImageMobject("audiobook.png")
        game_char = ImageMobject("game_character.png")
        assistive_tech = ImageMobject("assistive_tech.png")

        speaker_text = Text("Voice Assistants", font_size=24)
        audiobook_text = Text("Audiobooks", font_size=24)
        game_char_text = Text("Game Characters", font_size=24)
        assistive_tech_text = Text("Assistive Tech", font_size=24)

        speaker.move_to(self.left_region.get_center() + UP * 1.5)
        audiobook.move_to(self.right_region.get_center() + UP * 1.5)
        game_char.move_to(self.left_region.get_center() + DOWN * 1.5)
        assistive_tech.move_to(self.right_region.get_center() + DOWN * 1.5)

        speaker_text.next_to(speaker, DOWN)
        audiobook_text.next_to(audiobook, DOWN)
        game_char_text.next_to(game_char, DOWN)
        assistive_tech_text.next_to(assistive_tech, DOWN)

        self.play(Write(title))
        self.wait(0.5)

        self.play(FadeIn(speaker), Write(speaker_text))
        self.wait(1)
        self.play(FadeOut(speaker), FadeOut(speaker_text))

        self.play(FadeIn(audiobook), Write(audiobook_text))
        self.wait(1)
        self.play(FadeOut(audiobook), FadeOut(audiobook_text))

        self.play(FadeIn(game_char), Write(game_char_text))
        self.wait(1)
        self.play(FadeOut(game_char), FadeOut(game_char_text))

        self.play(FadeIn(assistive_tech), Write(assistive_tech_text))
        self.wait(1)
        self.play(FadeOut(assistive_tech), FadeOut(assistive_tech_text))

        self.wait(0.5)
        self.play(FadeOut(title))

# Set narration and duration
Scene4.narration_text = '''The applications are vast! Think of voice assistants like Siri or Alexa, audiobooks, creating personalized learning experiences, assisting people with disabilities, and even generating soundtracks for videos or games. The possibilities are constantly expanding!'''
Scene4.audio_duration = 5.0
