import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Mastering Matrix Multiplication", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())

        matrix_lines = VGroup()
        for i in range(4):
        line = Line(start=np.array([-3, i - 1.5, 0]), end=np.array([3, i - 1.5, 0]))
        matrix_lines.add(line)
        for i in range(4):
        line = Line(start=np.array([i - 1.5, -3, 0]), end=np.array([i - 1.5, 3, 0]))
        matrix_lines.add(line)

        matrix_lines.set_color(BLUE)
        matrix_lines.move_to(self.main_region.get_center())

        self.play(Create(matrix_lines), Write(title_text), run_time=3)
        self.wait(1)

        # Example applications (brief flashes)
        image_recognition = Text("Image Recognition", font_size=36)
        image_recognition.move_to(self.main_region.get_center())
        rendering_3d = Text("3D Rendering", font_size=36)
        rendering_3d.move_to(self.main_region.get_center())
        data_science = Text("Data Science", font_size=36)
        data_science.move_to(self.main_region.get_center())

        self.play(FadeIn(image_recognition), run_time=0.5)
        self.play(FadeOut(image_recognition), run_time=0.5)
        self.play(FadeIn(rendering_3d), run_time=0.5)
        self.play(FadeOut(rendering_3d), run_time=0.5)
        self.play(FadeIn(data_science), run_time=0.5)
        self.play(FadeOut(data_science), run_time=0.5)

        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome! Today, we\'ll unravel the mystery of matrix multiplication. It\'s a fundamental operation in linear algebra with applications in computer graphics, data science, and much more. Get ready to level up your math skills!'''
Scene1.audio_duration = 5.0
