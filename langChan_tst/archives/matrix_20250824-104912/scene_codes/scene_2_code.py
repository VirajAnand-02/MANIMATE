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
        title = self.create_textbox("Matrix Operations: Addition, Subtraction, and Scalar Multiplication", width=10, height=1.5)
        title.move_to(self.title_region.get_center())

        # Left side: Matrix addition and subtraction
        matrix_a = Matrix([[1, 2], [3, 4]])
        matrix_b = Matrix([[5, 6], [7, 8]])
        matrix_result = Matrix([[0, 0], [0, 0]])

        matrix_a.move_to(self.left_region.get_center() + LEFT * 2)
        matrix_b.move_to(self.left_region.get_center() + RIGHT * 2)
        matrix_result.move_to(self.left_region.get_center() + DOWN * 2)

        plus_sign = MathTex("+").move_to(self.left_region.get_center())

        self.play(Create(matrix_a), Create(matrix_b), Write(plus_sign))

        for i in range(2):
        for j in range(2):
        element_a = matrix_a.get_entries()[i * 2 + j]
        element_b = matrix_b.get_entries()[i * 2 + j]
        element_result = matrix_result.get_entries()[i * 2 + j]

        self.play(Indicate(element_a), Indicate(element_b))

        sum_value = int(matrix_a.matrix[i][j]) + int(matrix_b.matrix[i][j])
        self.play(Transform(element_result, MathTex(str(sum_value)).move_to(element_result.get_center())))

        self.wait(1)

        minus_sign = MathTex("-").move_to(self.left_region.get_center())
        self.play(Transform(plus_sign, minus_sign))

        for i in range(2):
        for j in range(2):
        element_a = matrix_a.get_entries()[i * 2 + j]
        element_b = matrix_b.get_entries()[i * 2 + j]
        element_result = matrix_result.get_entries()[i * 2 + j]

        sum_value = int(matrix_a.matrix[i][j]) - int(matrix_b.matrix[i][j])
        self.play(Transform(element_result, MathTex(str(sum_value)).move_to(element_result.get_center())))

        self.wait(1)

        # Right side: Scalar multiplication
        matrix_c = Matrix([[1, 2], [3, 4]])
        matrix_c.move_to(self.right_region.get_center() + LEFT * 2)

        scalar = MathTex("3").move_to(self.right_region.get_center() + RIGHT * 2)
        self.play(Create(matrix_c), Write(scalar))

        scaled_matrix = Matrix([[0, 0], [0, 0]])
        scaled_matrix.move_to(self.right_region.get_center() + DOWN * 2)

        for i in range(2):
        for j in range(2):
        element_c = matrix_c.get_entries()[i * 2 + j]
        element_scaled = scaled_matrix.get_entries()[i * 2 + j]

        arrow = Arrow(scalar.get_center(), element_c.get_center(), buff=0.5)
        self.play(Create(arrow), Indicate(element_c))

        product_value = 3 * int(matrix_c.matrix[i][j])
        self.play(Transform(element_scaled, MathTex(str(product_value)).move_to(element_scaled.get_center())))
        self.play(FadeOut(arrow))

        self.play(Create(scaled_matrix))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''Let\'s explore some basic matrix operations! For addition and subtraction, matrices must have the exact same dimensions. You simply add or subtract corresponding elements – row 1, column 1 of matrix A adds to row 1, column 1 of matrix B, and so on. It\'s like combining two identical spreadsheets cell by cell. Scalar multiplication is even simpler: you multiply every single element within the matrix by a single number, called a scalar. This effectively scales the entire matrix uniformly. These fundamental operations are crucial for manipulating data, whether you\'re combining financial reports or scaling geometric shapes.'''
Scene2.audio_duration = 5.0
