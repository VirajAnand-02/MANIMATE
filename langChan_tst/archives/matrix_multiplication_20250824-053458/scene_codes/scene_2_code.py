import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Define colors
        highlight_color = YELLOW
        incompatible_color = RED

        # Create matrices A and B
        matrix_A = MathTex(r"A", r"_{m \times n}").move_to(self.left_region.get_center())
        matrix_B = MathTex(r"B", r"_{n \times p}").move_to(self.right_region.get_center())

        # Highlight the 'n's
        n_A = matrix_A[1][3]
        n_B = matrix_B[1][0]
        n_A.set_color(highlight_color)
        n_B.set_color(highlight_color)

        # Create the arrow connecting the 'n's
        arrow = CurvedArrow(n_A.get_right(), n_B.get_left(), color=highlight_color)

        # Create matrix C
        matrix_C = MathTex(r"C", r"_{m \times p}")
        matrix_C.move_to(ORIGIN) # Center for now

        # Highlight the 'm' and 'p'
        m_C = matrix_C[1][0]
        p_C = matrix_C[1][3]
        m_C.set_color(highlight_color)
        p_C.set_color(highlight_color)

        # Move matrix C to below A and B
        matrix_C.move_to(DOWN * 2)

        # Create the X for incompatible matrices
        X = MathTex(r"\text{X}").scale(5).set_color(incompatible_color)
        X.move_to(ORIGIN)

        # Animations
        self.play(Write(matrix_A), Write(matrix_B))
        self.wait(1)
        self.play(Create(arrow))
        self.wait(2)
        self.play(Write(matrix_C))
        self.wait(2)

        # Incompatible case (briefly show the X)
        self.play(FadeOut(matrix_A), FadeOut(matrix_B), FadeOut(arrow), FadeOut(matrix_C))
        self.play(Write(X))
        self.wait(1)
        self.play(FadeOut(X))

        # Restore the compatible case
        self.play(Write(matrix_A), Write(matrix_B))
        self.play(Create(arrow))
        self.play(Write(matrix_C))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''The very first step in matrix multiplication is checking compatibility. You can only multiply two matrices, say Matrix A and Matrix B, if the number of columns in Matrix A is equal to the number of rows in Matrix B. If Matrix A is an \'m by n\' matrix (m rows, n columns) and Matrix B is an \'n by p\' matrix (n rows, p columns), then they are compatible! The resulting product matrix will have the dimensions \'m by p\' – matching the outer dimensions of the original matrices. If those inner numbers don\'t match, you simply cannot multiply them!'''
Scene2.audio_duration = 5.0
