import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # 1. Title Card
        title_text = self.create_textbox(
        "Understanding Matrix Multiplication",
        width=self.title_region.width * 0.9,
        height=self.title_region.height * 0.8
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(3) # For "Welcome to understanding matrix multiplication! Matrices are powerful tools in math, science, and computing."

        # 2. Show Matrices A and B
        matrix_A = MathTex(
        r"\begin{pmatrix}", "a", "&", "b", "\\\\", "c", "&", "d", r"\end{pmatrix}",
        font_size=72
        )
        matrix_B = MathTex(
        r"\begin{pmatrix}", "e", "&", "f", "\\\\", "g", "&", "h", r"\end{pmatrix}",
        font_size=72
        )

        # Position matrix A in the main region
        matrix_A.move_to(self.main_region.get_center() + LEFT * 2.5)
        # Position matrix B next to matrix A
        matrix_B.next_to(matrix_A, RIGHT, buff=1.5)

        self.play(FadeIn(matrix_A, shift=LEFT))
        self.wait(1)
        self.play(FadeIn(matrix_B, shift=RIGHT))
        self.wait(1) # For "If we have two matrices, say A and B,"

        # 3. Briefly show a red 'X' over an attempt to multiply them element-wise (e.g., a*e)
        incorrect_multiplication = MathTex(r"a \cdot e", font_size=60)
        incorrect_multiplication.move_to(self.main_region.get_center() + DOWN * 2)

        self.play(Write(incorrect_multiplication))
        self.wait(0.5)

        cross = Cross(incorrect_multiplication, stroke_width=8, color=RED)
        self.play(Create(cross))
        self.wait(2.5) # For "their product C isn't just A_ij times B_ij."

        self.play(FadeOut(incorrect_multiplication), FadeOut(cross))
        self.wait(0.5)

        # 4. Emphasize rows of A and columns of B
        # Narration: "Instead, it involves a specific process of combining rows from the first matrix with columns from the second."

        # Highlight Row 1 of A and Column 1 of B
        row1_A_elements = VGroup(matrix_A[1], matrix_A[3]) # 'a', 'b'
        col1_B_elements = VGroup(matrix_B[1], matrix_B[5]) # 'e', 'g'

        rect_A_row1 = SurroundingRectangle(row1_A_elements, color=YELLOW, buff=0.1)
        rect_B_col1 = SurroundingRectangle(col1_B_elements, color=BLUE, buff=0.1)

        self.play(Create(rect_A_row1), Create(rect_B_col1))
        self.wait(2) # For "combining rows from the first matrix with columns from the second."
        self.play(FadeOut(rect_A_row1), FadeOut(rect_B_col1))
        self.wait(0.5)

        # Highlight Row 2 of A and Column 2 of B (another example)
        row2_A_elements = VGroup(matrix_A[5], matrix_A[7]) # 'c', 'd'
        col2_B_elements = VGroup(matrix_B[3], matrix_B[7]) # 'f', 'h'

        rect_A_row2 = SurroundingRectangle(row2_A_elements, color=YELLOW, buff=0.1)
        rect_B_col2 = SurroundingRectangle(col2_B_elements, color=BLUE, buff=0.1)

        self.play(Create(rect_A_row2), Create(rect_B_col2))
        self.wait(2) # For "Let's dive into how this unique operation works."
        self.play(FadeOut(rect_A_row2), FadeOut(rect_B_col2))
        self.wait(1) # Final wait for narration to finish.

        # Fade out everything at the end for a clean transition to the next scene
        self.play(FadeOut(title_text), FadeOut(matrix_A), FadeOut(matrix_B))
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to understanding matrix multiplication! Matrices are powerful tools in math, science, and computing. But multiplying them isn\'t as simple as multiplying numbers element by element. If we have two matrices, say A and B, their product C isn\'t just A_ij times B_ij. Instead, it involves a specific process of combining rows from the first matrix with columns from the second. Let\'s dive into how this unique operation works.'''
Scene1.audio_duration = 5.0
