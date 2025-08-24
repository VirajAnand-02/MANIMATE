import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Matrix Multiplication Recap", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Dimension Rule
        dim_rule = MathTex(r"(m \times n) \cdot (n \times p) = (m \times p)")
        dim_rule.move_to(self.main_region.get_center() + UP * 2)

        # Row-by-Column Visual
        matrix1 = Matrix([["a", "b"], ["c", "d"]])
        matrix2 = Matrix([["e", "f"], ["g", "h"]])
        result_matrix = Matrix([["ae+bg", "af+bh"], ["ce+dg", "cf+dh"]])

        matrix1.move_to(self.main_region.get_center() + LEFT * 3 + DOWN * 1)
        matrix2.move_to(self.main_region.get_center() + RIGHT * 3 + DOWN * 1)
        result_matrix.move_to(self.main_region.get_center() + DOWN * 1)

        self.play(Write(dim_rule))
        self.play(Write(matrix1), Write(matrix2))
        self.wait(1)
        self.play(Write(result_matrix))
        self.wait(2)

        # 3D Cube Transformation
        cube = Cube(fill_opacity=0.5, fill_color=BLUE, stroke_color=WHITE)
        cube.move_to(self.main_region.get_center() + LEFT * 4 + UP * 0.5)
        cube.scale(0.5)
        self.play(
        Rotate(cube, angle=PI / 2, axis=UP, run_time=1),
        FadeOut(dim_rule, matrix1, matrix2, result_matrix)
        )

        # Neural Network Diagram
        nn_diagram = VGroup(*[Dot(point=[i, j, 0]) for i in range(-1, 2) for j in range(-1, 2)])
        for i in range(len(nn_diagram) - 1):
        nn_diagram.add(Line(nn_diagram[i].get_center(), nn_diagram[i+1].get_center()))
        nn_diagram.move_to(self.main_region.get_center() + UP * 0.5)
        nn_diagram.scale(0.5)
        self.play(Write(nn_diagram), FadeOut(cube))

        # System Transformations Graph
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1])
        graph = axes.plot(lambda x: x**2, color=GREEN)
        axes.move_to(self.main_region.get_center() + RIGHT * 4 + UP * 0.5)
        axes.scale(0.5)
        self.play(Create(axes), Create(graph), FadeOut(nn_diagram))
        self.wait(1)

        # Encouraging Message
        message = Text("Keep Practicing!", color=YELLOW)
        message.move_to(self.main_region.get_center() + DOWN * 2)

        # "Matrix Multiplication Mastered!" Graphic
        mastered_text = Text("Matrix Multiplication Mastered!", color=GREEN)
        mastered_text.move_to(self.main_region.get_center() + DOWN * 3)

        self.play(Write(message), Write(mastered_text), FadeOut(axes, graph))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''To recap: Matrix multiplication requires the inner dimensions to match. Each element in the result matrix is found by taking the dot product of a row from the first matrix and a column from the second. While it might seem complex at first, this operation is incredibly powerful. It\'s used in 3D computer graphics to transform objects – rotating, scaling, and translating them. In machine learning, it\'s fundamental for neural networks to process data. And in physics, it helps solve systems of equations. Keep practicing, and you\'ll master this essential mathematical tool!'''
Scene4.audio_duration = 5.0
