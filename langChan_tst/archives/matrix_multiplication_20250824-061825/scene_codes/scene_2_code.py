import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # --- Title Text ---
        title_text = self.create_textbox("How Matrix Multiplication Works", width=self.title_region.width, height=self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # --- Matrices ---
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]
        matrix_c_data = [[None, None], [None, None]]  # Placeholder for the result

        matrix_a = Matrix(matrix_a_data)
        matrix_b = Matrix(matrix_b_data)
        matrix_c = Matrix(matrix_c_data)

        matrix_a.move_to(self.left_region.get_center()).shift(LEFT * 2)
        matrix_b.move_to(self.left_region.get_center()).shift(RIGHT * 2)
        matrix_c.move_to(self.right_region.get_center())

        self.play(Write(matrix_a), Write(matrix_b), Write(matrix_c))
        self.wait(1)

        # --- Highlighting ---
        row_index = 0
        col_index = 0

        row_highlight = Rectangle(width=matrix_a[0][0].get_width() * 2.5, height=matrix_a[0][0].get_height() * 1.5, color=BLUE, fill_opacity=0.2)
        col_highlight = Rectangle(width=matrix_b[0][0].get_width() * 1.5, height=matrix_b[0][0].get_height() * 2.5, color=RED, fill_opacity=0.2)

        row_highlight.move_to(matrix_a.get_rows()[row_index].get_center())
        col_highlight.move_to(matrix_b.get_columns()[col_index].get_center())

        self.play(Create(row_highlight), Create(col_highlight))
        self.wait(1)

        # --- Arrows and Multiplication ---
        a11 = matrix_a[0][0]
        a12 = matrix_a[0][1]
        b11 = matrix_b[0][0]
        b21 = matrix_b[1][0]

        arrow1 = Arrow(a11.get_center(), b11.get_center(), buff=0.5)
        arrow2 = Arrow(a12.get_center(), b21.get_center(), buff=0.5)

        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # --- Calculation ---
        calculation_text = MathTex(f"{matrix_a_data[0][0]}*{matrix_b_data[0][0]} + {matrix_a_data[0][1]}*{matrix_b_data[1][0]}", "=", str(matrix_a_data[0][0]*matrix_b_data[0][0] + matrix_a_data[0][1]*matrix_b_data[1][0]))
        calculation_text.move_to(matrix_c.get_center()).shift(DOWN * 2)

        self.play(Write(calculation_text))
        self.wait(1)

        # --- Result in Matrix C ---
        result_value = matrix_a_data[0][0]*matrix_b_data[0][0] + matrix_a_data[0][1]*matrix_b_data[1][0]
        result_text = MathTex(str(result_value))
        result_text.move_to(matrix_c[0][0].get_center())

        self.play(Transform(calculation_text, result_text))
        self.play(Transform(matrix_c[0][0], result_text))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''Now for the \'how\'! To find an element in the resulting matrix, you take a specific row from the first matrix and a specific column from the second matrix. Let\'s say we want the element in row \'i\' and column \'j\' of the result. You\'ll multiply each element in row \'i\' of the first matrix by its corresponding element in column \'j\' of the second matrix, and then sum up all those products. This is often called the \'dot product\' of the row and column. The position of this sum directly corresponds to the row and column you selected in the result matrix.'''
Scene2.audio_duration = 5.0
