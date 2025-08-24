import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Matrix Multiplication Dimensions", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        matrix_a = MathTex(r"A_{m \times n}", color=BLUE).move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b = MathTex(r"B_{p \times q}", color=RED).move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(0.5)

        m = 2
        n = 3
        p = 3
        q = 2

        matrix_a_dims = MathTex(rf"A_{{{m} \times {n}}}", color=BLUE).move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b_dims = MathTex(rf"B_{{{p} \times {q}}}", color=RED).move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Transform(matrix_a, matrix_a_dims), Transform(matrix_b, matrix_b_dims))
        self.wait(0.5)

        rect_a_inner = SurroundingRectangle(matrix_a_dims[0][5:6], color=YELLOW)
        rect_b_inner = SurroundingRectangle(matrix_b_dims[0][3:4], color=YELLOW)

        self.play(Create(rect_a_inner), Create(rect_b_inner))
        self.wait(0.5)

        self.play(FadeOut(rect_a_inner), FadeOut(rect_b_inner))

        result_matrix_dims = MathTex(rf"C_{{{m} \times {q}}}", color=GREEN).move_to(self.main_region.get_center() + DOWN * 1.5)
        arrow = Arrow(start=self.main_region.get_center() + UP * 0.5, end=result_matrix_dims.get_center() + UP * 0.5, color=WHITE)

        self.play(Create(arrow), Write(result_matrix_dims))
        self.wait(1)

        # Transformation Example
        square = Square(side_length=1, color=WHITE).move_to(self.main_region.get_center() + UP * 2)
        self.play(FadeOut(matrix_a), FadeOut(matrix_b), FadeOut(arrow), FadeOut(result_matrix_dims))
        self.play(Create(square))
        self.wait(0.2)

        rotation_matrix = Matrix([[0, -1], [1, 0]])
        rotated_square = square.copy().rotate(PI/2)

        self.play(Transform(square, rotated_square))
        self.wait(0.5)

        scaling_matrix = Matrix([[2, 0], [0, 2]])
        scaled_square = rotated_square.copy().scale(1.5)

        self.play(Transform(square, scaled_square))
        self.wait(0.5)

        # Summary
        summary_text = self.create_textbox("Practice makes perfect!", width=self.main_region.width * 0.7, height=self.main_region.height * 0.3)
        summary_text.move_to(self.main_region.get_center())

        self.play(FadeOut(square))
        self.play(Write(summary_text))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''Before you multiply, always check the dimensions! For two matrices A (m x n) and B (p x q) to be multiplied, the number of columns in A must equal the number of rows in B. That is, \'n\' must equal \'p\'. The resulting matrix will then have the dimensions \'m x q\'. Matrix multiplication is not commutative, meaning A times B is generally not equal to B times A. This operation is fundamental for transformations like rotations and scaling in 3D graphics, solving linear systems, and much more. Keep practicing, and you\'ll master this essential mathematical tool!'''
Scene4.audio_duration = 5.0
