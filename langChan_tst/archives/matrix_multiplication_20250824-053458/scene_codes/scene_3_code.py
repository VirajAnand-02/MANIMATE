```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices (example 2x2 matrices)
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]

        matrix_a = Matrix(matrix_a_data)
        matrix_b = Matrix(matrix_b_data)

        # Position matrices
        matrix_a.to_edge(LEFT)
        matrix_b.to_edge(RIGHT)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(1)

        # Highlight first row of A and first column of B
        row_arrow = Arrow(matrix_a.get_rows()[0].get_left(), matrix_a.get_rows()[0].get_right(), buff=0.2)
        col_arrow = Arrow(matrix_b.get_columns()[0].get_top(), matrix_b.get_columns()[0].get_bottom(), buff=0.2)

        self.play(Create(row_arrow), Create(col_arrow))
        self.wait(1)

        # Extract elements for multiplication
        a11 = matrix_a.get_entries()[0].copy()
        a12 = matrix_a.get_entries()[1].copy()
        b11 = matrix_b.get_entries()[0].copy()
        b21 = matrix_b.get_entries()[2].copy()

        # Position elements
        a11.move_to(LEFT * 3 + DOWN * 2)
        b11.move_to(LEFT * 1 + DOWN * 2)
        a12.move_to(RIGHT * 1 + DOWN * 2)
        b21.move_to(RIGHT * 3 + DOWN * 2)

        self.play(
            Transform(matrix_a.get_entries()[0].copy(), a11),
            Transform(matrix_b.get_entries()[0].copy(), b11),
            Transform(matrix_a.get_entries()[1].copy(), a12),
            Transform(matrix_b.get_entries()[2].copy(), b21)
        )
        self.wait(0.5)

        # Create multiplication signs
        mult1 = MathTex("\\times").move_to(LEFT * 2 + DOWN * 2)
        mult2 = MathTex("\\times").move_to(RIGHT * 2 + DOWN * 2)

        self.play(Write(mult1), Write(mult2))
        self.wait(0.5)

        # Show the products
        product1 = MathTex("1 \\times 5").move_to(LEFT * 3 + DOWN * 3)
        product2 = MathTex("2 \\times 7").move_to(RIGHT * 3 + DOWN * 3)

        self.play(Write(product1), Write(product2))
        self.wait(0.5)

        # Plus sign
        plus_sign = MathTex("+").move_to(DOWN * 3)
        self.play(Write(plus_sign))
        self.wait(0.5)

        # Sum
        sum_result = MathTex("= 19").move_to(DOWN * 3 + RIGHT * 1.5)
        self.play(Write(sum_result))
        self.wait(0.5)

        # Create the result matrix
        result_matrix_data = [[19, None], [None, None]]
        result_matrix = Matrix(result_matrix_data)
        result_matrix.to_edge(DOWN)

        self.play(Write(result_matrix.get_entries()[0]))
        self.wait(1)

        self.play(FadeOut(row_arrow), FadeOut(col_arrow), FadeOut(a11), FadeOut(b11), FadeOut(a12), FadeOut(b21), FadeOut(mult1), FadeOut(mult2), FadeOut(product1), FadeOut(product2), FadeOut(plus_sign), FadeOut(sum_result))

        self.wait(2)
```