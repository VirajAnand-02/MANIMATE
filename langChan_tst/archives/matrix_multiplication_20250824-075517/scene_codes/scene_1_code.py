import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Mastering Matrix Multiplication", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        matrix1 = Matrix([[1, 2], [3, 4]])
        matrix2 = Matrix([[5], [6]])
        matrix3 = Matrix([[7, 8, 9]])

        matrix1.move_to(self.main_region.get_center() + LEFT * 3)
        matrix2.move_to(self.main_region.get_center())
        matrix3.move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Create(matrix1), Create(matrix2), Create(matrix3))
        self.wait(0.5)

        cube = Cube().scale(0.5).move_to(self.main_region.get_center() + UP * 2 + LEFT * 3)
        network = NeuralNetwork([3, 4, 2]).scale(0.5).move_to(self.main_region.get_center() + UP * 2)
        table = Table([["A", "B"], ["C", "D"]]).scale(0.5).move_to(self.main_region.get_center() + UP * 2 + RIGHT * 3)

        self.play(FadeIn(cube), FadeIn(network), FadeIn(table))
        self.wait(0.5)

        q_mark = MathTex("?").scale(3).move_to(self.main_region.get_center() + DOWN * 2)
        matrix_a = Matrix([["a", "b"], ["c", "d"]]).move_to(self.main_region.get_center() + DOWN * 2 + LEFT * 2)
        matrix_b = Matrix([["e", "f"], ["g", "h"]]).move_to(self.main_region.get_center() + DOWN * 2 + RIGHT * 2)

        self.play(FadeOut(cube), FadeOut(network), FadeOut(table), FadeOut(matrix1), FadeOut(matrix2), FadeOut(matrix3))
        self.play(Create(matrix_a), Create(matrix_b), Write(q_mark))
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to our deep dive into matrix multiplication! Matrices are fundamental mathematical objects, essentially rectangular arrays of numbers, symbols, or expressions. They\'re not just abstract concepts; they power everything from computer graphics and image processing to physics simulations and machine learning. But unlike simple numbers, multiplying matrices has its own unique set of rules. Let\'s unravel this powerful operation step by step.'''
Scene1.audio_duration = 5.0
