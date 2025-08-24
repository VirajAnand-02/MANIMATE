import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene4(SplitScreen):
    def construct_scene(self):
        # 1. Title
        title_text = self.create_textbox("Matrix Multiplication: Dimension Check", self.left_region.width * 0.9, self.left_region.height * 0.2)
        title_text.move_to(self.left_region.get_center())
        self.play(FadeIn(title_text))
        self.wait(0.5)

        # 2. Valid Multiplication Example (A 2x3, B 3x2)
        matrix_A_dims = MathTex(r"A_{2 \times 3}", font_size=72)
        matrix_B_dims = MathTex(r"B_{3 \times 2}", font_size=72)

        # Arrange them in the right region
        matrix_group_1 = HGroup(matrix_A_dims, MathTex(r"\times", font_size=72), matrix_B_dims, buff=0.5)
        matrix_group_1.scale_to_fit_width(self.right_region.width * 0.8)
        matrix_group_1.move_to(self.right_region.get_center() + UP * 1.5)

        self.play(FadeIn(matrix_group_1))
        self.wait(1)

        # Highlight inner dimensions (3 and 3)
        # A_{2 \times 3} -> index 5 is '3'
        # B_{3 \times 2} -> index 3 is '3'
        inner_dim_A = matrix_A_dims[0][5]
        inner_dim_B = matrix_B_dims[0][3]

        rect_inner_A = SurroundingRectangle(inner_dim_A, color=YELLOW, buff=0.1)
        rect_inner_B = SurroundingRectangle(inner_dim_B, color=YELLOW, buff=0.1)

        check_mark = Check(color=GREEN).scale(0.8).next_to(matrix_group_1, DOWN, buff=0.5)

        self.play(Create(rect_inner_A), Create(rect_inner_B))
        self.wait(0.5)
        self.play(FadeIn(check_mark))
        self.wait(1)

        # Show result dimensions
        result_dims_text = MathTex(r"\rightarrow C_{2 \times 2}", font_size=72, color=BLUE)
        result_dims_text.next_to(check_mark, DOWN, buff=0.5)

        # A_{2 \times 3} -> index 3 is '2'
        # B_{3 \times 2} -> index 5 is '2'
        outer_dim_A = matrix_A_dims[0][3]
        outer_dim_B = matrix_B_dims[0][5]

        rect_outer_A = SurroundingRectangle(outer_dim_A, color=BLUE, buff=0.1)
        rect_outer_B = SurroundingRectangle(outer_dim_B, color=BLUE, buff=0.1)

        self.play(
        FadeOut(rect_inner_A), FadeOut(rect_inner_B), FadeOut(check_mark),
        Create(rect_outer_A), Create(rect_outer_B),
        FadeIn(result_dims_text)
        )
        self.wait(2)

        self.play(FadeOut(matrix_group_1), FadeOut(rect_outer_A), FadeOut(rect_outer_B), FadeOut(result_dims_text))
        self.wait(0.5)

        # 3. Invalid Multiplication Example (A 2x4, B 3x2)
        matrix_A_dims_bad = MathTex(r"A_{2 \times 4}", font_size=72)
        matrix_B_dims_bad = MathTex(r"B_{3 \times 2}", font_size=72)

        matrix_group_2 = HGroup(matrix_A_dims_bad, MathTex(r"\times", font_size=72), matrix_B_dims_bad, buff=0.5)
        matrix_group_2.scale_to_fit_width(self.right_region.width * 0.8)
        matrix_group_2.move_to(self.right_region.get_center() + UP * 1.5)

        self.play(FadeIn(matrix_group_2))
        self.wait(1)

        # Highlight inner dimensions (4 and 3)
        # A_{2 \times 4} -> index 5 is '4'
        # B_{3 \times 2} -> index 3 is '3'
        inner_dim_A_bad = matrix_A_dims_bad[0][5]
        inner_dim_B_bad = matrix_B_dims_bad[0][3]

        rect_inner_A_bad = SurroundingRectangle(inner_dim_A_bad, color=RED, buff=0.1)
        rect_inner_B_bad = SurroundingRectangle(inner_dim_B_bad, color=RED, buff=0.1)

        x_mark = Cross(color=RED).scale(0.8).next_to(matrix_group_2, DOWN, buff=0.5)
        error_text = Text("Error: Cannot Multiply", color=RED, font_size=48).next_to(x_mark, DOWN, buff=0.5)

        self.play(Create(rect_inner_A_bad), Create(rect_inner_B_bad))
        self.wait(0.5)
        self.play(FadeIn(x_mark), Write(error_text))
        self.wait(2)

        self.play(FadeOut(matrix_group_2), FadeOut(rect_inner_A_bad), FadeOut(rect_inner_B_bad), FadeOut(x_mark), FadeOut(error_text))
        self.wait(0.5)

        # 4. Summary Graphic
        summary_formula = MathTex(r"A_{m \times \textbf{n}} \cdot B_{\textbf{n} \times p} = C_{m \times p}", font_size=72)
        summary_formula.scale_to_fit_width(self.right_region.width * 0.9)
        summary_formula.move_to(self.right_region.get_center() + UP * 1.5)

        # Highlight matching 'n's
        matching_n_A = summary_formula.get_part_by_tex(r"\textbf{n}")[0] # First bold n
        matching_n_B = summary_formula.get_part_by_tex(r"\textbf{n}")[1] # Second bold n

        rect_n_A = SurroundingRectangle(matching_n_A, color=YELLOW, buff=0.1)
        rect_n_B = SurroundingRectangle(matching_n_B, color=YELLOW, buff=0.1)

        # Highlight outer 'm' and 'p'
        outer_m = summary_formula.get_part_by_tex("m")[0]
        outer_p = summary_formula.get_part_by_tex("p")[0]

        rect_m = SurroundingRectangle(outer_m, color=BLUE, buff=0.1)
        rect_p = SurroundingRectangle(outer_p, color=BLUE, buff=0.1)

        rule_text = Text("Inner Dimensions MUST Match!", color=YELLOW, font_size=40).next_to(summary_formula, DOWN, buff=0.5)
        result_text = Text("Outer Dimensions give Result Size", color=BLUE, font_size=40).next_to(rule_text, DOWN, buff=0.3)
        dot_product_rule = Text("Each Element: Row by Column Dot Product", font_size=36).next_to(result_text, DOWN, buff=0.5)

        self.play(FadeIn(summary_formula))
        self.wait(1)
        self.play(
        Create(rect_n_A), Create(rect_n_B),
        Write(rule_text)
        )
        self.wait(1.5)
        self.play(
        FadeOut(rect_n_A), FadeOut(rect_n_B),
        Create(rect_m), Create(rect_p),
        Write(result_text)
        )
        self.wait(1.5)
        self.play(
        FadeOut(rect_m), FadeOut(rect_p),
        Write(dot_product_rule)
        )
        self.wait(2)

        self.play(FadeOut(title_text), FadeOut(summary_formula), FadeOut(rule_text), FadeOut(result_text), FadeOut(dot_product_rule))
        self.wait(0.5)

# Set narration and duration
Scene4.narration_text = '''Before you multiply, always check the dimensions! For matrix multiplication A * B to be possible, the number of columns in matrix A must equal the number of rows in matrix B. If A is an m x n matrix and B is an n x p matrix, then their product C will be an m x p matrix. The \'inner\' dimensions must match, and the \'outer\' dimensions give you the size of the result. So, remember: check dimensions, then it\'s row by column dot product for each element. Keep practicing, and you\'ll master matrix multiplication!'''
Scene4.audio_duration = 5.0
