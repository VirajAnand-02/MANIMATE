```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define the matrices
        matrix_A_data = [[1, 2], [3, 4]]
        matrix_B_data = [[5, 6], [7, 8]]
        matrix_C_data = [[None, None], [None, None]]

        matrix_A = Matrix(matrix_A_data, bracket_h_buff=0.5, bracket_v_buff=0.5)
        matrix_B = Matrix(matrix_B_data, bracket_h_buff=0.5, bracket_v_buff=0.5)
        matrix_C = Matrix(matrix_C_data, bracket_h_buff=0.5, bracket_v_buff=0.5)

        # Position the matrices
        matrix_A.to_corner(UP + LEFT)
        matrix_B.to_corner(UP + RIGHT)
        matrix_C.to_corner(DOWN)

        # Highlight C11
        c11_rect = SurroundingRectangle(matrix_C.entries[0][0], color=YELLOW)

        # Add the matrices to the scene
        self.play(Write(matrix_A), Write(matrix_B), Write(matrix_C))
        self.play(Create(c11_rect))
        self.wait(0.5)

        # Highlight row 1 of A
        row_1_A_rect = SurroundingRectangle(VGroup(*matrix_A.entries[0]), color=GREEN)
        self.play(Create(row_1_A_rect))
        self.wait(0.3)

        # Highlight column 1 of B
        col_1_B_rect = SurroundingRectangle(VGroup(matrix_B.entries[0][0], matrix_B.entries[1][0]), color=BLUE)
        self.play(Create(col_1_B_rect))
        self.wait(0.3)

        # Arrows and multiplication
        a11 = matrix_A.entries[0][0].copy()
        b11 = matrix_B.entries[0][0].copy()
        a12 = matrix_A.entries[0][1].copy()
        b21 = matrix_B.entries[1][0].copy()

        arrow1 = Arrow(a11.get_center(), UP * 2 + LEFT * 2, buff=0)
        arrow2 = Arrow(b11.get_center(), UP * 2 + RIGHT * 2, buff=0)
        self.play(Create(arrow1), Create(arrow2))
        self.wait(0.2)

        product1 = MathTex(f"{matrix_A_data[0][0]} \\times {matrix_B_data[0][0]} = {matrix_A_data[0][0] * matrix_B_data[0][0]}").move_to(DOWN * 2 + LEFT * 3)
        self.play(Write(product1))
        self.wait(0.3)

        arrow3 = Arrow(a12.get_center(), DOWN * 2 + LEFT * 2, buff=0)
        arrow4 = Arrow(b21.get_center(), DOWN * 2 + RIGHT * 2, buff=0)
        self.play(Create(arrow3), Create(arrow4))
        self.wait(0.2)

        product2 = MathTex(f"{matrix_A_data[0][1]} \\times {matrix_B_data[1][0]} = {matrix_A_data[0][1] * matrix_B_data[1][0]}").move_to(DOWN * 2 + RIGHT * 3)
        self.play(Write(product2))
        self.wait(0.3)

        plus_sign = MathTex("+").move_to(DOWN * 2)
        self.play(Write(plus_sign))
        self.wait(0.2)

        sum_result = matrix_A_data[0][0] * matrix_B_data[0][0] + matrix_A_data[0][1] * matrix_B_data[1][0]
        sum_text = MathTex(str(sum_result)).move_to(matrix_C.entries[0][0].get_center())
        self.play(Transform(VGroup(product1, product2, plus_sign), sum_text))
        self.wait(0.5)

        # Pause for reinforcement
        self.wait(2)
```