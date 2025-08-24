```python
from manim import *

class GeneratedScene_4(Scene):
    def construct(self):
        # Define matrices A, B, and C (result)
        matrix_A_values = [[1, 2], [3, 4]]
        matrix_B_values = [[5, 6], [7, 8]]
        matrix_C_values_initial = [["?", "?"], ["?", "?"]]
        matrix_C_values_partial = [[19, 22], [43, "?"]] # Assuming C11, C12, C21 are done
        matrix_C_values_final = [[19, 22], [43, 50]]

        # Create Mobjects for matrices and signs
        matrix_A = Matrix(matrix_A_values, h_buff=1.5).scale(0.8)
        matrix_B = Matrix(matrix_B_values, h_buff=1.5).scale(0.8)
        matrix_C = Matrix(matrix_C_values_initial, h_buff=1.5).scale(0.8)
        times_sign = MathTex("\\times").scale(0.8)
        equals_sign = MathTex("=").scale(0.8)

        # Arrange them on screen
        matrix_group = VGroup(matrix_A, times_sign, matrix_B, equals_sign, matrix_C).arrange(RIGHT, buff=0.7).to_edge(UP, buff=1)

        self.add(matrix_A, times_sign, matrix_B, equals_sign)
        self.play(Create(matrix_C))
        self.wait(0.5)

        # Fill in the already calculated values (C11, C12, C21)
        matrix_C_partial_mobj = Matrix(matrix_C_values_partial, h_buff=1.5).scale(0.8).move_to(matrix_C)
        self.play(Transform(matrix_C, matrix_C_partial_mobj))
        self.wait(1.5)

        # --- C22 Calculation ---
        c22_target_entry = matrix_C.get_entries_without_brackets()[3] # The '?' for C22
        c22_target_position = c22_target_entry.get_center()

        # Highlight Row 2 of A and Column 2 of B
        row2_A = matrix_A.get_rows()[1] # [3, 4]
        col2_B = matrix_B.get_columns()[1] # [6, 8]

        self.play(
            Indicate(row2_A, color=YELLOW),
            Indicate(col2_B, color=YELLOW),
            run_time=2
        )
        self.wait(1.5)

        # Display calculation: (3 * 6) + (4 * 8)
        calc_text_1 = MathTex("(3 \\times 6)", "+", "(4 \\times 8)").next_to(matrix_group, DOWN, buff=1)
        self.play(Write(calc_text_1), run_time=2)
        self.wait(2)

        # Display intermediate sum: 18 + 32
        calc_text_2 = MathTex("18", "+", "32").move_to(calc_text_1)
        self.play(TransformMatchingTex(calc_text_1, calc_text_2), run_time=2)
        self.wait(2)

        # Display final result: 50
        calc_text_3 = MathTex("50").move_to(calc_text_2)
        self.play(TransformMatchingTex(calc_text_2, calc_text_3), run_time=2)
        self.wait(2)

        # Slide '50' into the C22 position
        c22_value_mobj = MathTex("50").scale(0.8).move_to(calc_text_3)
        self.play(
            c22_value_mobj.animate.move_to(c22_target_position),
            FadeOut(calc_text_3, shift=DOWN),
            run_time=1.5
            # Indicate animations fade out on their own, no explicit FadeOut needed for highlights
        )
        self.wait(1)

        # Update matrix_C to show the final '50'
        matrix_C_final_mobj = Matrix(matrix_C_values_final, h_buff=1.5).scale(0.8).move_to(matrix_C)
        self.play(Transform(matrix_C, matrix_C_final_mobj), run_time=2.5)
        self.wait(2.5)

        # --- Final Matrix Display ---
        # Move the complete C matrix to the center and make it prominent
        final_C_prominent = Matrix(matrix_C_values_final, h_buff=1.5).scale(1.5)
        self.play(
            FadeOut(matrix_A, times_sign, matrix_B, equals_sign),
            Transform(matrix_C, final_C_prominent),
            run_time=2
        )
        self.wait(4)

        # --- Recap Animation ---
        # Re-position the final C matrix and bring back A and B for the recap
        recap_matrix_A = Matrix(matrix_A_values).scale(0.7).shift(LEFT * 3 + UP * 1.5)
        recap_matrix_B = Matrix(matrix_B_values).scale(0.7).shift(RIGHT * 3 + UP * 1.5)
        recap_times_sign = MathTex("\\times").scale(0.7).next_to(recap_matrix_A, RIGHT, buff=0.5)
        recap_equals_sign = MathTex("=").scale(0.7).next_to(recap_matrix_B, RIGHT, buff=0.5)

        # Transform the prominent C matrix to its recap position and size
        recap_matrix_C_mobj = Matrix(matrix_C_values_final).scale(0.7).next_to(recap_equals_sign, RIGHT, buff=0.5)

        self.play(
            Transform(matrix_C, recap_matrix_C_mobj), # matrix_C now refers to recap_matrix_C_mobj
            FadeIn(recap_matrix_A, recap_times_sign, recap_matrix_B, recap_equals_sign),
            run_time=2
        )
        self.wait(2)

        # Create arrows for each calculation
        arrow_config = {"buff": 0.1, "max_stroke_width_to_length_ratio": 0.5, "max_tip_length_to_length_ratio": 0.25, "stroke_width": 6}

        # C11: Row 1 of A to Col 1 of B
        r1_A_recap = recap_matrix_A.get_rows()[0]
        c1_B_recap = recap_matrix_B.get_columns()[0]
        arrow_c11 = Arrow(r1_A_recap.get_right(), c1_B_recap.get_left(), color=RED, **arrow_config)
        c11_label_recap = matrix_C.get_entries_without_brackets()[0] # Use matrix_C as it's the current recap matrix

        # C12: Row 1 of A to Col 2 of B
        r1_A_recap = recap_matrix_A.get_rows()[0]
        c2_B_recap = recap_matrix_B.get_columns()[1]
        arrow_c12 = Arrow(r1_A_recap.get_right(), c2_B_recap.get_left(), color=BLUE, **arrow_config)
        c12_label_recap = matrix_C.get_entries_without_brackets()[1]

        # C21: Row 2 of A to Col 1 of B
        r2_A_recap = recap_matrix_A.get_rows()[1]
        c1_B_recap = recap_matrix_B.get_columns()[0]
        arrow_c21 = Arrow(r2_A_recap.get_right(), c1_B_recap.get_left(), color=GREEN, **arrow_config)
        c21_label_recap = matrix_C.get_entries_without_brackets()[2]

        # C22: Row 2 of A to Col 2 of B
        r2_A_recap = recap_matrix_A.get_rows()[1]
        c2_B_recap = recap_matrix_B.get_columns()[1]
        arrow_c22 = Arrow(r2_A_recap.get_right(), c2_B_recap.get_left(), color=YELLOW, **arrow_config)
        c22_label_recap = matrix_C.get_entries_without_brackets()[3]

        # Animate each arrow and corresponding label
        self.play(Create(arrow_c11), Indicate(c11_label_recap, scale_factor=1.2), run_time=1.2)
        self.wait(0.5)
        self.play(Create(arrow_c12), Indicate(c12_label_recap, scale_factor=1.2), run_time=1.2)
        self.wait(0.5)
        self.play(Create(arrow_c21), Indicate(c21_label_recap, scale_factor=1.2), run_time=1.2)
        self.wait(0.5)
        self.play(Create(arrow_c22), Indicate(c22_label_recap, scale_factor=1.2), run_time=1.2)
        self.wait(2)

        # Fade out recap elements (arrows, A, B, signs), leaving only the final matrix C
        self.play(
            FadeOut(arrow_c11, arrow_c12, arrow_c21, arrow_c22,
                    recap_matrix_A, recap_times_sign, recap_matrix_B, recap_equals_sign),
            matrix_C.animate.scale(1.5/0.7).move_to(ORIGIN), # Scale C back to prominent size and center
            run_time=3
        )
        self.wait(3)
```