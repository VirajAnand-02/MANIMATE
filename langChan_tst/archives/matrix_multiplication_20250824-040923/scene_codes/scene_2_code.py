import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        # Define matrix data
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]
        matrix_c_data = [["?", "?"], ["?", "?"]]

        # 1. Create the title text and place it in the left region
        title = self.create_textbox("Matrix Multiplication: Row by Column", width=self.left_region.width * 0.9, height=self.left_region.height * 0.2)
        title.move_to(self.left_region.get_center() + UP * self.left_region.height * 0.3)
        self.play(Write(title), run_time=2)
        self.wait(2)

        # 2. Display Matrix A, Matrix B, and an empty Result Matrix C
        matrix_a = Matrix(matrix_a_data)
        matrix_b = Matrix(matrix_b_data)
        matrix_c = Matrix(matrix_c_data)

        equals = MathTex("=")
        times = MathTex("\\times")

        # Arrange matrices horizontally
        matrix_group = HGroup(matrix_a, times, matrix_b, equals, matrix_c).arrange(buff=0.7)
        matrix_group.move_to(self.right_region.get_center())

        self.play(FadeIn(matrix_group), run_time=3)
        self.wait(4) # Narration: "The core principle of matrix multiplication is the 'row by column' dot product."

        # 3. Highlight Row 1 of A and Column 1 of B (for C_11)
        row1_a = matrix_a.get_rows()[0]
        col1_b = matrix_b.get_columns()[0]

        rect_a = SurroundingRectangle(row1_a, color=YELLOW)
        rect_b = SurroundingRectangle(col1_b, color=BLUE)

        self.play(Create(rect_a), Create(rect_b), run_time=3.5)
        self.wait(4) # Narration: "To find an element in the resulting matrix, say C_ij, you take the i-th row of the first matrix and the j-th column of the second matrix."

        # Get individual elements for arrows
        a11 = matrix_a.get_entries()[0][0]
        a12 = matrix_a.get_entries()[0][1]
        b11 = matrix_b.get_entries()[0][0]
        b21 = matrix_b.get_entries()[1][0]

        # 4. Show arrows connecting corresponding elements
        arrow1 = Arrow(a11.get_right(), b11.get_left(), buff=0.1, color=YELLOW, max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2)
        arrow2 = Arrow(a12.get_right(), b21.get_left(), buff=0.1, color=BLUE, max_stroke_width_to_length_ratio=0.05, max_tip_length_to_length_ratio=0.2)

        self.play(Create(arrow1), Create(arrow2), run_time=3)
        self.wait(3) # Narration: "Then, you multiply corresponding elements and sum those products."

        # 5. Display the calculation
        result_val = (matrix_a_data[0][0] * matrix_b_data[0][0]) + (matrix_a_data[0][1] * matrix_b_data[1][0])
        calc_expression = MathTex(
        f"({matrix_a_data[0][0]} \\times {matrix_b_data[0][0]}) + ({matrix_a_data[0][1]} \\times {matrix_b_data[1][0]})",
        font_size=40
        )
        calc_expression.next_to(matrix_group, DOWN, buff=1)

        self.play(Write(calc_expression), run_time=4)
        self.wait(3) # Narration: "This sum gives you a single element in your new matrix."

        # 6. Display the calculated value and populate C[1,1]
        result_mobject = MathTex(f"= {result_val}", font_size=40).next_to(calc_expression, RIGHT)
        self.play(Write(result_mobject), run_time=2)
        self.wait(3) # Narration: "This sum gives you a single element in your new matrix."

        c_11_target_pos = matrix_c.get_entries()[0][0].get_center()
        c_11_value = MathTex(str(result_val)).move_to(c_11_target_pos)

        self.play(
        FadeOut(rect_a, rect_b, arrow1, arrow2, calc_expression),
        TransformFromCopy(result_mobject, c_11_value),
        run_time=3.5
        )
        self.wait(4) # Narration: "Let's look at an example: how to get the first element, C_11."

# Set narration and duration
Scene2.narration_text = '''The core principle of matrix multiplication is the \'row by column\' dot product. To find an element in the resulting matrix, say C_ij, you take the i-th row of the first matrix and the j-th column of the second matrix. Then, you multiply corresponding elements and sum those products. This sum gives you a single element in your new matrix. Let\'s look at an example: how to get the first element, C_11.'''
Scene2.audio_duration = 5.0
