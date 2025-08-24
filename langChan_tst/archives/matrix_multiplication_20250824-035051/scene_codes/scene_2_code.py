import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Left Side
        matrix_a = MathTex(r"\begin{bmatrix} a & b & c \\ d & e & f \end{bmatrix}").move_to(self.left_region.get_center() + UP * 1.5)
        matrix_b = MathTex(r"\begin{bmatrix} g & h \\ i & j \\ k & l \end{bmatrix}").move_to(self.left_region.get_center() + DOWN * 1.5)
        label_a = Text("Matrix A").next_to(matrix_a, UP)
        label_b = Text("Matrix B").next_to(matrix_b, DOWN)

        arrow_a = Arrow(matrix_a.get_corner(DL), matrix_a.get_corner(DR), color=YELLOW)
        arrow_b = Arrow(matrix_b.get_corner(UL), matrix_b.get_corner(UR), color=YELLOW)

        text_match = Text("Columns of A = Rows of B", font_size=24).move_to(self.left_region.get_center())

        # Right Side
        matrix_c = MathTex(r"\begin{bmatrix} m & n \\ o & p \end{bmatrix}").move_to(self.right_region.get_center() + UP * 1.5)
        checkmark = MathTex(r"\checkmark").next_to(matrix_c, RIGHT)

        matrix_undefined_a = MathTex(r"\begin{bmatrix} m & n \\ o & p \end{bmatrix}").move_to(self.right_region.get_center() + DOWN * 1.5 + LEFT * 1.5)
        matrix_undefined_b = MathTex(r"\begin{bmatrix} g & h \\ i & j \\ k & l \end{bmatrix}").next_to(matrix_undefined_a, RIGHT)
        cross = MathTex(r"\times").next_to(matrix_undefined_b, RIGHT)
        text_undefined = Text("Undefined", color=RED).next_to(cross, RIGHT)

        self.play(Create(matrix_a), Create(matrix_b), Write(label_a), Write(label_b))
        self.wait(0.5)
        self.play(Create(arrow_a), Create(arrow_b))
        self.play(Write(text_match))
        self.wait(1)
        self.play(Create(matrix_c), Write(checkmark))
        self.play(Create(matrix_undefined_a), Create(matrix_undefined_b), Write(cross), Write(text_undefined))
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''Unlike regular multiplication, matrix multiplication has specific rules. It\'s all about rows and columns! To multiply two matrices, the number of columns in the first matrix MUST equal the number of rows in the second matrix. If they don\'t match, the multiplication is undefined.'''
Scene2.audio_duration = 5.0
