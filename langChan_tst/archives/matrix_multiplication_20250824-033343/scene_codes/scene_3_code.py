import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene3(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Matrix Multiplication", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        matrix_a = Matrix([[1, 2], [3, 4]])
        matrix_b = Matrix([[5, 6], [7, 8]])
        result_matrix = Matrix([[0, 0], [0, 0]])

        matrix_a.move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b.move_to(self.main_region.get_center() + RIGHT * 3)
        result_matrix.move_to(self.main_region.get_center())

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(0.5)

        # Highlight row 1 of A and column 1 of B
        row_a = matrix_a.get_rows()[0]
        col_b = matrix_b.get_columns()[0]
        rect_a = SurroundingRectangle(row_a, color=YELLOW)
        rect_b = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(0.5)

        # Multiply and sum
        num1 = matrix_a.entries[0][0].copy()
        num2 = matrix_b.entries[0][0].copy()
        num3 = matrix_a.entries[0][1].copy()
        num4 = matrix_b.entries[1][0].copy()

        num1.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 1)
        num2.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.5)
        num3.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.5)
        num4.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 1)

        self.play(
        Transform(matrix_a.entries[0][0].copy(), num1),
        Transform(matrix_b.entries[0][0].copy(), num2),
        Transform(matrix_a.entries[0][1].copy(), num3),
        Transform(matrix_b.entries[1][0].copy(), num4)
        )
        self.wait(0.5)

        times1 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.75)
        times2 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.75)
        plus = MathTex("+").move_to(self.main_region.get_center() + DOWN * 2)

        self.play(Write(times1), Write(times2), Write(plus))
        self.wait(0.5)

        result = 1 * 5 + 2 * 7
        result_text = MathTex(str(result)).move_to(result_matrix.entries[0][0].get_center())

        self.play(Transform(VGroup(num1, num2, num3, num4, times1, times2, plus), result_text))
        self.wait(0.5)
        self.play(Transform(result_text, result_matrix.entries[0][0]))
        self.wait(0.5)

        result_matrix.entries[0][0].become(result_text)
        self.play(FadeOut(rect_a), FadeOut(rect_b))
        self.wait(1)

        # Highlight row 1 of A and column 2 of B
        row_a = matrix_a.get_rows()[0]
        col_b = matrix_b.get_columns()[1]
        rect_a = SurroundingRectangle(row_a, color=YELLOW)
        rect_b = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(0.5)

        # Multiply and sum
        num1 = matrix_a.entries[0][0].copy()
        num2 = matrix_b.entries[0][1].copy()
        num3 = matrix_a.entries[0][1].copy()
        num4 = matrix_b.entries[1][1].copy()

        num1.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 1)
        num2.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.5)
        num3.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.5)
        num4.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 1)

        self.play(
        Transform(matrix_a.entries[0][0].copy(), num1),
        Transform(matrix_b.entries[0][1].copy(), num2),
        Transform(matrix_a.entries[0][1].copy(), num3),
        Transform(matrix_b.entries[1][1].copy(), num4)
        )
        self.wait(0.5)

        times1 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.75)
        times2 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.75)
        plus = MathTex("+").move_to(self.main_region.get_center() + DOWN * 2)

        self.play(Write(times1), Write(times2), Write(plus))
        self.wait(0.5)

        result = 1 * 6 + 2 * 8
        result_text = MathTex(str(result)).move_to(result_matrix.entries[0][1].get_center())

        self.play(Transform(VGroup(num1, num2, num3, num4, times1, times2, plus), result_text))
        self.wait(0.5)
        self.play(Transform(result_text, result_matrix.entries[0][1]))
        self.wait(0.5)

        result_matrix.entries[0][1].become(result_text)
        self.play(FadeOut(rect_a), FadeOut(rect_b))
        self.wait(1)

        # Highlight row 2 of A and column 1 of B
        row_a = matrix_a.get_rows()[1]
        col_b = matrix_b.get_columns()[0]
        rect_a = SurroundingRectangle(row_a, color=YELLOW)
        rect_b = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(0.5)

        # Multiply and sum
        num1 = matrix_a.entries[1][0].copy()
        num2 = matrix_b.entries[0][0].copy()
        num3 = matrix_a.entries[1][1].copy()
        num4 = matrix_b.entries[1][0].copy()

        num1.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 1)
        num2.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.5)
        num3.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.5)
        num4.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 1)

        self.play(
        Transform(matrix_a.entries[1][0].copy(), num1),
        Transform(matrix_b.entries[0][0].copy(), num2),
        Transform(matrix_a.entries[1][1].copy(), num3),
        Transform(matrix_b.entries[1][0].copy(), num4)
        )
        self.wait(0.5)

        times1 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.75)
        times2 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.75)
        plus = MathTex("+").move_to(self.main_region.get_center() + DOWN * 2)

        self.play(Write(times1), Write(times2), Write(plus))
        self.wait(0.5)

        result = 3 * 5 + 4 * 7
        result_text = MathTex(str(result)).move_to(result_matrix.entries[1][0].get_center())

        self.play(Transform(VGroup(num1, num2, num3, num4, times1, times2, plus), result_text))
        self.wait(0.5)
        self.play(Transform(result_text, result_matrix.entries[1][0]))
        self.wait(0.5)

        result_matrix.entries[1][0].become(result_text)
        self.play(FadeOut(rect_a), FadeOut(rect_b))
        self.wait(1)

        # Highlight row 2 of A and column 2 of B
        row_a = matrix_a.get_rows()[1]
        col_b = matrix_b.get_columns()[1]
        rect_a = SurroundingRectangle(row_a, color=YELLOW)
        rect_b = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(0.5)

        # Multiply and sum
        num1 = matrix_a.entries[1][0].copy()
        num2 = matrix_b.entries[0][1].copy()
        num3 = matrix_a.entries[1][1].copy()
        num4 = matrix_b.entries[1][1].copy()

        num1.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 1)
        num2.move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.5)
        num3.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.5)
        num4.move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 1)

        self.play(
        Transform(matrix_a.entries[1][0].copy(), num1),
        Transform(matrix_b.entries[0][1].copy(), num2),
        Transform(matrix_a.entries[1][1].copy(), num3),
        Transform(matrix_b.entries[1][1].copy(), num4)
        )
        self.wait(0.5)

        times1 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 0.75)
        times2 = MathTex("\\times").move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 0.75)
        plus = MathTex("+").move_to(self.main_region.get_center() + DOWN * 2)

        self.play(Write(times1), Write(times2), Write(plus))
        self.wait(0.5)

        result = 3 * 6 + 4 * 8
        result_text = MathTex(str(result)).move_to(result_matrix.entries[1][1].get_center())

        self.play(Transform(VGroup(num1, num2, num3, num4, times1, times2, plus), result_text))
        self.wait(0.5)
        self.play(Transform(result_text, result_matrix.entries[1][1]))
        self.wait(0.5)

        result_matrix.entries[1][1].become(result_text)
        self.play(FadeOut(rect_a), FadeOut(rect_b))
        self.wait(1)

        self.play(Transform(matrix_a, matrix_b))
        self.play(Transform(matrix_b, result_matrix))
        self.wait(1)

# Set narration and duration
Scene3.narration_text = '''Each element in the resulting matrix is calculated by taking the dot product of a row from the first matrix and a column from the second matrix. Let\'s see that in action!'''
Scene3.audio_duration = 5.0
