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
        # Define matrices A and B
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]

        # Create MathTex objects for matrices A and B
        matrix_a = MathTex(
        r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}"
        ).move_to(self.left_region.get_center())
        matrix_b = MathTex(
        r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}"
        ).move_to(self.right_region.get_center())

        # Create an empty matrix C
        matrix_c = MathTex(
        r"\begin{bmatrix} ? & ? \\ ? & ? \end{bmatrix}"
        ).move_to(ORIGIN)

        # Create surrounding rectangles for highlighting
        row_a_rect = Rectangle(
        width=matrix_a[0][0:3].get_width() + 0.2,
        height=matrix_a[0][0:3].get_height() + 0.2,
        color=YELLOW
        ).move_to(matrix_a[0][0:3].get_center())

        col_b_rect = Rectangle(
        width=matrix_b[0][0].get_width() + matrix_b[0][3].get_width() + 0.2,
        height=matrix_b[0][0].get_height() * 2 + 0.2,
        color=YELLOW
        ).move_to(matrix_b[0][0].get_center() + matrix_b[0][3].get_center()).shift(DOWN*0.1)

        # Create arrows and labels for element multiplication
        arrow_1 = Arrow(matrix_a[0][0].get_right(), matrix_b[0][0].get_left(), color=BLUE)
        arrow_2 = Arrow(matrix_a[0][2].get_right(), matrix_b[0][3].get_left(), color=BLUE)

        product_1 = MathTex("1 \\times 5 = 5").next_to(arrow_1, DOWN)
        product_2 = MathTex("2 \\times 7 = 14").next_to(arrow_2, DOWN)
        sum_products = MathTex("5 + 14 = 19").next_to(product_1, DOWN)

        # Animations
        self.play(Create(matrix_a), Create(matrix_b))
        self.play(Write(matrix_c))
        self.wait(0.5)
        self.play(Create(row_a_rect))
        self.play(Create(col_b_rect))
        self.wait(0.5)
        self.play(Create(arrow_1), Create(arrow_2))
        self.play(Write(product_1), Write(product_2))
        self.play(Write(sum_products))

        # Update matrix C
        new_matrix_c = MathTex(
        r"\begin{bmatrix} 19 & ? \\ ? & ? \end{bmatrix}"
        ).move_to(ORIGIN)
        self.play(Transform(matrix_c, new_matrix_c))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''The key to matrix multiplication lies in the \'row by column\' rule. To find a single element in the resulting matrix, say at row \'i\' and column \'j\', you take the \'i-th\' row of the first matrix and the \'j-th\' column of the second matrix. Then, you multiply their corresponding elements and sum up those products. Let\'s look at a simple example: If we want to find the element in the first row, first column of our result, we\'ll use the first row of Matrix A and the first column of Matrix B. Multiply element by element, then add them up. This sum gives us just one entry in our new matrix.'''
Scene2.audio_duration = 5.0
