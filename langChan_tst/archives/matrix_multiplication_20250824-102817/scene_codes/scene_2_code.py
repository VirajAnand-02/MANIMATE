import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication: Row by Column", width=self.left_region.width, height=self.title_region.height)
        title.move_to(self.title_region.get_center())

        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]

        matrix_a = Matrix(matrix_a_data)
        matrix_b = Matrix(matrix_b_data)
        result_matrix = Matrix([[" ", " "], [" ", " "]])

        matrix_a.move_to(self.left_region.get_center()).shift(UP * 1.5)
        matrix_b.move_to(self.right_region.get_center()).shift(UP * 1.5)
        result_matrix.move_to(self.left_region.get_center()).shift(DOWN * 1.5)

        self.play(Write(matrix_a), Write(matrix_b), Write(result_matrix))
        self.wait(1)

        # First element calculation (row 1 of A, column 1 of B)
        row_a = matrix_a.get_rows()[0]
        col_b = matrix_b.get_columns()[0]

        row_a_highlight = SurroundingRectangle(row_a, color=YELLOW)
        col_b_highlight = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(row_a_highlight), Create(col_b_highlight))
        self.wait(1)

        row_a_copy = row_a.copy().move_to(ORIGIN)
        col_b_copy = col_b.copy().move_to(ORIGIN)

        self.play(
        row_a.animate.move_to(LEFT * 3 + DOWN * 2),
        col_b.animate.move_to(RIGHT * 3 + DOWN * 2),
        row_a_highlight.animate.move_to(LEFT * 3 + DOWN * 2),
        col_b_highlight.animate.move_to(RIGHT * 3 + DOWN * 2),
        )
        self.wait(1)

        element_1_a = row_a_copy[0]
        element_1_b = col_b_copy[0]
        element_2_a = row_a_copy[1]
        element_2_b = col_b_copy[1]

        element_1_a_highlight = SurroundingRectangle(element_1_a, color=GREEN)
        element_1_b_highlight = SurroundingRectangle(element_1_b, color=GREEN)
        element_2_a_highlight = SurroundingRectangle(element_2_a, color=GREEN)
        element_2_b_highlight = SurroundingRectangle(element_2_b, color=GREEN)

        self.play(Create(element_1_a_highlight), Create(element_1_b_highlight))
        self.wait(0.5)
        product_1 = MathTex(f"{matrix_a_data[0][0]}*{matrix_b_data[0][0]}").move_to(DOWN * 3)
        self.play(Write(product_1))
        self.wait(0.5)
        self.play(FadeOut(element_1_a_highlight), FadeOut(element_1_b_highlight))

        self.play(Create(element_2_a_highlight), Create(element_2_b_highlight))
        self.wait(0.5)
        product_2 = MathTex(f"+{matrix_a_data[0][1]}*{matrix_b_data[1][0]}").next_to(product_1, RIGHT)
        self.play(Write(product_2))
        self.wait(0.5)
        self.play(FadeOut(element_2_a_highlight), FadeOut(element_2_b_highlight))

        sum_result = matrix_a_data[0][0] * matrix_b_data[0][0] + matrix_a_data[0][1] * matrix_b_data[1][0]
        sum_text = MathTex(f"={sum_result}").next_to(product_2, RIGHT)
        self.play(Write(sum_text))
        self.wait(0.5)

        result_element = result_matrix.get_entries()[0]
        sum_result_mob = MathTex(str(sum_result)).move_to(result_element.get_center())
        self.play(Transform(VGroup(product_1, product_2, sum_text), sum_result_mob))
        self.play(Transform(VGroup(sum_result_mob), result_element))
        self.wait(1)

        self.play(
        row_a.animate.move_to(self.left_region.get_center()).shift(UP * 1.5),
        col_b.animate.move_to(self.right_region.get_center()).shift(UP * 1.5),
        row_a_highlight.animate.move_to(self.left_region.get_center()).shift(UP * 1.5),
        col_b_highlight.animate.move_to(self.right_region.get_center()).shift(UP * 1.5),
        FadeOut(row_a_copy),
        FadeOut(col_b_copy),
        )
        self.wait(1)

        # Second element calculation (row 2 of A, column 2 of B)
        row_a = matrix_a.get_rows()[1]
        col_b = matrix_b.get_columns()[1]

        row_a_highlight = SurroundingRectangle(row_a, color=YELLOW)
        col_b_highlight = SurroundingRectangle(col_b, color=YELLOW)

        self.play(Create(row_a_highlight), Create(col_b_highlight))
        self.wait(1)

        row_a_copy = row_a.copy().move_to(ORIGIN)
        col_b_copy = col_b.copy().move_to(ORIGIN)

        self.play(
        row_a.animate.move_to(LEFT * 3 + DOWN * 2),
        col_b.animate.move_to(RIGHT * 3 + DOWN * 2),
        row_a_highlight.animate.move_to(LEFT * 3 + DOWN * 2),
        col_b_highlight.animate.move_to(RIGHT * 3 + DOWN * 2),
        )
        self.wait(1)

        element_1_a = row_a_copy[0]
        element_1_b = col_b_copy[0]
        element_2_a = row_a_copy[1]
        element_2_b = col_b_copy[1]

        element_1_a_highlight = SurroundingRectangle(element_1_a, color=GREEN)
        element_1_b_highlight = SurroundingRectangle(element_1_b, color=GREEN)
        element_2_a_highlight = SurroundingRectangle(element_2_a, color=GREEN)
        element_2_b_highlight = SurroundingRectangle(element_2_b, color=GREEN)

        self.play(Create(element_1_a_highlight), Create(element_1_b_highlight))
        self.wait(0.5)
        product_1 = MathTex(f"{matrix_a_data[1][0]}*{matrix_b_data[0][1]}").move_to(DOWN * 3)
        self.play(Write(product_1))
        self.wait(0.5)
        self.play(FadeOut(element_1_a_highlight), FadeOut(element_1_b_highlight))

        self.play(Create(element_2_a_highlight), Create(element_2_b_highlight))
        self.wait(0.5)
        product_2 = MathTex(f"+{matrix_a_data[1][1]}*{matrix_b_data[1][1]}").next_to(product_1, RIGHT)
        self.play(Write(product_2))
        self.wait(0.5)
        self.play(FadeOut(element_2_a_highlight), FadeOut(element_2_b_highlight))

        sum_result = matrix_a_data[1][0] * matrix_b_data[0][1] + matrix_a_data[1][1] * matrix_b_data[1][1]
        sum_text = MathTex(f"={sum_result}").next_to(product_2, RIGHT)
        self.play(Write(sum_text))
        self.wait(0.5)

        result_element = result_matrix.get_entries()[3]
        sum_result_mob = MathTex(str(sum_result)).move_to(result_element.get_center())
        self.play(Transform(VGroup(product_1, product_2, sum_text), sum_result_mob))
        self.play(Transform(VGroup(sum_result_mob), result_element))
        self.wait(1)

        self.play(
        row_a.animate.move_to(self.left_region.get_center()).shift(UP * 1.5),
        col_b.animate.move_to(self.right_region.get_center()).shift(UP * 1.5),
        row_a_highlight.animate.move_to(self.left_region.get_center()).shift(UP * 1.5),
        col_b_highlight.animate.move_to(self.right_region.get_center()).shift(UP * 1.5),
        FadeOut(row_a_copy),
        FadeOut(col_b_copy),
        )

        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''The core rule for matrix multiplication is \'row by column.\' To find an element in the resulting matrix, you take a row from the first matrix and a column from the second matrix. Then, you multiply their corresponding elements, pair by pair, and sum up those products. This sum becomes one single element in your new matrix. For example, to find the element in the first row, first column of the result, you\'d use the first row of the first matrix and the first column of the second matrix. It\'s like performing a series of dot products.'''
Scene2.audio_duration = 5.0
