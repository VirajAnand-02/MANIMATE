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
        matrix_3x3 = Matrix([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
        ])
        matrix_3x3.move_to(self.left_region.get_center())

        row_label = self.create_textbox("Row", width=1.5, height=0.5)
        col_label = self.create_textbox("Column", width=1.5, height=0.5)
        element_label = self.create_textbox("Element", width=1.5, height=0.5)
        order_label = self.create_textbox("Order (m x n)", width=2.5, height=0.5)

        row_label.move_to(self.right_region.get_center() + UP * 2.5)
        col_label.move_to(self.right_region.get_center() + UP * 1.25)
        element_label.move_to(self.right_region.get_center() + DOWN * 0)
        order_label.move_to(self.right_region.get_center() + DOWN * 2)

        self.play(Write(matrix_3x3))

        row_rect = SurroundingRectangle(matrix_3x3.get_rows()[0], color=YELLOW)
        self.play(Create(row_rect))
        row_arrow = Arrow(row_label.get_left(), row_rect.get_right(), buff=0.1)
        self.play(Write(row_arrow), Write(row_label))
        self.wait(0.5)
        self.play(FadeOut(row_rect), FadeOut(row_arrow))

        col_rect = SurroundingRectangle(matrix_3x3.get_columns()[0], color=GREEN)
        self.play(Create(col_rect))
        col_arrow = Arrow(col_label.get_left(), col_rect.get_right(), buff=0.1)
        self.play(Write(col_arrow), Write(col_label))
        self.wait(0.5)
        self.play(FadeOut(col_rect), FadeOut(col_arrow))

        element = matrix_3x3.entries[0][0]
        element_rect = SurroundingRectangle(element, color=BLUE)
        self.play(Create(element_rect))
        element_arrow = Arrow(element_label.get_left(), element_rect.get_right(), buff=0.1)
        self.play(Write(element_arrow), Write(element_label))
        self.wait(0.5)

        a_ij = MathTex("a_{ij}", color=BLUE)
        a_ij.next_to(element_rect, DOWN)
        self.play(Write(a_ij))
        self.wait(0.5)
        self.play(FadeOut(element_rect), FadeOut(element_arrow), FadeOut(a_ij))

        order_rect = SurroundingRectangle(matrix_3x3, color=PURPLE)
        self.play(Create(order_rect))
        order_arrow = Arrow(order_label.get_left(), order_rect.get_right(), buff=0.1)
        self.play(Write(order_arrow), Write(order_label))
        self.wait(0.5)
        self.play(FadeOut(order_rect), FadeOut(order_arrow))
        self.play(FadeOut(row_label), FadeOut(col_label), FadeOut(element_label), FadeOut(order_label))

        self.play(FadeOut(matrix_3x3))

        matrix_3x2 = Matrix([
        [1, 2],
        [3, 4],
        [5, 6]
        ])
        matrix_3x2.move_to(self.left_region.get_center())
        order_text = MathTex("3 \\times 2", color=TEAL)
        order_text.next_to(matrix_3x2, RIGHT)

        self.play(Write(matrix_3x2), Write(order_text))

        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''Let\'s look inside a matrix. Every matrix has rows, which run horizontally, and columns, which run vertically. Each individual number inside the matrix is called an element. We identify each element by its position: \'a sub i j\', where \'i\' is the row number and \'j\' is the column number. For example, \'a one one\' is the element in the first row, first column. The size of a matrix is called its order or dimension, defined by the number of rows \'m\' by the number of columns \'n\', written as \'m x n\'. A 3x2 matrix has three rows and two columns. Understanding this notation is key to working with matrices.'''
Scene2.audio_duration = 5.0
