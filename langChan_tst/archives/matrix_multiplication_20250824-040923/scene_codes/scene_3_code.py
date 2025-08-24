```python
from manim import *
import numpy as np

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices A, B, and the initial C (from Scene 2's end state)
        A_vals = [[1, 2], [3, 4]]
        B_vals = [[5, 6], [7, 8]]
        C_vals_initial = [[19, "?"], ["?", "?"]]
        C_vals_final = [[19, 22], [43, 50]] # Pre-calculated final values

        A_mat = Matrix(A_vals)
        B_mat = Matrix(B_vals)
        C_mat = Matrix(C_vals_initial)

        # Position matrices on the screen
        A_mat.to_edge(LEFT).shift(UP * 0.5)
        equals1 = MathTex("=").next_to(A_mat, RIGHT, buff=0.5)
        B_mat.next_to(equals1, RIGHT, buff=0.5)
        equals2 = MathTex("=").next_to(B_mat, RIGHT, buff=0.5)
        C_mat.next_to(equals2, RIGHT, buff=0.5)

        # Add initial matrices to the scene
        self.add(A_mat, equals1, B_mat, equals2, C_mat)
        self.wait(0.5)

        # --- C_12 Calculation: Row 1 of A and Column 2 of B ---
        self.next_section("C_12_calc")
        # Highlight the relevant row and column
        self.play(
            Indicate(A_mat.get_rows()[0], color=YELLOW),
            Indicate(B_mat.get_columns()[1], color=YELLOW),
            run_time=2
        )
        self.wait(0.5)

        # Display the dot product calculation
        calc_tex_c12 = MathTex("(1 \\times 6) + (2 \\times 8)").scale(0.8)
        calc_tex_c12.next_to(C_mat, DOWN, buff=1)
        self.play(Write(calc_tex_c12), run_time=1.5)
        self.wait(1)

        # Show the result of the calculation
        result_tex_c12 = MathTex("= 22").scale(0.8).move_to(calc_tex_c12)
        self.play(Transform(calc_tex_c12, result_tex_c12), run_time=1.5)
        self.wait(1)

        # Replace the placeholder in C_mat with the calculated value
        c12_placeholder = C_mat.get_entries()[1] # This is the '?' at C[0][1]
        c12_value = MathTex("22").move_to(c12_placeholder) # Create '22' at the target position

        self.play(
            FadeOut(calc_tex_c12),
            Transform(c12_placeholder, c12_value), # Animate '?' morphing into '22'
            run_time=2
        )
        self.wait(1)

        # --- C_21 Calculation: Row 2 of A and Column 1 of B ---
        self.next_section("C_21_calc")
        # Highlight the relevant row and column
        self.play(
            Indicate(A_mat.get_rows()[1], color=YELLOW),
            Indicate(B_mat.get_columns()[0], color=YELLOW),
            run_time=2
        )
        self.wait(0.5)

        # Display the dot product calculation
        calc_tex_c21 = MathTex("(3 \\times 5) + (4 \\times 7)").scale(0.8)
        calc_tex_c21.next_to(C_mat, DOWN, buff=1)
        self.play(Write(calc_tex_c21), run_time=1.5)
        self.wait(1)

        # Show the result of the calculation
        result_tex_c21 = MathTex("= 43").scale(0.8).move_to(calc_tex_c21)
        self.play(Transform(calc_tex_c21, result_tex_c21), run_time=1.5)
        self.wait(1)

        # Replace the placeholder in C_mat with the calculated value
        c21_placeholder = C_mat.get_entries()[2] # This is the '?' at C[1][0]
        c21_value = MathTex("43").move_to(c21_placeholder)

        self.play(
            FadeOut(calc_tex_c21),
            Transform(c21_placeholder, c21_value),
            run_time=2
        )
        self.wait(1)

        # --- C_22 Calculation: Row 2 of A and Column 2 of B ---
        self.next_section("C_22_calc")
        # Highlight the relevant row and column
        self.play(
            Indicate(A_mat.get_rows()[1], color=YELLOW),
            Indicate(B_mat.get_columns()[1], color=YELLOW),
            run_time=2
        )
        self.wait(0.5)

        # Display the dot product calculation
        calc_tex_c22 = MathTex("(3 \\times 6) + (4 \\times 8)").scale(0.8)
        calc_tex_c22.next_to(C_mat, DOWN, buff=1)
        self.play(Write(calc_tex_c22), run_time=1.5)
        self.wait(1)

        # Show the result of the calculation
        result_tex_c22 = MathTex("= 50").scale(0.8).move_to(calc_tex_c22)
        self.play(Transform(calc_tex_c22, result_tex_c22), run_time=1.5)
        self.wait(1)

        # Replace the placeholder in C_mat with the calculated value
        c22_placeholder = C_mat.get_entries()[3] # This is the '?' at C[1][1]
        c22_value = MathTex("50").move_to(c22_placeholder)

        self.play(
            FadeOut(calc_tex_c22),
            Transform(c22_placeholder, c22_value),
            run_time=2
        )
        self.wait(1)

        # --- Final Display ---
        self.next_section("final_display")
        # The C_mat is now fully populated visually.
        # Emphasize the complete resulting matrix.
        final_C_rect = SurroundingRectangle(C_mat, color=GREEN, buff=0.1)
        self.play(Create(final_C_rect))
        self.wait(2)
        self.play(FadeOut(final_C_rect))
        self.wait(1)
```