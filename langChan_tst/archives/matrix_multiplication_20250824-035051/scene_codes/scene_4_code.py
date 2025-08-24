import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication - Row by Column", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(1)

        matrix_a_data = [[1, 2, 3], [4, 5, 6]]
        matrix_b_data = [[7, 8], [9, 10], [11, 12]]

        matrix_a = Matrix(matrix_a_data)
        matrix_b = Matrix(matrix_b_data)

        matrix_a.move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b.move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(1)

        # Highlight first row of A and second column of B
        row_a = matrix_a.get_rows()[0]
        col_b = matrix_b.get_columns()[1]

        rect_a = SurroundingRectangle(row_a, color=YELLOW)
        rect_b = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(1)

        # Show calculation
        calculation = MathTex("1*8 + 2*10 + 3*12 = 64").move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Write(calculation))
        self.wait(1)

        # Resulting matrix C
        matrix_c_data = [["64", ""], ["", ""]]
        matrix_c = Matrix(matrix_c_data)
        matrix_c.move_to(self.main_region.get_center())

        self.play(FadeOut(rect_a), FadeOut(rect_b), FadeOut(calculation))
        self.play(Transform(VGroup(matrix_a, matrix_b), matrix_c))
        self.wait(1)

        # Repeat for second row of A
        row_a = matrix_a.get_rows()[1]  # Accessing rows from the original matrix_a
        rect_a = SurroundingRectangle(row_a, color=YELLOW)

        self.play(FadeOut(matrix_c)) # Fade out C to reveal A and B again
        self.play(Write(matrix_a), Write(matrix_b)) # Rewrite A and B

        row_a = matrix_a.get_rows()[1]
        col_b = matrix_b.get_columns()[1]

        rect_a = SurroundingRectangle(row_a, color=YELLOW)
        rect_b = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(1)

        calculation = MathTex("4*8 + 5*10 + 6*12 = 144").move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Write(calculation))
        self.wait(1)

        matrix_c_data = [["", ""], ["", "144"]]
        matrix_c = Matrix(matrix_c_data)
        matrix_c.move_to(self.main_region.get_center())

        self.play(FadeOut(rect_a), FadeOut(rect_b), FadeOut(calculation))
        self.play(Transform(VGroup(matrix_a, matrix_b), matrix_c))
        self.wait(1)

# Set narration and duration
Scene4.narration_text = '''We repeat this process for each row of the first matrix and each column of the second matrix. So, for the first row of the first matrix and the second column of the second matrix, we multiply and add again. This gives us the element in the first row, second column of the resulting matrix.'''
Scene4.audio_duration = 5.0
