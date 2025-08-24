import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox(
        "Demystifying Matrix Multiplication: 2x2 Matrices",
        self.title_region.width,
        self.title_region.height
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text), run_time=2)
        self.wait(0.5)

        # 2. Two blank 2x2 matrices appear side-by-side, labeled 'A' and 'B'.
        # Create blank matrices with labels
        matrix_A_blank = Matrix([["", ""], ["", ""]])
        label_A = MathTex("A =")
        group_A_blank = VGroup(label_A, matrix_A_blank).arrange(RIGHT, buff=0.2)

        matrix_B_blank = Matrix([["", ""], ["", ""]])
        label_B = MathTex("B =")
        group_B_blank = VGroup(label_B, matrix_B_blank).arrange(RIGHT, buff=0.2)

        # Arrange A and B in the main region. This group will be transformed later.
        current_expression_group = HGroup(group_A_blank, group_B_blank).arrange(RIGHT, buff=1.5)
        current_expression_group.move_to(self.main_region.get_center())

        self.play(
        FadeIn(group_A_blank),
        FadeIn(group_B_blank),
        run_time=3
        )
        self.wait(0.5)

        # 3. Numbers populate them: A = [[1, 2], [3, 4]], B = [[5, 6], [7, 8]].
        # Create the filled matrices with labels
        matrix_A_filled = Matrix([[1, 2], [3, 4]])
        label_A_filled = MathTex("A =")
        group_A_filled = VGroup(label_A_filled, matrix_A_filled).arrange(RIGHT, buff=0.2)

        matrix_B_filled = Matrix([[5, 6], [7, 8]])
        label_B_filled = MathTex("B =")
        group_B_filled = VGroup(label_B_filled, matrix_B_filled).arrange(RIGHT, buff=0.2)

        # Animate the transformation from blank to filled
        # After this, group_A_blank and group_B_blank mobjects will hold the state of group_A_filled and group_B_filled
        self.play(
        Transform(group_A_blank, group_A_filled),
        Transform(group_B_blank, group_B_filled),
        run_time=3
        )
        self.wait(0.5)

        # 4. An equals sign and a question mark appear, followed by a blank 2x2 matrix for 'C'.
        equals_sign = MathTex("=").scale(1.5)
        question_mark = MathTex("?").scale(1.5)

        matrix_C_blank = Matrix([["", ""], ["", ""]])
        label_C = MathTex("C =")
        group_C_blank = VGroup(label_C, matrix_C_blank).arrange(RIGHT, buff=0.2)

        # Create the final arrangement of all elements
        # group_A_blank and group_B_blank now refer to the filled matrices due to the previous Transform
        final_expression_group = HGroup(
        group_A_blank,
        group_B_blank,
        equals_sign,
        question_mark,
        group_C_blank
        ).arrange(RIGHT, buff=0.7)
        final_expression_group.move_to(self.main_region.get_center())

        # Animate the appearance of the new elements and the rearrangement of the entire expression
        self.play(
        Transform(current_expression_group, final_expression_group),
        FadeIn(equals_sign),
        FadeIn(question_mark),
        FadeIn(group_C_blank),
        run_time=4
        )
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Hello and welcome! Today, we\'re demystifying matrix multiplication, specifically for 2x2 matrices. Matrices are powerful tools in math, computer graphics, and engineering. We\'ll take two matrices, A and B, and multiply them to get a new matrix, C. Remember, matrix multiplication isn\'t just multiplying corresponding elements. It\'s a bit more involved, but once you see the pattern, it\'s straightforward! Let\'s dive in.'''
Scene1.audio_duration = 5.0
