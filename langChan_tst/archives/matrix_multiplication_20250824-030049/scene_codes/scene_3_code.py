import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene3(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Matrix Multiplication Mechanics", width=6, height=1)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Matrices A and B
        matrix_a = MathTex(r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}")
        matrix_b = MathTex(r"\begin{bmatrix} e & f \\ g & h \end{bmatrix}")
        matrix_c = MathTex(r"\begin{bmatrix} ae+bg & af+bh \\ ce+dg & cf+dh \end{bmatrix}")

        matrix_a.move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b.move_to(self.main_region.get_center() + RIGHT * 3)
        matrix_c.move_to(self.main_region.get_center() + DOWN * 2)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(1)

        # Highlight row and column
        row_a = SurroundingRectangle(matrix_a[0][0:2], color=YELLOW)
        col_b = SurroundingRectangle(matrix_b[0][::2], color=YELLOW)

        self.play(Create(row_a), Create(col_b))
        self.wait(1)

        # Element-wise multiplication and summation
        calculation = MathTex(r"(a \times e) + (b \times g) = ae + bg")
        calculation.move_to(self.main_region.get_center() + UP * 2)

        self.play(Write(calculation))
        self.wait(2)

        self.play(FadeOut(row_a), FadeOut(col_b), FadeOut(calculation))
        self.wait(1)

        self.play(Write(matrix_c))
        self.wait(2)

# Set narration and duration
Scene3.narration_text = '''Now, for the mechanics. Each element in the resulting matrix C is calculated as the dot product of a row from matrix A and a column from matrix B. Let\'s break down how to compute one specific element.'''
Scene3.audio_duration = 5.0
