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
        title_text = self.create_textbox("Mastering Matrix Multiplication", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        matrix_text = Text("Rectangular arrays of numbers")
        matrix_text.move_to(self.main_region.get_center())

        matrix = Matrix([[1, 2], [3, 4]])
        matrix.next_to(matrix_text, DOWN)

        self.play(Write(matrix_text), Create(matrix))
        self.wait(1)

        # Examples of applications
        cube = Cube(fill_opacity=0.5, color=BLUE).scale(0.5).move_to(LEFT * 3)
        self.play(Rotate(cube, angle=PI / 4, axis=OUT, run_time=1))
        self.play(Rotate(cube, angle=PI / 4, axis=UP, run_time=1))

        axes = Axes(x_range=[0, 5, 1], y_range=[0, 5, 1]).scale(0.4).move_to(UP * 1.5)
        dots = VGroup(*[Dot(axes.c2p(x, np.random.rand() * 4), radius=0.03) for x in np.linspace(0, 4, 10)])
        self.play(Create(axes), Create(dots))

        equations = MathTex(r"x + y = 5", r"2x - y = 1").scale(0.7).move_to(RIGHT * 3)
        self.play(Write(equations))
        self.wait(1)

        # Matrix compatibility rule
        matrix_a = MathTex(r"A_{m \times n}").move_to(LEFT * 2 + DOWN * 2)
        matrix_b = MathTex(r"B_{n \times p}").move_to(RIGHT * 2 + DOWN * 2)

        n_a = matrix_a.get_part_by_tex("n")
        n_b = matrix_b.get_part_by_tex("n")

        self.play(Write(matrix_a), Write(matrix_b))
        self.play(n_a.animate.set_color(YELLOW), n_b.animate.set_color(YELLOW))
        self.wait(2)

# Set narration and duration
Scene1.narration_text = '''Welcome to the fascinating world of matrix multiplication! You\'ve probably encountered matrices as rectangular arrays of numbers. But what happens when we want to multiply them? Unlike simple number multiplication, matrix multiplication has a unique set of rules and powerful applications. From transforming objects in computer graphics to solving complex systems in engineering, understanding this operation is crucial. Before we dive into the \'how,\' let\'s quickly remember that for two matrices, A and B, to be multiplied, the number of columns in A must equal the number of rows in B. This is a fundamental rule we\'ll see in action. Let\'s get started!'''
Scene1.audio_duration = 5.0
