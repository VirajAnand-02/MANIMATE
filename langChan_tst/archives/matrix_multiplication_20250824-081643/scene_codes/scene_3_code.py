```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices A and B (example values)
        matrix_a_data = [[1, 2, 3], [4, 5, 6]]
        matrix_b_data = [[7, 8], [9, 10], [11, 12]]

        # Create MathTex objects for matrices A and B
        matrix_a = MathTex(
            r"\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}",
            substrings_to_isolate=","
        ).scale(0.75).to_edge(LEFT)
        matrix_b = MathTex(
            r"\begin{bmatrix} 7 & 8 \\ 9 & 10 \\ 11 & 12 \end{bmatrix}",
            substrings_to_isolate=","
        ).scale(0.75).next_to(matrix_a, RIGHT, buff=1)

        # Empty result matrix C
        matrix_c = MathTex(
            r"\begin{bmatrix} c_{11} & c_{12} \\ c_{21} & c_{22} \end{bmatrix}",
            substrings_to_isolate=","
        ).scale(0.75).to_edge(RIGHT)

        self.play(Write(matrix_a), Write(matrix_b), Write(matrix_c))
        self.wait(1)

        # Step 1: Highlight row 1 of A and column 1 of B
        row_1_a = SurroundingRectangle(matrix_a[0][0:5], color=YELLOW)
        col_1_b = SurroundingRectangle(matrix_b[0][0:3], color=YELLOW)
        self.play(Create(row_1_a), Create(col_1_b))

        # Calculation for C11
        c11_calc = MathTex(
            "(1*7 + 2*9 + 3*11) = 58"
        ).scale(0.6).next_to(matrix_b, DOWN, buff=0.5)
        self.play(Write(c11_calc))
        self.wait(0.5)

        c11_val = MathTex("58").scale(0.75)
        self.play(Transform(c11_calc, c11_val.move_to(c11_calc.get_center())))
        self.wait(0.5)

        c11_replace = MathTex("58").scale(0.75).move_to(matrix_c[0][0].get_center())
        self.play(Transform(matrix_c[0][0], c11_replace))
        self.play(FadeOut(row_1_a), FadeOut(col_1_b), FadeOut(c11_calc))
        self.wait(0.5)

        # Step 2: Highlight row 1 of A and column 2 of B
        row_1_a = SurroundingRectangle(matrix_a[0][0:5], color=YELLOW)
        col_2_b = SurroundingRectangle(matrix_b[0][3:6], color=YELLOW)
        self.play(Create(row_1_a), Create(col_2_b))

        # Calculation for C12
        c12_calc = MathTex(
            "(1*8 + 2*10 + 3*12) = 64"
        ).scale(0.6).next_to(matrix_b, DOWN, buff=0.5)
        self.play(Write(c12_calc))
        self.wait(0.5)

        c12_val = MathTex("64").scale(0.75)
        self.play(Transform(c12_calc, c12_val.move_to(c12_calc.get_center())))
        self.wait(0.5)

        c12_replace = MathTex("64").scale(0.75).move_to(matrix_c[0][2].get_center())
        self.play(Transform(matrix_c[0][2], c12_replace))
        self.play(FadeOut(row_1_a), FadeOut(col_2_b), FadeOut(c12_calc))
        self.wait(0.5)

        # Step 3: Highlight row 2 of A and column 1 of B
        row_2_a = SurroundingRectangle(matrix_a[0][6:11], color=YELLOW)
        col_1_b = SurroundingRectangle(matrix_b[0][0:3], color=YELLOW)
        self.play(Create(row_2_a), Create(col_1_b))

        # Calculation for C21
        c21_calc = MathTex(
            "(4*7 + 5*9 + 6*11) = 133"
        ).scale(0.6).next_to(matrix_b, DOWN, buff=0.5)
        self.play(Write(c21_calc))
        self.wait(0.5)

        c21_val = MathTex("133").scale(0.75)
        self.play(Transform(c21_calc, c21_val.move_to(c21_calc.get_center())))
        self.wait(0.5)

        c21_replace = MathTex("133").scale(0.75).move_to(matrix_c[0][4].get_center())
        self.play(Transform(matrix_c[0][4], c21_replace))
        self.play(FadeOut(row_2_a), FadeOut(col_1_b), FadeOut(c21_calc))
        self.wait(0.5)

        # Step 4: Highlight row 2 of A and column 2 of B
        row_2_a = SurroundingRectangle(matrix_a[0][6:11], color=YELLOW)
        col_2_b = SurroundingRectangle(matrix_b[0][3:6], color=YELLOW)
        self.play(Create(row_2_a), Create(col_2_b))

        # Calculation for C22
        c22_calc = MathTex(
            "(4*8 + 5*10 + 6*12) = 144"
        ).scale(0.6).next_to(matrix_b, DOWN, buff=0.5)
        self.play(Write(c22_calc))
        self.wait(0.5)

        c22_val = MathTex("144").scale(0.75)
        self.play(Transform(c22_calc, c22_val.move_to(c22_calc.get_center())))
        self.wait(0.5)

        c22_replace = MathTex("144").scale(0.75).move_to(matrix_c[0][6].get_center())
        self.play(Transform(matrix_c[0][6], c22_replace))
        self.play(FadeOut(row_2_a), FadeOut(col_2_b), FadeOut(c22_calc))
        self.wait(0.5)

        # Final Result Matrix
        final_matrix_c = MathTex(
            r"\begin{bmatrix} 58 & 64 \\ 133 & 144 \end{bmatrix}",
            substrings_to_isolate=","
        ).scale(0.75).move_to(matrix_c.get_center())
        self.play(Transform(matrix_c, final_matrix_c))
        self.wait(2)
```