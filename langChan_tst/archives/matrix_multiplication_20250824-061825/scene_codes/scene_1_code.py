import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Matrix Multiplication:\nThe Foundation", width=self.title_region.width * 0.9, height=self.title_region.height * 0.9)
        title_text.move_to(self.title_region.get_center())
        self.add(title_text)

        # Define matrices A and B
        matrix_a = MathTex(r"A_{2x3}", color=BLUE).move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b = MathTex(r"B_{3x2}", color=GREEN).move_to(self.main_region.get_center() + RIGHT * 3)
        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(0.5)

        # Highlight the inner dimensions
        a_inner = MathTex("3", color=YELLOW).move_to(matrix_a.get_center() + RIGHT * 1.2)
        b_inner = MathTex("3", color=YELLOW).move_to(matrix_b.get_center() + LEFT * 1.2)
        self.play(Write(a_inner), Write(b_inner))
        self.wait(0.2)

        # Pulsate the inner dimensions
        self.play(
        a_inner.animate.scale(1.2).set_opacity(0.5),
        b_inner.animate.scale(1.2).set_opacity(0.5),
        run_time=0.5,
        rate_func=there_and_back
        )
        self.play(
        a_inner.animate.scale(1/1.2).set_opacity(1),
        b_inner.animate.scale(1/1.2).set_opacity(1),
        run_time=0.5,
        rate_func=there_and_back
        )
        self.wait(0.5)

        # Create matrix C
        matrix_c = MathTex(r"C_{2x2}", color=RED).move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Write(matrix_c))
        self.wait(0.5)

        # Highlight the outer dimensions
        c_outer_rows = MathTex("2", color=PURPLE).move_to(matrix_c.get_center() + LEFT * 1.2)
        c_outer_cols = MathTex("2", color=PURPLE).move_to(matrix_c.get_center() + RIGHT * 1.2)
        self.play(Write(c_outer_rows), Write(c_outer_cols))
        self.wait(0.5)

        # Move the outer dimensions to A and B
        a_outer_rows = MathTex("2", color=PURPLE).move_to(matrix_a.get_center() + LEFT * 1.2)
        b_outer_cols = MathTex("2", color=PURPLE).move_to(matrix_b.get_center() + RIGHT * 1.2)
        self.play(Transform(c_outer_rows, a_outer_rows), Transform(c_outer_cols, b_outer_cols))

        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to the exciting world of matrix multiplication! This operation is fundamental in fields like computer graphics, physics, and data science. But before we dive into *how* to multiply, there\'s a crucial rule about *when* you can multiply. For two matrices, say A and B, to be multiplied (A * B), the number of columns in the first matrix (A) *must* equal the number of rows in the second matrix (B). If matrix A is m x n, and matrix B is n x p, then the resulting matrix C will be m x p. Remember, inner dimensions must match!'''
Scene1.audio_duration = 5.0
