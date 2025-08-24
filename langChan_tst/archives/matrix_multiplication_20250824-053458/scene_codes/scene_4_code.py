import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import SplitScreen
import numpy as np

class Scene4(SplitScreen):
    def construct_scene(self):
        # Define matrices A and B
        matrix_A_data = [[1, 2], [3, 4]]
        matrix_B_data = [[5, 6], [7, 8]]

        # Create MathTex objects for matrices A and B
        matrix_A = MathTex(
        r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}",
        color=BLUE
        )
        matrix_B = MathTex(
        r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}",
        color=GREEN
        )

        # Position matrices A and B on the left region
        matrix_A.move_to(self.left_region.get_center() + LEFT * 2)
        matrix_B.move_to(self.left_region.get_center() + RIGHT * 2)

        # Create a blank result matrix C
        matrix_C = MathTex(
        r"\begin{bmatrix} ? & ? \\ ? & ? \end{bmatrix}",
        color=YELLOW
        )

        # Position matrix C on the right region
        matrix_C.move_to(self.right_region.get_center())

        # Add matrices A, B, and C to the scene
        self.play(Write(matrix_A), Write(matrix_B), Write(matrix_C))
        self.wait(1)

        # --- C_11 Calculation ---
        # Highlight row 1 of A and column 1 of B
        row_1_A = SurroundingRectangle(matrix_A[0][0:3], color=RED)
        col_1_B = SurroundingRectangle(matrix_B[0][0:3], color=RED)
        self.play(Create(row_1_A), Create(col_1_B))
        self.wait(0.5)

        # Show the multiplication and summation for C_11
        c_11_calculation = MathTex(
        r"(1 \times 5) + (2 \times 7) = 5 + 14 = 19",
        color=RED
        ).next_to(matrix_C, DOWN)
        self.play(Write(c_11_calculation))
        self.wait(0.5)

        # Update C_11 in matrix C
        matrix_C_updated = MathTex(
        r"\begin{bmatrix} 19 & ? \\ ? & ? \end{bmatrix}",
        color=YELLOW
        ).move_to(self.right_region.get_center())
        self.play(Transform(matrix_C, matrix_C_updated))
        self.play(FadeOut(row_1_A), FadeOut(col_1_B), FadeOut(c_11_calculation))
        self.wait(0.5)

        # --- C_12 Calculation ---
        # Highlight row 1 of A and column 2 of B
        row_1_A = SurroundingRectangle(matrix_A[0][0:3], color=ORANGE)
        col_2_B = SurroundingRectangle(matrix_B[0][4:7], color=ORANGE)
        self.play(Create(row_1_A), Create(col_2_B))
        self.wait(0.5)

        # Show the multiplication and summation for C_12
        c_12_calculation = MathTex(
        r"(1 \times 6) + (2 \times 8) = 6 + 16 = 22",
        color=ORANGE
        ).next_to(matrix_C, DOWN)
        self.play(Write(c_12_calculation))
        self.wait(0.5)

        # Update C_12 in matrix C
        matrix_C_updated = MathTex(
        r"\begin{bmatrix} 19 & 22 \\ ? & ? \end{bmatrix}",
        color=YELLOW
        ).move_to(self.right_region.get_center())
        self.play(Transform(matrix_C, matrix_C_updated))
        self.play(FadeOut(row_1_A), FadeOut(col_2_B), FadeOut(c_12_calculation))
        self.wait(0.5)

        # --- C_21 Calculation ---
        # Highlight row 2 of A and column 1 of B
        row_2_A = SurroundingRectangle(matrix_A[0][4:7], color=PURPLE)
        col_1_B = SurroundingRectangle(matrix_B[0][0:3], color=PURPLE)
        self.play(Create(row_2_A), Create(col_1_B))
        self.wait(0.5)

        # Show the multiplication and summation for C_21
        c_21_calculation = MathTex(
        r"(3 \times 5) + (4 \times 7) = 15 + 28 = 43",
        color=PURPLE
        ).next_to(matrix_C, DOWN)
        self.play(Write(c_21_calculation))
        self.wait(0.5)

        # Update C_21 in matrix C
        matrix_C_updated = MathTex(
        r"\begin{bmatrix} 19 & 22 \\ 43 & ? \end{bmatrix}",
        color=YELLOW
        ).move_to(self.right_region.get_center())
        self.play(Transform(matrix_C, matrix_C_updated))
        self.play(FadeOut(row_2_A), FadeOut(col_1_B), FadeOut(c_21_calculation))
        self.wait(0.5)

        # --- C_22 Calculation ---
        # Highlight row 2 of A and column 2 of B
        row_2_A = SurroundingRectangle(matrix_A[0][4:7], color=TEAL)
        col_2_B = SurroundingRectangle(matrix_B[0][4:7], color=TEAL)
        self.play(Create(row_2_A), Create(col_2_B))
        self.wait(0.5)

        # Show the multiplication and summation for C_22
        c_22_calculation = MathTex(
        r"(3 \times 6) + (4 \times 8) = 18 + 32 = 50",
        color=TEAL
        ).next_to(matrix_C, DOWN)
        self.play(Write(c_22_calculation))
        self.wait(0.5)

        # Update C_22 in matrix C
        matrix_C_final = MathTex(
        r"\begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}",
        color=YELLOW
        ).move_to(self.right_region.get_center())
        self.play(Transform(matrix_C, matrix_C_final))
        self.play(FadeOut(row_2_A), FadeOut(col_2_B), FadeOut(c_22_calculation))
        self.wait(1)

# Set narration and duration
Scene4.narration_text = '''Let\'s walk through a quick example. Consider Matrix A: [[1, 2], [3, 4]] and Matrix B: [[5, 6], [7, 8]]. Both are 2x2, so the result will also be 2x2. To find the top-left element, C_11: we take row 1 of A [1, 2] and column 1 of B [5, 7]. (1*5) + (2*7) = 5 + 14 = 19. For C_12: row 1 of A [1, 2] and column 2 of B [6, 8]. (1*6) + (2*8) = 6 + 16 = 22. You repeat this for every position. C_21: (3*5) + (4*7) = 15 + 28 = 43. And C_22: (3*6) + (4*8) = 18 + 32 = 50. So, the final product matrix is [[19, 22], [43, 50]].'''
Scene4.audio_duration = 5.0
