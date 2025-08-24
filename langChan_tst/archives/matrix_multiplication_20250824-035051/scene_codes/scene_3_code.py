import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene3(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication", width=self.title_region.width, height=self.title_region.height)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(1)

        matrix_a = MathTex(r"\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}").move_to(LEFT * 3)
        matrix_b = MathTex(r"\begin{bmatrix} 7 & 8 \\ 9 & 10 \\ 11 & 12 \end{bmatrix}").move_to(RIGHT * 3)
        matrix_c = MathTex(r"\begin{bmatrix} 58 & ? \\ ? & ? \end{bmatrix}").move_to(DOWN * 2)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(1)

        rect_a = SurroundingRectangle(matrix_a[0][0:3])
        rect_b = SurroundingRectangle(matrix_b[0][0::2])

        self.play(Create(rect_a), Create(rect_b))
        self.wait(1)

        equation = MathTex(r"1 \times 7 + 2 \times 9 + 3 \times 11 = 58").move_to(UP * 2)
        self.play(Write(equation))
        self.wait(2)

        self.play(Transform(equation, matrix_c[0][0]))
        self.wait(1)

        self.play(FadeOut(rect_a), FadeOut(rect_b), FadeOut(equation))
        self.wait(1)

# Set narration and duration
Scene3.narration_text = '''Let\'s see how it works! We take the first row of the first matrix and the first column of the second matrix. We multiply corresponding elements and then add the results. This gives us the element in the first row and first column of the resulting matrix.'''
Scene3.audio_duration = 5.0
