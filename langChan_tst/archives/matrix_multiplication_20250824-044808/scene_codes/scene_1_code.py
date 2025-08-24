import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Matrix Multiplication: The Basics", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Create Matrix A
        matrix_a = MathTex(r"A", font_size=48)
        dims_a = MathTex(r"m \times n", font_size=36)
        matrix_a.move_to(self.main_region.get_center() + LEFT * 3)
        dims_a.next_to(matrix_a, DOWN)

        # Create Matrix B
        matrix_b = MathTex(r"B", font_size=48)
        dims_b = MathTex(r"n \times p", font_size=36)
        matrix_b.move_to(self.main_region.get_center() + RIGHT * 3)
        dims_b.next_to(matrix_b, DOWN)

        # Create Matrix C
        matrix_c = MathTex(r"C", font_size=48)
        dims_c = MathTex(r"m \times p", font_size=36)
        matrix_c.move_to(self.main_region.get_center() + DOWN * 2)
        dims_c.next_to(matrix_c, DOWN)

        self.play(Write(matrix_a), Write(dims_a), Write(matrix_b), Write(dims_b))
        self.wait(0.5)

        # Create arrow
        arrow = Arrow(matrix_a.get_right(), matrix_b.get_left(), buff=0.5)
        self.play(Create(arrow))
        self.wait(0.5)

        # Highlight the 'n's
        n_a = dims_a[0][2]
        n_b = dims_b[0][0]
        self.play(Indicate(n_a), Indicate(n_b))
        self.wait(1)

        self.play(FadeOut(arrow))
        self.play(Write(matrix_c), Write(dims_c))
        self.wait(2)

# Set narration and duration
Scene1.narration_text = '''Welcome to our deep dive into matrix multiplication! Unlike simple scalar multiplication, multiplying two matrices is a bit more involved, but incredibly powerful for tasks like 3D graphics, data transformations, and solving complex systems of equations. Before we jump into the \'how,\' there\'s a crucial \'if.\' You can only multiply two matrices if the number of columns in the first matrix equals the number of rows in the second matrix. Think of it like a puzzle piece fitting together. If Matrix A is an \'m by n\' matrix, and Matrix B is an \'n by p\' matrix, then their product, Matrix C, will be an \'m by p\' matrix. The \'n\'s must match!'''
Scene1.audio_duration = 5.0
