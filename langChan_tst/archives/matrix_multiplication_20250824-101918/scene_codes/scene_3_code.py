```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices
        matrix_a = MathTex(r"A = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}").shift(UP * 2.5 + LEFT * 3.5)
        matrix_b = MathTex(r"B = \begin{bmatrix} b_{11} & b_{12} \\ b_{21} & b_{22} \end{bmatrix}").shift(UP * 2.5 + RIGHT * 3.5)
        matrix_c = MathTex(r"C = \begin{bmatrix} \quad & \quad \\ \quad & \quad \end{bmatrix}").shift(DOWN * 0.5)

        self.play(Write(matrix_a), Write(matrix_b), Write(matrix_c))
        self.wait(1)

        # Step 1: C11
        rect_a1 = Rectangle(width=2.0, height=0.7, color=YELLOW).move_to(matrix_a[0][2:4]).shift(DOWN*0.05)
        rect_b1 = Rectangle(width=0.7, height=2.0, color=YELLOW).move_to(matrix_b[0][2:5]).shift(RIGHT*0.05)
        c11_calc = MathTex(r"(a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21})").next_to(matrix_c, DOWN, buff=0.7)
        c11_result = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & \quad \\ \quad & \quad \end{bmatrix}").move_to(matrix_c.get_center())

        self.play(Create(rect_a1), Create(rect_b1))
        self.play(Write(c11_calc))
        self.wait(2)
        self.play(Transform(matrix_c, c11_result), FadeOut(rect_a1), FadeOut(rect_b1), FadeOut(c11_calc))
        self.wait(1)

        # Step 2: C12
        matrix_c_temp = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & \quad \\ \quad & \quad \end{bmatrix}").move_to(matrix_c.get_center())
        rect_a2 = Rectangle(width=2.0, height=0.7, color=YELLOW).move_to(matrix_a[0][2:4]).shift(DOWN*0.05)
        rect_b2 = Rectangle(width=0.7, height=2.0, color=YELLOW).move_to(matrix_b[0][6:9]).shift(LEFT*0.05)
        c12_calc = MathTex(r"(a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22})").next_to(matrix_c, DOWN, buff=0.7)
        c12_result = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & (a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22}) \\ \quad & \quad \end{bmatrix}").move_to(matrix_c.get_center())

        self.play(Transform(matrix_c, matrix_c_temp), Create(rect_a2), Create(rect_b2))
        self.play(Write(c12_calc))
        self.wait(2)
        self.play(Transform(matrix_c, c12_result), FadeOut(rect_a2), FadeOut(rect_b2), FadeOut(c12_calc))
        self.wait(1)

        # Step 3: C21
        matrix_c_temp2 = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & (a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22}) \\ \quad & \quad \end{bmatrix}").move_to(matrix_c.get_center())
        rect_a3 = Rectangle(width=2.0, height=0.7, color=YELLOW).move_to(matrix_a[0][6:8]).shift(UP*0.05)
        rect_b3 = Rectangle(width=0.7, height=2.0, color=YELLOW).move_to(matrix_b[0][2:5]).shift(RIGHT*0.05)
        c21_calc = MathTex(r"(a_{21} \cdot b_{11}) + (a_{22} \cdot b_{21})").next_to(matrix_c, DOWN, buff=0.7)
        c21_result = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & (a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22}) \\ (a_{21} \cdot b_{11}) + (a_{22} \cdot b_{21}) & \quad \end{bmatrix}").move_to(matrix_c.get_center())

        self.play(Transform(matrix_c, matrix_c_temp2), Create(rect_a3), Create(rect_b3))
        self.play(Write(c21_calc))
        self.wait(2)
        self.play(Transform(matrix_c, c21_result), FadeOut(rect_a3), FadeOut(rect_b3), FadeOut(c21_calc))
        self.wait(1)

        # Step 4: C22
        matrix_c_temp3 = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & (a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22}) \\ (a_{21} \cdot b_{11}) + (a_{22} \cdot b_{21}) & \quad \end{bmatrix}").move_to(matrix_c.get_center())
        rect_a4 = Rectangle(width=2.0, height=0.7, color=YELLOW).move_to(matrix_a[0][6:8]).shift(UP*0.05)
        rect_b4 = Rectangle(width=0.7, height=2.0, color=YELLOW).move_to(matrix_b[0][6:9]).shift(LEFT*0.05)
        c22_calc = MathTex(r"(a_{21} \cdot b_{12}) + (a_{22} \cdot b_{22})").next_to(matrix_c, DOWN, buff=0.7)
        c22_result = MathTex(r"C = \begin{bmatrix} (a_{11} \cdot b_{11}) + (a_{12} \cdot b_{21}) & (a_{11} \cdot b_{12}) + (a_{12} \cdot b_{22}) \\ (a_{21} \cdot b_{11}) + (a_{22} \cdot b_{21}) & (a_{21} \cdot b_{12}) + (a_{22} \cdot b_{22}) \end{bmatrix}").move_to(matrix_c.get_center())

        self.play(Transform(matrix_c, matrix_c_temp3), Create(rect_a4), Create(rect_b4))
        self.play(Write(c22_calc))
        self.wait(2)
        self.play(Transform(matrix_c, c22_result), FadeOut(rect_a4), FadeOut(rect_b4), FadeOut(c22_calc))
        self.wait(3)
```