import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
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
        # --- Scene Setup ---
        # Matrices A and B
        matrix_a = MathTex(r"A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}", font_size=60)
        matrix_b = MathTex(r"B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}", font_size=60)
        matrix_c_initial = MathTex(r"C = \begin{pmatrix} ? & ? \\ ? & ? \end{pmatrix}", font_size=60)

        # Arrange A and B side by side, then C below them in the left_region
        matrices_ab = VGroup(matrix_a, matrix_b).arrange(RIGHT, buff=1.5)
        matrices_ab.move_to(self.left_region.get_center() + UP * self.left_region.height / 4)

        matrix_c_initial.next_to(matrices_ab, DOWN, buff=1.0)
        matrix_c_initial.align_to(matrices_ab, LEFT) # Align C with A

        self.play(
        Write(matrix_a),
        Write(matrix_b),
        Write(matrix_c_initial)
        )
        self.wait(0.5)

        # --- Highlight Row 1 of A and Column 1 of B ---
        # Get elements for row 1 of A: 1, 2
        a_11 = matrix_a.get_entries()[0] # The '1'
        a_12 = matrix_a.get_entries()[1] # The '2'
        row1_a = VGroup(a_11, a_12)

        # Get elements for col 1 of B: 5, 7
        b_11 = matrix_b.get_entries()[0] # The '5'
        b_21 = matrix_b.get_entries()[2] # The '7'
        col1_b = VGroup(b_11, b_21)

        # Create surrounding rectangles
        rect_a1 = SurroundingRectangle(row1_a, color=YELLOW, buff=0.1)
        rect_b1 = SurroundingRectangle(col1_b, color=YELLOW, buff=0.1)

        self.play(
        Create(rect_a1),
        Create(rect_b1),
        run_time=1.5
        )
        self.wait(0.5)

        # --- Multiplication on the Right ---
        # Create copies of the elements to move to the right region
        a_11_copy = a_11.copy().set_color(YELLOW)
        a_12_copy = a_12.copy().set_color(YELLOW)
        b_11_copy = b_11.copy().set_color(YELLOW)
        b_21_copy = b_21.copy().set_color(YELLOW)

        # Define target positions in the right region
        target_pos_1x5_left = self.right_region.get_center() + UP * self.right_region.height / 4 + LEFT * 1.5
        target_pos_1x5_right = self.right_region.get_center() + UP * self.right_region.height / 4 + RIGHT * 0.5
        target_pos_2x7_left = self.right_region.get_center() + DOWN * self.right_region.height / 10 + LEFT * 1.5
        target_pos_2x7_right = self.right_region.get_center() + DOWN * self.right_region.height / 10 + RIGHT * 0.5

        # Animate copies moving
        self.play(
        a_11_copy.animate.move_to(target_pos_1x5_left),
        b_11_copy.animate.move_to(target_pos_1x5_right),
        a_12_copy.animate.move_to(target_pos_2x7_left),
        b_21_copy.animate.move_to(target_pos_2x7_right),
        FadeOut(rect_a1), # Fade out the highlighting rectangles
        FadeOut(rect_b1),
        run_time=1.5
        )
        self.wait(0.5)

        # Create multiplication expressions
        mult_sign1 = MathTex(r"\times", font_size=60).next_to(a_11_copy, RIGHT, buff=0.2)
        eq_sign1 = MathTex(r"=", font_size=60).next_to(b_11_copy, RIGHT, buff=0.2)
        result_5 = MathTex("5", font_size=60).next_to(eq_sign1, RIGHT, buff=0.2).set_color(BLUE)

        mult_sign2 = MathTex(r"\times", font_size=60).next_to(a_12_copy, RIGHT, buff=0.2)
        eq_sign2 = MathTex(r"=", font_size=60).next_to(b_21_copy, RIGHT, buff=0.2)
        result_14 = MathTex("14", font_size=60).next_to(eq_sign2, RIGHT, buff=0.2).set_color(BLUE)

        self.play(
        Write(mult_sign1),
        Write(eq_sign1),
        Write(result_5),
        Write(mult_sign2),
        Write(eq_sign2),
        Write(result_14),
        run_time=2
        )
        self.wait(0.5)

        # --- Summation ---
        plus_sign = MathTex("+", font_size=60).next_to(result_5, DOWN, buff=0.5).align_to(mult_sign1, LEFT)
        line_sum = Line(LEFT, RIGHT).set_width(result_14.get_right()[0] - result_5.get_left()[0]).next_to(result_14, DOWN, buff=0.3)
        line_sum.align_to(result_14, RIGHT) # Align the right end of the line with result_14's right end

        sum_result = MathTex("19", font_size=72).next_to(line_sum, DOWN, buff=0.5).set_color(GREEN)

        self.play(
        Write(plus_sign),
        Create(line_sum),
        run_time=1
        )
        self.wait(0.5)
        self.play(
        Write(sum_result),
        run_time=1.5
        )
        self.wait(1)

        # --- Place Result in C11 ---
        # Get the position of the '?' in C11
        c_11_question_mark = matrix_c_initial.get_entries()[0] # The first '?'

        # Create a copy of the '19' from the sum result to move
        sum_result_copy = sum_result.copy()

        # Animate the '19' moving to the C11 position
        self.play(
        sum_result_copy.animate.move_to(c_11_question_mark.get_center()),
        run_time=1.5
        )
        self.wait(0.5)

        # Create the final '19' mobject that will replace the '?' in the matrix
        final_19_in_matrix = MathTex("19", font_size=60).move_to(c_11_question_mark.get_center())
        final_19_in_matrix.set_color(GREEN) # Keep the color consistent

        # Replace the '?' with '19' in the matrix and fade out the moving copy
        self.play(
        ReplacementTransform(c_11_question_mark, final_19_in_matrix),
        FadeOut(sum_result_copy),
        run_time=1
        )
        self.wait(1)

        # --- Cleanup ---
        # Fade out all elements in the right region and the highlighting elements
        self.play(
        FadeOut(a_11_copy), FadeOut(b_11_copy), FadeOut(a_12_copy), FadeOut(b_21_copy),
        FadeOut(mult_sign1), FadeOut(eq_sign1), FadeOut(result_5),
        FadeOut(mult_sign2), FadeOut(eq_sign2), FadeOut(result_14),
        FadeOut(plus_sign), FadeOut(line_sum), FadeOut(sum_result),
        run_time=1.5
        )
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''To find the element in the first row, first column of our result matrix C, often called C11, we take the first row of matrix A and multiply it by the first column of matrix B. We multiply corresponding elements and then sum them up. So, for C11, we multiply (1 times 5) plus (2 times 7). That gives us 5 plus 14, which equals 19. This is our first element!'''
Scene2.audio_duration = 5.0
