import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title = self.create_textbox("Matrix Multiplication Example", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(1)

        # Matrices
        matrix_a = MathTex(r"A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}").move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b = MathTex(r"B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}").move_to(self.main_region.get_center() + RIGHT * 3)
        matrix_c = MathTex(r"C = \begin{bmatrix} \quad & \quad \\ \quad & \quad \end{bmatrix}").move_to(self.main_region.get_center())

        self.play(Write(matrix_a), Write(matrix_b), Write(matrix_c))
        self.wait(1)

        # C11
        rect_a_row1 = Rectangle(width=2, height=0.7, color=YELLOW).move_to(matrix_a[0][2:4].get_center()).shift(UP * 0.35)
        rect_b_col1 = Rectangle(width=0.7, height=2, color=YELLOW).move_to(matrix_b[0][2:5:3].get_center()).shift(LEFT * 0.35)
        self.play(Create(rect_a_row1), Create(rect_b_col1))
        c11_calc = MathTex(r"(1 \times 5) + (2 \times 7) = 5 + 14 = 19").move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Write(c11_calc))
        self.wait(1)
        c11_val = MathTex(r"19").move_to(matrix_c[0][2].get_center())
        self.play(Transform(c11_calc, c11_val))
        self.play(FadeOut(rect_a_row1), FadeOut(rect_b_col1))
        self.wait(0.5)

        # C12
        rect_a_row1 = Rectangle(width=2, height=0.7, color=YELLOW).move_to(matrix_a[0][2:4].get_center()).shift(UP * 0.35)
        rect_b_col2 = Rectangle(width=0.7, height=2, color=YELLOW).move_to(matrix_b[0][3:6:3].get_center()).shift(RIGHT * 0.35)
        self.play(Create(rect_a_row1), Create(rect_b_col2))
        c12_calc = MathTex(r"(1 \times 6) + (2 \times 8) = 6 + 16 = 22").move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Transform(c11_calc, c12_calc))
        self.wait(1)
        c12_val = MathTex(r"22").move_to(matrix_c[0][3].get_center())
        self.play(Transform(c12_calc, c12_val))
        self.play(FadeOut(rect_a_row1), FadeOut(rect_b_col2))
        self.wait(0.5)

        # C21
        rect_a_row2 = Rectangle(width=2, height=0.7, color=YELLOW).move_to(matrix_a[0][5:7].get_center()).shift(DOWN * 0.35)
        rect_b_col1 = Rectangle(width=0.7, height=2, color=YELLOW).move_to(matrix_b[0][2:5:3].get_center()).shift(LEFT * 0.35)
        self.play(Create(rect_a_row2), Create(rect_b_col1))
        c21_calc = MathTex(r"(3 \times 5) + (4 \times 7) = 15 + 28 = 43").move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Transform(c12_val, c21_calc))
        self.wait(1)
        c21_val = MathTex(r"43").move_to(matrix_c[0][6].get_center())
        self.play(Transform(c21_calc, c21_val))
        self.play(FadeOut(rect_a_row2), FadeOut(rect_b_col1))
        self.wait(0.5)

        # C22
        rect_a_row2 = Rectangle(width=2, height=0.7, color=YELLOW).move_to(matrix_a[0][5:7].get_center()).shift(DOWN * 0.35)
        rect_b_col2 = Rectangle(width=0.7, height=2, color=YELLOW).move_to(matrix_b[0][3:6:3].get_center()).shift(RIGHT * 0.35)
        self.play(Create(rect_a_row2), Create(rect_b_col2))
        c22_calc = MathTex(r"(3 \times 6) + (4 \times 8) = 18 + 32 = 50").move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Transform(c21_val, c22_calc))
        self.wait(1)
        c22_val = MathTex(r"50").move_to(matrix_c[0][7].get_center())
        self.play(Transform(c22_calc, c22_val))
        self.play(FadeOut(rect_a_row2), FadeOut(rect_b_col2))
        self.wait(0.5)

        # Final Matrix C
        matrix_c_final = MathTex(r"C = \begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}").move_to(self.main_region.get_center())
        self.play(Transform(matrix_c, matrix_c_final))
        self.wait(1)

        # Recap
        recap_text1 = Text("Dimensions must match!", color=GREEN).move_to(self.main_region.get_center() + UP * 2)
        recap_text2 = Text("Row by Column!", color=GREEN).move_to(self.main_region.get_center() + DOWN * 2)
        self.play(Write(recap_text1), Write(recap_text2))
        self.wait(2)

        self.play(FadeOut(matrix_a), FadeOut(matrix_b), FadeOut(matrix_c_final), FadeOut(recap_text1), FadeOut(recap_text2), FadeOut(title))
        self.wait(1)

# Set narration and duration
Scene4.narration_text = '''Let\'s walk through a complete example. Here we have matrix A, a 2x2, and matrix B, also a 2x2. First, check compatibility: 2 columns of A match 2 rows of B, so our result C will be a 2x2 matrix. To find C11, we take row 1 of A and column 1 of B: (1 times 5) plus (2 times 7) equals 5 plus 14, which is 19. For C12, row 1 of A and column 2 of B: (1 times 6) plus (2 times 8) equals 6 plus 16, which is 22. For C21, row 2 of A and column 1 of B: (3 times 5) plus (4 times 7) equals 15 plus 28, which is 43. And finally, for C22, row 2 of A and column 2 of B: (3 times 6) plus (4 times 8) equals 18 plus 32, which is 50. So, our final matrix C is [[19, 22], [43, 50]]. Remember: check dimensions, then row by column, multiply and sum!'''
Scene4.audio_duration = 5.0
