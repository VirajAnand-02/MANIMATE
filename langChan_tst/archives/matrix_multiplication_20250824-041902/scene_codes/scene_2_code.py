import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Define matrices A and B
        matrix_a = MathTex(r"\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}", font_size=60)
        matrix_b = MathTex(r"\begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}", font_size=60)
        mult_sign = MathTex(r"\times", font_size=60)

        # Group and position matrices A and B in the left region
        left_group = VGroup(matrix_a, mult_sign, matrix_b).arrange(RIGHT, buff=0.7)
        left_group.move_to(self.left_region.get_center())

        # Define the title for the right region
        c11_title = self.create_textbox(
        "Calculating C_{11}",
        width=self.right_region.width * 0.8,
        height=0.5
        )
        c11_title.move_to(self.right_region.get_top() + DOWN * c11_title.height / 2)

        # Define the blank result matrix C
        result_matrix_c = MathTex(r"\begin{pmatrix} ? & ? \\ ? & ? \end{pmatrix}", font_size=60)
        result_matrix_c.move_to(self.right_region.get_center() + DOWN * self.right_region.height / 3)

        # --- Animation Sequence ---

        # 1. Display matrices A and B on the left
        self.play(Write(left_group), run_time=2)

        # 2. Display the calculation title and blank result matrix on the right
        self.play(Write(c11_title), Create(result_matrix_c), run_time=2)
        self.wait(3) # Wait for initial narration about matrix multiplication

        # 3. Highlight the first row of A and the first column of B
        # MathTex indexing: matrix_a[1] is '1', matrix_a[3] is '2'
        # matrix_b[1] is '5', matrix_b[5] is '7'
        row1_a = VGroup(matrix_a[1], matrix_a[3])
        col1_b = VGroup(matrix_b[1], matrix_b[5])
        self.play(Indicate(row1_a, color=YELLOW), Indicate(col1_b, color=YELLOW), run_time=2)

        # 4. Show arrows connecting corresponding elements and display the initial calculation
        arrow1 = Arrow(matrix_a[1].get_right(), matrix_b[1].get_left(), buff=0.1, color=GREEN)
        arrow2 = Arrow(matrix_a[3].get_right(), matrix_b[5].get_left(), buff=0.1, color=GREEN)

        calc_text = MathTex(r"(1 \times 5) + (2 \times 7)", font_size=50)
        calc_text.next_to(c11_title, DOWN, buff=1)

        self.play(Create(arrow1), Create(arrow2), Write(calc_text), run_time=3)
        self.wait(2) # Wait for "dot product" explanation

        # 5. Show the intermediate sum
        intermediate_sum = MathTex(r"5 + 14", font_size=50)
        intermediate_sum.move_to(calc_text)
        self.play(Transform(calc_text, intermediate_sum), run_time=2)

        # 6. Show the final result
        final_result = MathTex(r"19", font_size=50)
        final_result.move_to(calc_text)
        self.play(Transform(calc_text, final_result), run_time=2)

        # 7. Place '19' into the C_11 position of the result matrix
        # result_matrix_c[1] is the first '?'
        c11_value = MathTex("19", font_size=60).move_to(result_matrix_c[1])
        self.play(Transform(result_matrix_c[1], c11_value), run_time=2)
        self.wait(3)

# Set narration and duration
Scene2.narration_text = '''The key to matrix multiplication lies in calculating each individual element of the resulting matrix. For an element at position (i, j) in the product matrix C, we take the i-th row of the first matrix, A, and the j-th column of the second matrix, B. We then multiply corresponding elements from that row and column, and sum up all those products. This is often called a \'dot product\'. Let\'s see it in action for one element, C_11.'''
Scene2.audio_duration = 5.0
