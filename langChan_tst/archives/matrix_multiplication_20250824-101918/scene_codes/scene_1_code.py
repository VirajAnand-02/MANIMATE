import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication", self.title_region.width, self.title_region.height)
        title.move_to(self.title_region.get_center())

        matrix1 = Matrix([["a", "b"], ["c", "d"]])
        matrix2 = Matrix([["e", "f"], ["g", "h"]])
        matrix1.move_to(LEFT * 3)
        matrix2.move_to(RIGHT * 3)

        self.play(Write(title))
        self.play(Create(matrix1), Create(matrix2))
        self.wait(0.5)

        # Hint at applications
        cube = Cube(side_length=2).move_to(UP * 2)
        self.play(Rotate(cube, angle=PI / 2, axis=UP), run_time=0.5)
        self.wait(0.25)

        neural_network = VGroup(*[
        *[Dot(np.array([x, y, 0])) for x in np.linspace(-2, 2, 5)],
        *[Line(np.array([-2, y, 0]), np.array([2, 0, 0])) for y in np.linspace(-1, 1, 3)],
        *[Line(np.array([-2, 0, 0]), np.array([2, y, 0])) for y in np.linspace(-1, 1, 3)],
        *[Line(np.array([-2, y, 0]), np.array([2, y, 0])) for y in np.linspace(-1, 1, 3)],
        ]).scale(0.3).move_to(DOWN * 2)
        self.play(Create(neural_network), run_time=0.5)
        self.wait(0.25)

        data_table = Table([["1", "2"], ["3", "4"]]).scale(0.5).move_to(DOWN * 2)
        self.play(Transform(neural_network, data_table), run_time=0.5)
        self.wait(0.25)

        self.play(FadeOut(cube), FadeOut(neural_network))

        # Question mark
        question_mark = Tex("?").scale(5).move_to(ORIGIN)
        self.play(Transform(matrix1, question_mark.copy().move_to(LEFT * 3)), Transform(matrix2, question_mark.copy().move_to(RIGHT * 3)))

        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to the fascinating world of matrix multiplication! Matrices are rectangular arrays of numbers, and multiplying them isn\'t as simple as multiplying individual numbers. But it\'s a fundamental operation in computer graphics, scientific computing, machine learning, and many other fields. In this video, we\'ll demystify how to multiply matrices, step-by-step, and understand why it\'s so important.'''
Scene1.audio_duration = 5.0
