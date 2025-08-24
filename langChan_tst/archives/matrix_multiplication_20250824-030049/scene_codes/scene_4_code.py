import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication Example", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(1)

        # Define matrices A and B
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]

        # Create MathTex objects for matrices A and B
        matrix_a = MathTex(
        r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}",
        tex_template=TexTemplateLibrary.simple_equations,
        ).move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b = MathTex(
        r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}",
        tex_template=TexTemplateLibrary.simple_equations,
        ).move_to(self.main_region.get_center() + RIGHT * 3)

        # Create MathTex object for the equals sign
        equals_sign = MathTex("=").move_to(self.main_region.get_center())

        # Display matrices A and B and the equals sign
        self.play(Write(matrix_a), Write(matrix_b), Write(equals_sign))
        self.wait(1)

        # Create MathTex object for the resulting matrix C (calculation)
        matrix_c_calculation = MathTex(
        r"\begin{bmatrix} (1 \cdot 5 + 2 \cdot 7) & (1 \cdot 6 + 2 \cdot 8) \\ (3 \cdot 5 + 4 \cdot 7) & (3 \cdot 6 + 4 \cdot 8) \end{bmatrix}",
        tex_template=TexTemplateLibrary.simple_equations,
        ).move_to(self.main_region.get_center() + DOWN * 2)

        # Display the calculation for matrix C
        self.play(Write(matrix_c_calculation))
        self.wait(2)

        # Create MathTex object for the resulting matrix C (result)
        matrix_c_result = MathTex(
        r"\begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}",
        tex_template=TexTemplateLibrary.simple_equations,
        ).move_to(self.main_region.get_center() + DOWN * 2)

        # Replace the calculation with the result
        self.play(ReplacementTransform(matrix_c_calculation, matrix_c_result))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''Let\'s walk through a complete example. We have a 2x2 matrix A and a 2x2 matrix B. We\'ll calculate each element of the resulting matrix C step-by-step, showing the dot product calculation for each position. Pay close attention to which row and column are being used.'''
Scene4.audio_duration = 5.0
