import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title = self.create_textbox("Welcome to the Fascinating World of Matrices!", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(2)

        # Main animation
        matrix = Matrix([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
        ])
        matrix.move_to(self.main_region.get_center())
        self.play(Create(matrix))
        self.wait(1)

        cube = Cube(side_length=1).move_to(LEFT * 3 + UP * 1)
        data_points = DotCloud(np.random.rand(100, 3)).move_to(UP * 1)
        circuit = Rectangle(width=1, height=1).move_to(RIGHT * 3 + UP * 1)

        cube_label = Text("3D Graphics").next_to(cube, DOWN)
        data_label = Text("Data Science").next_to(data_points, DOWN)
        circuit_label = Text("Engineering").next_to(circuit, DOWN)

        self.play(FadeIn(cube), Write(cube_label))
        self.play(FadeIn(data_points), Write(data_label))
        self.play(FadeIn(circuit), Write(circuit_label))
        self.wait(2)

        title_card = Text("Matrix Multiplication: The Basics", font_size=48)
        title_card.move_to(self.main_region.get_center())

        self.play(
        Transform(matrix, title_card),
        FadeOut(cube, data_points, circuit, cube_label, data_label, circuit_label)
        )
        self.wait(3)

# Set narration and duration
Scene1.narration_text = '''Welcome to the fascinating world of matrices! A matrix is simply a rectangular array of numbers, symbols, or expressions, arranged in rows and columns. They\'re fundamental in computer graphics, data science, physics, and engineering. But unlike regular numbers, multiplying matrices has its own unique rules. Forget everything you know about standard multiplication for a moment, because matrix multiplication is a whole different beast. Let\'s dive in and demystify it!'''
Scene1.audio_duration = 5.0
