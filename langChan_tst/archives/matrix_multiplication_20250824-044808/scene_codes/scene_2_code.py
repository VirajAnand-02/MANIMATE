import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication: Rows by Columns", width=self.left_region.width, height=self.title_region.height)
        title.move_to(self.title_region.get_center())

        matrix_a = MathTex(
        r"\begin{bmatrix} a_{11} & a_{12} & \cdots & a_{1n} \\ a_{21} & a_{22} & \cdots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \cdots & a_{mn} \end{bmatrix}"
        )
        matrix_b = MathTex(
        r"\begin{bmatrix} b_{11} & b_{12} & \cdots & b_{1p} \\ b_{21} & b_{22} & \cdots & b_{2p} \\ \vdots & \vdots & \ddots & \vdots \\ b_{n1} & b_{n2} & \cdots & b_{np} \end{bmatrix}"
        )
        matrix_c = MathTex(
        r"\begin{bmatrix} c_{11} & \cdots \\ \vdots & \ddots \end{bmatrix}"
        )

        matrix_a.move_to(self.left_region.get_center() + LEFT * 1.5)
        matrix_b.move_to(self.left_region.get_center() + RIGHT * 1.5)
        matrix_c.move_to(self.right_region.get_center())

        self.play(Write(matrix_a), Write(matrix_b), Write(matrix_c))
        self.wait(1)

        row_a = Rectangle(width=matrix_a.width, height=matrix_a[0][0].height * 0.8)
        row_a.move_to(matrix_a[0][0].get_center()).shift(UP * (matrix_a[0][0].height * 1.5))
        row_a.set_color(YELLOW)

        col_b = Rectangle(width=matrix_b[0][0].width * 0.8, height=matrix_b.height)
        col_b.move_to(matrix_b[0][0].get_center()).shift(LEFT * (matrix_b[0][0].width * 1.5))
        col_b.set_color(GREEN)

        self.play(Create(row_a), Create(col_b))
        self.wait(1)

        arrow1 = Arrow(row_a.get_left(), col_b.get_top(), buff=0.2)
        arrow2 = Arrow(row_a.get_center(), col_b.get_center(), buff=0.2)
        arrow3 = Arrow(row_a.get_right(), col_b.get_bottom(), buff=0.2)

        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.wait(1)

        mult1 = MathTex("a_{11} \\cdot b_{11}")
        mult2 = MathTex("a_{12} \\cdot b_{21}")
        multn = MathTex("a_{1n} \\cdot b_{n1}")
        sum_text = MathTex("a_{11} \\cdot b_{11} + a_{12} \\cdot b_{21} + \\cdots + a_{1n} \\cdot b_{n1}")

        mult1.next_to(arrow1, DOWN)
        mult2.next_to(arrow2, DOWN)
        multn.next_to(arrow3, DOWN)
        sum_text.next_to(mult2, DOWN)

        self.play(Write(mult1), Write(mult2), Write(multn))
        self.wait(1)

        self.play(Write(sum_text))
        self.wait(1)

        c11 = matrix_c[0][0]
        arrow_to_c = Arrow(sum_text.get_center(), c11.get_center(), buff=0.2)
        self.play(Create(arrow_to_c))
        self.wait(1)

        self.play(FadeOut(row_a, col_b, arrow1, arrow2, arrow3, mult1, mult2, multn, sum_text, arrow_to_c))
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''So, how do we actually multiply them? It\'s all about \'rows by columns.\' To find a single element in the resulting product matrix, say at position (i, j), you take the i-th row of the first matrix and multiply it by the j-th column of the second matrix. This isn\'t just multiplying corresponding elements; it\'s a \'dot product.\' You multiply the first element of the row by the first element of the column, the second element of the row by the second element of the column, and so on. Then, you sum all those products together. This sum gives you just one single element in your new matrix. Let\'s visualize this process.'''
Scene2.audio_duration = 5.0
