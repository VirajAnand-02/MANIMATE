```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices A and B
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]
        matrix_c_data = [[None, None], [None, None]]  # Initialize result matrix

        matrix_a = Matrix(matrix_a_data, element_alignment_corner=UP + LEFT).shift(LEFT * 3)
        matrix_b = Matrix(matrix_b_data, element_alignment_corner=UP + LEFT).shift(LEFT)
        matrix_c = Matrix(matrix_c_data, element_alignment_corner=UP + LEFT).shift(RIGHT * 3)

        text_a = Tex("Matrix A").next_to(matrix_a, UP)
        text_b = Tex("Matrix B").next_to(matrix_b, UP)
        text_c = Tex("Result Matrix C").next_to(matrix_c, UP)

        self.play(Create(matrix_a), Create(matrix_b), Create(matrix_c),
                  Write(text_a), Write(text_b), Write(text_c))
        self.wait(1)

        # Calculations and highlighting
        calculations = []
        result_values = [19, 22, 43, 50]
        matrix_c_coords = [(0, 0), (0, 1), (1, 0), (1, 1)]

        row_col_combinations = [
            ([0], [0]),  # Row 1 of A, Column 1 of B
            ([0], [1]),  # Row 1 of A, Column 2 of B
            ([1], [0]),  # Row 2 of A, Column 1 of B
            ([1], [1])   # Row 2 of A, Column 2 of B
        ]

        for i, (row_indices, col_indices) in enumerate(row_col_combinations):
            # Highlight row of A and column of B
            row_highlight_a = SurroundingRectangle(VGroup(*[matrix_a.entries[row_index][j] for row_index in row_indices for j in range(2)]), color=YELLOW)
            col_highlight_b = SurroundingRectangle(VGroup(*[matrix_b.entries[j][col_index] for col_index in col_indices for j in range(2)]), color=GREEN)

            self.play(Create(row_highlight_a), Create(col_highlight_b))
            self.wait(0.5)

            # Perform calculation
            if i == 0:
                calculation_text = Tex("(1*5) + (2*7) = 19").shift(DOWN * 2)
            elif i == 1:
                calculation_text = Tex("(1*6) + (2*8) = 22").shift(DOWN * 2)
            elif i == 2:
                calculation_text = Tex("(3*5) + (4*7) = 43").shift(DOWN * 2)
            elif i == 3:
                calculation_text = Tex("(3*6) + (4*8) = 50").shift(DOWN * 2)

            self.play(Write(calculation_text))
            self.wait(0.5)

            # Update result matrix
            row, col = matrix_c_coords[i]
            new_matrix_c_data = [row[:] for row in matrix_c_data]
            new_matrix_c_data[row][col] = result_values[i]
            new_matrix_c = Matrix(new_matrix_c_data, element_alignment_corner=UP + LEFT).shift(RIGHT * 3)

            self.play(Transform(matrix_c, new_matrix_c))
            matrix_c = new_matrix_c # Update matrix_c to the new state
            self.wait(0.5)

            self.play(FadeOut(row_highlight_a), FadeOut(col_highlight_b), FadeOut(calculation_text))

        self.wait(2)
        self.play(FadeOut(matrix_a), FadeOut(matrix_b), FadeOut(matrix_c),
                  FadeOut(text_a), FadeOut(text_b), FadeOut(text_c))
        self.wait(1)
```