import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # --- Title Text ---
        title_text = self.create_textbox(
        "Matrix Multiplication Dimensions", width=6, height=1
        )
        title_text.move_to(self.title_region.get_center())

        # --- Matrix A ---
        matrix_a_text = MathTex(r"A_{m \times n}")
        matrix_a_text.move_to(self.left_region.get_center())

        # --- Matrix B ---
        matrix_b_text = MathTex(r"B_{n \times p}")
        matrix_b_text.move_to(self.right_region.get_center())

        # --- Arrow ---
        arrow = Arrow(
        matrix_a_text[-1].get_right(), matrix_b_text[2].get_left(), buff=0.2
        )

        # --- Matrix C ---
        matrix_c_text = MathTex(r"C_{m \times p}")
        matrix_c_text.move_to(self.bottom_region.get_center())

        # --- Animations ---
        self.play(Write(matrix_a_text), Write(matrix_b_text))
        self.wait(0.5)
        self.play(Create(arrow))
        self.wait(0.5)
        self.play(Write(matrix_c_text))
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''First, let\'s understand the dimensions. To multiply matrix A by matrix B, the number of columns in A *must* equal the number of rows in B. If A is an \'m x n\' matrix and B is an \'n x p\' matrix, the resulting matrix C will be an \'m x p\' matrix.'''
Scene2.audio_duration = 5.0
