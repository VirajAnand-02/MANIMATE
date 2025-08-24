import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox(
        "Matrix Multiplication: The Basics",
        self.title_region.width * 0.9,
        self.title_region.height * 0.8
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(3) # Welcome to our deep dive into matrix multiplication! Matrices are powerful tools for organizing data, and knowing how to multiply them is key.

        # 2. Display two simple 2x2 matrices, A and B
        matrix_a = MathTex(
        r"\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}",
        font_size=60
        )
        matrix_b = MathTex(
        r"\begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}",
        font_size=60
        )
        label_a = MathTex("A =", font_size=60).next_to(matrix_a, LEFT, buff=0.2)
        label_b = MathTex("B =", font_size=60).next_to(matrix_b, LEFT, buff=0.2)

        # Group labels with matrices for easier arrangement
        group_a = VGroup(label_a, matrix_a)
        group_b = VGroup(label_b, matrix_b)

        # Arrange them side by side in the main region
        matrices_group = VGroup(group_a, group_b).arrange(RIGHT, buff=1.5)
        matrices_group.move_to(self.main_region.get_center())

        self.play(FadeIn(matrices_group))
        self.wait(2) # Display two simple 2x2 matrices, A and B.

        # 3. Show a quick visual attempt to multiply them element-wise
        equals_sign = MathTex("=", font_size=60).next_to(group_b, RIGHT, buff=0.5)

        # Element-wise product expression
        matrix_c_element_wise_expr = MathTex(
        r"\begin{pmatrix} 1 \times 5 & 2 \times 6 \\ 3 \times 7 & 4 \times 8 \end{pmatrix}",
        font_size=60
        )
        matrix_c_element_wise_expr.next_to(equals_sign, RIGHT, buff=0.5)

        self.play(Write(equals_sign), Write(matrix_c_element_wise_expr))
        self.wait(5) # But unlike scalar multiplication or even matrix addition, matrix multiplication isn't done element by element.

        # Element-wise product result
        matrix_c_element_wise_result = MathTex(
        r"\begin{pmatrix} 5 & 12 \\ 21 & 32 \end{pmatrix}",
        font_size=60
        )
        matrix_c_element_wise_result.move_to(matrix_c_element_wise_expr.get_center())

        self.play(Transform(matrix_c_element_wise_expr, matrix_c_element_wise_result))
        self.wait(1)

        # Show an 'X' or 'NO' symbol appearing over the result
        x_mark = Cross(matrix_c_element_wise_expr, stroke_width=8, color=RED)
        no_text = Text("NO", font_size=96, color=RED).move_to(matrix_c_element_wise_expr.get_center())

        self.play(Create(x_mark), FadeIn(no_text))
        self.wait(5) # That's a common mistake!

        # 4. Transition to a large question mark
        self.play(
        FadeOut(matrices_group),
        FadeOut(equals_sign),
        FadeOut(matrix_c_element_wise_expr), # This is now the result mobject
        FadeOut(x_mark),
        FadeOut(no_text)
        )
        self.wait(1)

        question_mark = Text("?", font_size=200, color=YELLOW)
        question_mark.move_to(self.main_region.get_center())
        self.play(Write(question_mark))
        self.wait(11) # Instead, it follows a unique 'row by column' rule that we'll unravel today. Get ready to transform your understanding of matrices!

# Set narration and duration
Scene1.narration_text = '''Welcome to our deep dive into matrix multiplication! Matrices are powerful tools for organizing data, and knowing how to multiply them is key. But unlike scalar multiplication or even matrix addition, matrix multiplication isn\'t done element by element. That\'s a common mistake! Instead, it follows a unique \'row by column\' rule that we\'ll unravel today. Get ready to transform your understanding of matrices!'''
Scene1.audio_duration = 5.0
