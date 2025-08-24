import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Matrix Multiplication", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())

        self.play(Write(title_text))
        self.wait(1)

        # Example applications (replace with actual visuals if possible)
        graphics_example = Text("Computer Graphics Rendering")
        data_example = Text("Data Analysis Visualization")

        graphics_example.move_to(self.main_region.get_center())
        data_example.move_to(self.main_region.get_center())

        self.play(FadeIn(graphics_example))
        self.wait(0.5)
        self.play(FadeOut(graphics_example))

        self.play(FadeIn(data_example))
        self.wait(0.5)
        self.play(FadeOut(data_example))

        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome! Today, we\'re diving into matrix multiplication. It might seem intimidating, but we\'ll break it down step-by-step. Get ready to unlock a powerful tool used in computer graphics, data science, and more!'''
Scene1.audio_duration = 5.0
