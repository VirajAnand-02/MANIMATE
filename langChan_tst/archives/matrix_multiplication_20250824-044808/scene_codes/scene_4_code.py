import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title = self.create_textbox("Matrix Multiplication Recap", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(1)

        # Compatibility Rule
        matrix_a = MathTex(r"A_{(m \times n)}", color=BLUE).move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b = MathTex(r"B_{(n \times p)}", color=GREEN).move_to(self.main_region.get_center())
        arrow = Arrow(matrix_a.get_right(), matrix_b.get_left(), buff=0.1)
        matrix_c = MathTex(r"C_{(m \times p)}", color=YELLOW).move_to(self.main_region.get_center() + RIGHT * 3)
        arrow2 = Arrow(matrix_b.get_right(), matrix_c.get_left(), buff=0.1)

        self.play(Create(matrix_a), Create(matrix_b))
        self.play(Create(arrow))
        self.play(Create(matrix_c), Create(arrow2))
        self.wait(1)

        group = VGroup(matrix_a, matrix_b, arrow, matrix_c, arrow2)
        self.play(FadeOut(group))

        # Row-by-Column Dot Product
        matrix_1 = Matrix([["a", "b"], ["c", "d"]]).scale(0.7).move_to(self.main_region.get_center() + LEFT * 2)
        matrix_2 = Matrix([["e", "f"], ["g", "h"]]).scale(0.7).move_to(self.main_region.get_center() + RIGHT * 2)
        result_matrix = Matrix([[" ", " "], [" ", " "]]).scale(0.7).move_to(self.main_region.get_center() + DOWN * 2)

        row = SurroundingRectangle(matrix_1.get_rows()[0], color=BLUE)
        col = SurroundingRectangle(matrix_2.get_columns()[0], color=GREEN)
        element = SurroundingRectangle(result_matrix.get_entries()[0], color=YELLOW)

        self.play(Create(matrix_1), Create(matrix_2), Create(result_matrix))
        self.play(Create(row), Create(col), Create(element))
        self.wait(1)

        group2 = VGroup(matrix_1, matrix_2, result_matrix, row, col, element)
        self.play(FadeOut(group2))

        # Application Icons
        cube = Cube(side_length=2, fill_color=RED, fill_opacity=0.5).move_to(self.main_region.get_center() + LEFT * 3)
        network = NeuralNetworkMobject([3, 4, 2]).scale(0.7).move_to(self.main_region.get_center())
        calculator = Calculator().scale(0.7).move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Create(cube), Create(network), Create(calculator))
        self.play(Rotate(cube, angle=TAU, axis=OUT, run_time=2, rate_func=linear))
        self.wait(1)

        group3 = VGroup(cube, network, calculator)
        self.play(FadeOut(group3))

        # Thank You Message
        thank_you = Text("Thank You for Watching!", font_size=48).move_to(self.main_region.get_center())
        self.play(Write(thank_you))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''To quickly recap, remember two key rules for matrix multiplication: first, the inner dimensions must match – columns of the first matrix must equal rows of the second. Second, each element in the product matrix is found by taking the dot product of a row from the first matrix and a column from the second. This powerful operation is fundamental in computer graphics for transforming objects in 3D space, in machine learning for neural networks, and in various scientific computations. Keep practicing, and you\'ll master this essential skill!'''
Scene4.audio_duration = 5.0
