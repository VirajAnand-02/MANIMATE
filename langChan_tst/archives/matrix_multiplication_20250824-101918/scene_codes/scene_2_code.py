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
        # Left side
        matrix_a = MathTex(r"A_{m \times n}").move_to(self.left_region.get_center() + LEFT * 2)
        matrix_b = MathTex(r"B_{n \times p}").move_to(self.left_region.get_center() + RIGHT * 2)
        matrix_c = MathTex(r"C_{m \times p}").move_to(self.left_region.get_center() + DOWN * 2)

        self.play(Write(matrix_a), Write(matrix_b))

        # Highlight 'n' columns of A and 'n' rows of B
        rect_a = Rectangle(width=matrix_a.width, height=matrix_a.height, color=YELLOW)
        rect_b = Rectangle(width=matrix_b.width, height=matrix_b.height, color=YELLOW)

        rect_a.move_to(matrix_a.get_center())
        rect_b.move_to(matrix_b.get_center())

        self.play(Create(rect_a), Create(rect_b))
        self.wait(0.5)

        check_mark = MathTex(r"\checkmark").move_to(self.left_region.get_center() + UP * 0.5)
        self.play(Write(check_mark))
        self.wait(0.5)

        self.play(FadeOut(rect_a), FadeOut(rect_b), FadeOut(check_mark))

        self.play(Write(matrix_c))
        self.wait(1)

        # Right side
        row_vector = MathTex(r"\begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \end{bmatrix}").move_to(self.right_region.get_center() + UP)
        col_vector = MathTex(r"\begin{bmatrix} b_{11} \\ b_{21} \\ \vdots \\ b_{n1} \end{bmatrix}").move_to(self.right_region.get_center() + DOWN)

        self.play(Write(row_vector), Write(col_vector))

        arrow1 = Arrow(row_vector.get_center() + DOWN * 0.5, col_vector.get_center() + UP * 0.5, buff=0)
        self.play(Create(arrow1))

        times_symbol = MathTex(r"\times").move_to(self.right_region.get_center())
        self.play(Write(times_symbol))

        plus_symbol = MathTex(r"\sum").move_to(self.right_region.get_center() + DOWN * 1)
        self.play(Write(plus_symbol))

        result = MathTex(r"c_{11}").move_to(self.right_region.get_center() + DOWN * 2)
        self.play(Write(result))

        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''Before we dive into the \'how,\' let\'s talk about \'when.\' You can only multiply two matrices if the number of columns in the first matrix equals the number of rows in the second matrix. This is called the \'compatibility rule.\' If matrix A is \'m by n\' and matrix B is \'n by p,\' then their product C will be \'m by p.\' Now, for the calculation itself: to find each element in the resulting matrix, you\'ll take a row from the first matrix and a column from the second. You multiply corresponding elements and then sum up those products. Let\'s visualize this.'''
Scene2.audio_duration = 5.0
