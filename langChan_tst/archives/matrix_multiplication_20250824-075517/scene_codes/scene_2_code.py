import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Matrix Dimensions Explanation

        # Define colors
        highlight_color = YELLOW
        mismatch_color = RED

        # --- Matrix A (m x n) ---
        matrix_a_label = MathTex("A", color=BLUE).scale(1.5)
        matrix_a_dims = MathTex("m \\times n").scale(1.2)
        matrix_a = Rectangle(width=2, height=1.5)
        matrix_a_group = VGroup(matrix_a, matrix_a_label, matrix_a_dims).arrange(DOWN)
        matrix_a_group.move_to(self.left_region.get_center())
        self.play(Create(matrix_a), Write(matrix_a_label), Write(matrix_a_dims))

        # --- Matrix B (n x p) ---
        matrix_b_label = MathTex("B", color=GREEN).scale(1.5)
        matrix_b_dims = MathTex("n \\times p").scale(1.2)
        matrix_b = Rectangle(width=2, height=1.5)
        matrix_b_group = VGroup(matrix_b, matrix_b_label, matrix_b_dims).arrange(DOWN)
        matrix_b_group.move_to(self.right_region.get_center())
        self.play(Create(matrix_b), Write(matrix_b_label), Write(matrix_b_dims))

        self.wait(0.5)

        # --- Highlight matching 'n's ---
        n_a = matrix_a_dims[0][2]  # The 'n' in 'm x n'
        n_b = matrix_b_dims[0][0]  # The 'n' in 'n x p'

        self.play(
        n_a.animate.set_color(highlight_color),
        n_b.animate.set_color(highlight_color),
        run_time=0.75
        )

        # --- Connect the 'n's with a line ---
        connector_line = Line(n_a.get_center(), n_b.get_center(), color=highlight_color)
        self.play(Create(connector_line), run_time=0.5)
        self.wait(0.25)

        # --- Matrix C (m x p) ---
        matrix_c_label = MathTex("C", color=PURPLE).scale(1.5)
        matrix_c_dims = MathTex("m \\times p").scale(1.2)
        matrix_c = Rectangle(width=2, height=1.5)
        matrix_c_group = VGroup(matrix_c, matrix_c_label, matrix_c_dims).arrange(DOWN)
        matrix_c_group.move_to(DOWN * 2)

        arrow = Arrow(UP, matrix_c_group.get_top(), buff=0.2)

        self.play(Create(arrow), Create(matrix_c), Write(matrix_c_label), Write(matrix_c_dims))

        # --- Highlight 'm' and 'p' in Matrix C ---
        m_c = matrix_c_dims[0][0]
        p_c = matrix_c_dims[0][2]

        self.play(
        m_c.animate.set_color(highlight_color),
        p_c.animate.set_color(highlight_color),
        run_time=0.75
        )
        self.wait(0.5)

        # --- Example 1: 2x3 * 3x2 = 2x2 ---
        self.play(
        FadeOut(matrix_a_group, shift=UP),
        FadeOut(matrix_b_group, shift=UP),
        FadeOut(matrix_c_group, shift=DOWN),
        FadeOut(arrow)
        )

        matrix_a_label = MathTex("A", color=BLUE).scale(1.5)
        matrix_a_dims = MathTex("2 \\times 3").scale(1.2)
        matrix_a = Rectangle(width=2, height=1.5)
        matrix_a_group = VGroup(matrix_a, matrix_a_label, matrix_a_dims).arrange(DOWN)
        matrix_a_group.move_to(self.left_region.get_center())

        matrix_b_label = MathTex("B", color=GREEN).scale(1.5)
        matrix_b_dims = MathTex("3 \\times 2").scale(1.2)
        matrix_b = Rectangle(width=2, height=1.5)
        matrix_b_group = VGroup(matrix_b, matrix_b_label, matrix_b_dims).arrange(DOWN)
        matrix_b_group.move_to(self.right_region.get_center())

        matrix_c_label = MathTex("C", color=PURPLE).scale(1.5)
        matrix_c_dims = MathTex("2 \\times 2").scale(1.2)
        matrix_c = Rectangle(width=2, height=1.5)
        matrix_c_group = VGroup(matrix_c, matrix_c_label, matrix_c_dims).arrange(DOWN)
        matrix_c_group.move_to(DOWN * 2)

        arrow = Arrow(UP, matrix_c_group.get_top(), buff=0.2)

        self.play(
        Create(matrix_a), Write(matrix_a_label), Write(matrix_a_dims),
        Create(matrix_b), Write(matrix_b_label), Write(matrix_b_dims),
        Create(arrow), Create(matrix_c), Write(matrix_c_label), Write(matrix_c_dims)
        )

        three_a = matrix_a_dims[0][2]
        three_b = matrix_b_dims[0][0]
        self.play(
        three_a.animate.set_color(highlight_color),
        three_b.animate.set_color(highlight_color),
        run_time=0.75
        )
        self.wait(0.5)

        # --- Example 2: 2x3 * 2x2 = Undefined ---
        self.play(
        FadeOut(matrix_a_group, shift=UP),
        FadeOut(matrix_b_group, shift=UP),
        FadeOut(matrix_c_group, shift=DOWN),
        FadeOut(arrow)
        )

        matrix_a_label = MathTex("A", color=BLUE).scale(1.5)
        matrix_a_dims = MathTex("2 \\times 3").scale(1.2)
        matrix_a = Rectangle(width=2, height=1.5)
        matrix_a_group = VGroup(matrix_a, matrix_a_label, matrix_a_dims).arrange(DOWN)
        matrix_a_group.move_to(self.left_region.get_center())

        matrix_b_label = MathTex("B", color=GREEN).scale(1.5)
        matrix_b_dims = MathTex("2 \\times 2").scale(1.2)
        matrix_b = Rectangle(width=2, height=1.5)
        matrix_b_group = VGroup(matrix_b, matrix_b_label, matrix_b_dims).arrange(DOWN)
        matrix_b_group.move_to(self.right_region.get_center())

        self.play(
        Create(matrix_a), Write(matrix_a_label), Write(matrix_a_dims),
        Create(matrix_b), Write(matrix_b_label), Write(matrix_b_dims),
        )

        three_a = matrix_a_dims[0][2]
        two_b = matrix_b_dims[0][0]
        self.play(
        three_a.animate.set_color(mismatch_color),
        two_b.animate.set_color(mismatch_color),
        run_time=0.75
        )

        cross = Tex("$\\times$").scale(5).set_color(mismatch_color)
        self.play(Write(cross))
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''First, the crucial rule for compatibility: you can only multiply two matrices, say A and B (as A times B), if the number of columns in the first matrix, A, is equal to the number of rows in the second matrix, B. If matrix A is \'m by n\' and matrix B is \'n by p\', then the resulting matrix C will have dimensions \'m by p\'. Notice how the \'inner\' dimensions, \'n\' and \'n\', must match, and the \'outer\' dimensions, \'m\' and \'p\', determine the size of your answer. If they don\'t match, the multiplication is simply undefined!'''
Scene2.audio_duration = 5.0
