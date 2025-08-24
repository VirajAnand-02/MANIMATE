import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Title Text
        title = self.create_textbox("Dimensions Matter!", width=6, height=1)
        title.move_to(self.title_region.get_center())

        # Matrix A (m x n)
        matrix_a_text = MathTex(r"A_{m \times n}", color=BLUE)
        matrix_a_text.move_to(self.left_region.get_center())

        # Matrix B (n x p)
        matrix_b_text = MathTex(r"B_{n \times p}", color=GREEN)
        matrix_b_text.move_to(self.right_region.get_center())

        # Resultant Matrix (m x p)
        resultant_matrix_text = MathTex(r"C_{m \times p}", color=YELLOW)
        resultant_matrix_text.move_to(self.bottom_region.get_center())

        # Arrows
        arrow_a = Arrow(matrix_a_text.get_right(), [0, 0, 0], color=RED)
        arrow_b = Arrow(matrix_b_text.get_left(), [0, 0, 0], color=RED)

        arrow_a.move_to(matrix_a_text.get_right() + RIGHT * 0.5)
        arrow_b.move_to(matrix_b_text.get_left() + LEFT * 0.5)

        # Animations
        self.play(Write(title))
        self.wait(1)
        self.play(
        AnimationGroup(
        Write(matrix_a_text),
        Write(matrix_b_text),
        lag_ratio=0.2
        )
        )
        self.wait(1)

        self.play(
        AnimationGroup(
        Create(arrow_a),
        Create(arrow_b),
        lag_ratio=0.2
        )
        )
        self.wait(1)

        self.play(Write(resultant_matrix_text))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''First, dimensions matter! To multiply matrix A by matrix B, the number of columns in A must equal the number of rows in B. If A is m x n and B is n x p, the result will be m x p.'''
Scene2.audio_duration = 5.0
