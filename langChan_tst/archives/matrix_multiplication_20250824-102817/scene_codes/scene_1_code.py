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
        title = self.create_textbox("Matrix Multiplication", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        matrix_grid = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix_grid.move_to(self.main_region.get_center())
        self.play(Create(matrix_grid))
        self.wait(1)

        matrix_a = Matrix([[1, 2], [3, 4]])
        matrix_b = Matrix([[5, 6], [7, 8]])
        matrix_a.move_to(self.main_region.get_center() + LEFT * 3)
        matrix_b.move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Transform(matrix_grid, VGroup(matrix_a, matrix_b).arrange(RIGHT, buff=2)))
        self.wait(1)

        question_mark = Tex("?").scale(3)
        question_mark.move_to(self.main_region.get_center())
        self.play(FadeIn(question_mark))
        self.wait(1)

        self.play(FadeOut(question_mark))

        cube = Cube().scale(0.7).move_to(self.main_region.get_center() + LEFT * 3)
        graph = Axes().scale(0.5).move_to(self.main_region.get_center())
        data_points = VGroup(*[Dot(point=np.random.rand(3)) for _ in range(20)]).scale(0.5).move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(FadeOut(matrix_a, matrix_b))
        self.play(FadeIn(cube, graph, data_points))
        self.wait(3)

# Set narration and duration
Scene1.narration_text = '''Welcome to the world of matrices! You might think multiplying matrices is as simple as multiplying corresponding numbers, but for matrices, it\'s a bit more profound. Matrix multiplication isn\'t just about combining individual elements; it\'s about combining entire rows and columns in a very specific way. This unique operation is fundamental to computer graphics, physics simulations, and data analysis. It allows us to perform complex transformations and calculations that simple element-wise multiplication just can\'t achieve. Let\'s dive in and unravel this powerful mathematical tool.'''
Scene1.audio_duration = 5.0
