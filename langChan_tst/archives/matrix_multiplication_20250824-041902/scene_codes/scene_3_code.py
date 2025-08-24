```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # --- Mobject Definitions ---
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]
        # Matrix C starts with 19 already filled, and '?' for others
        matrix_c_initial_data = [[19, "?"], ["?", "?"]]

        mat_a = Matrix(matrix_a_data)
        mat_b = Matrix(matrix_b_data)
        mat_c = Matrix(matrix_c_initial_data)

        label_a = MathTex("A").next_to(mat_a, UP)
        label_b = MathTex("B").next_to(mat_b, UP)
        label_c = MathTex("C").next_to(mat_c, UP)

        # --- Positioning ---
        # Place Matrix A and B at the top, side-by-side
        mat_a.move_to(UP * 2 + LEFT * 3)
        label_a.next_to(mat_a, UP, buff=0.2)

        mat_b.move_to(UP * 2 + RIGHT * 3)
        label_b.next_to(mat_b, UP, buff=0.2)

        # Position Matrix C below A and B, horizontally centered
        mat_c.next_to(mat_a, DOWN, buff=1.5)
        # Shift C to the right to align its center with the midpoint of A and B's centers
        mat_c.shift(RIGHT * (mat_b.get_center()[0] - mat_a.get_center()[0]) / 2)
        label_c.next_to(mat_c, UP, buff=0.2)

        # --- Initial Display ---
        self.play(
            Create(mat_a), Write(label_a),
            Create(mat_b), Write(label_b),
            Create(mat_c), Write(label_c)
        )
        self.wait(0.5)

        # --- Calculate C_12 ---
        # Highlight the first row of A and the second column of B
        row_a1 = mat_a.get_rows()[0]
        col_b2 = mat_b.get_columns()[1]

        rect_a1 = SurroundingRectangle(row_a1, color=YELLOW)
        rect_b2 = SurroundingRectangle(col_b2, color=YELLOW)

        self.play(Create(rect_a1), Create(rect_b2))
        self.wait(0.5)

        # Show the calculation for C_12
        calc_c12 = MathTex("(1 \\times 6) + (2 \\times 8) = 6 + 16 = 22")
        calc_c12.next_to(mat_c, RIGHT, buff=1).shift(UP * 0.5)

        self.play(Write(calc_c12))
        self.wait(0.5)

        # Fill '22' into C_12
        # Get the '?' mobject at position [0][1] in Matrix C
        c12_entry_placeholder = mat_c.get_entries()[0][1]
        c12_result_num = MathTex("22").move_to(c12_entry_placeholder)

        self.play(Transform(c12_entry_placeholder, c12_result_num))
        self.wait(0.5)

        # Clean up C_12 calculation elements
        self.play(
            FadeOut(rect_a1),
            FadeOut(rect_b2),
            FadeOut(calc_c12)
        )
        self.wait(0.5)

        # --- Calculate C_21 ---
        # Highlight the second row of A and the first column of B
        row_a2 = mat_a.get_rows()[1]
        col_b1 = mat_b.get_columns()[0]

        rect_a2 = SurroundingRectangle(row_a2, color=YELLOW)
        rect_b1 = SurroundingRectangle(col_b1, color=YELLOW)

        self.play(Create(rect_a2), Create(rect_b1))
        self.wait(0.5)

        # Show the calculation for C_21
        calc_c21 = MathTex("(3 \\times 5) + (4 \\times 7) = 15 + 28 = 43")
        calc_c21.next_to(mat_c, RIGHT, buff=1).shift(UP * 0.5)

        self.play(Write(calc_c21))
        self.wait(0.5)

        # Fill '43' into C_21
        # Get the '?' mobject at position [1][0] in Matrix C
        c21_entry_placeholder = mat_c.get_entries()[1][0]
        c21_result_num = MathTex("43").move_to(c21_entry_placeholder)

        self.play(Transform(c21_entry_placeholder, c21_result_num))
        self.wait(0.5)

        # Clean up C_21 calculation elements
        self.play(
            FadeOut(rect_a2),
            FadeOut(rect_b1),
            FadeOut(calc_c21)
        )
        self.wait(1) # Final wait
```