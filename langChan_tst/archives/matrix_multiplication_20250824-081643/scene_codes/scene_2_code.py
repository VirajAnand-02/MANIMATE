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
        title = self.create_textbox("Matrix Multiplication: Row by Column", width=self.left_region.width, height=1)
        title.move_to(self.left_region.get_center())

        matrix_a = Matrix([["A11", "A12"], ["A21", "A22"]])
        matrix_b = Matrix([["B11", "B12"], ["B21", "B22"]])
        matrix_c = Matrix([["C11", "C12"], ["C21", "C22"]])

        matrix_a.move_to(self.right_region.get_center() + LEFT * 2)
        matrix_b.move_to(self.right_region.get_center() + RIGHT * 2)
        matrix_c.move_to(self.right_region.get_center() + DOWN * 2)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(1)

        # Highlight first row of A and first column of B
        row_a = matrix_a.get_rows()[0]
        col_b = matrix_b.get_columns()[0]

        rect_a = SurroundingRectangle(row_a)
        rect_b = SurroundingRectangle(col_b)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(1)

        # Arrows and calculations for C11
        arrow1 = Arrow(row_a[0].get_center(), matrix_c.get_entries()[0].get_center() + LEFT * 0.5, buff=0)
        arrow2 = Arrow(row_a[1].get_center(), matrix_c.get_entries()[0].get_center() + RIGHT * 0.5, buff=0)

        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # Show the sum of products
        c11_text = MathTex("A11*B11 + A12*B21").scale(0.7)
        c11_text.next_to(matrix_c.get_entries()[0], DOWN)

        self.play(Write(c11_text))
        self.wait(1)

        self.play(FadeOut(rect_a), FadeOut(rect_b), FadeOut(arrow1), FadeOut(arrow2), FadeOut(c11_text))
        self.wait(0.5)

        # Highlight first row of A and second column of B
        col_b = matrix_b.get_columns()[1]

        rect_a = SurroundingRectangle(row_a)
        rect_b = SurroundingRectangle(col_b)

        self.play(Create(rect_a), Create(rect_b))
        self.wait(1)

        # Arrows and calculations for C12
        arrow1 = Arrow(row_a[0].get_center(), matrix_c.get_entries()[1].get_center() + LEFT * 0.5, buff=0)
        arrow2 = Arrow(row_a[1].get_center(), matrix_c.get_entries()[1].get_center() + RIGHT * 0.5, buff=0)

        self.play(Create(arrow1), Create(arrow2))
        self.wait(1)

        # Show the sum of products
        c12_text = MathTex("A11*B12 + A12*B22").scale(0.7)
        c12_text.next_to(matrix_c.get_entries()[1], DOWN)

        self.play(Write(c12_text))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''The heart of matrix multiplication lies in the \'row by column\' rule. Imagine we have two matrices, Matrix A and Matrix B. To find an element in the resulting product matrix, say at position (i, j), we take the i-th row of Matrix A and multiply each of its elements by the corresponding elements in the j-th column of Matrix B. Then, we sum up these products. This might sound a bit abstract, so let\'s visualize it. We\'re essentially performing a dot product between a row vector from the first matrix and a column vector from the second. Each element in our new matrix is the result of one such dot product. Let\'s see how this works with a small example.'''
Scene2.audio_duration = 5.0
