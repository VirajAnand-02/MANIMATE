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

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Matrix Multiplication: Order Matters!", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Main animation
        matrix_a = MathTex(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}").move_to(LEFT * 3)
        matrix_b = MathTex(r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}").move_to(LEFT)
        matrix_c = MathTex(r"\begin{bmatrix} 19 & 22 \\ 43 & 50 \end{bmatrix}").move_to(RIGHT * 1.5)
        equals_ab = MathTex("=").move_to(RIGHT * 0.5)
        times_ab = MathTex(r"\times").move_to(LEFT * 2)

        group_ab = VGroup(matrix_a, times_ab, matrix_b, equals_ab, matrix_c).move_to(self.main_region.get_center() + UP * 1.5)

        self.play(Write(matrix_a), Write(matrix_b), Write(times_ab))
        self.play(Write(equals_ab), Write(matrix_c))
        self.wait(1)

        matrix_b2 = MathTex(r"\begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix}").move_to(LEFT * 3)
        matrix_a2 = MathTex(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}").move_to(LEFT)
        matrix_d = MathTex(r"\begin{bmatrix} 23 & 34 \\ 31 & 46 \end{bmatrix}").move_to(RIGHT * 1.5)
        equals_ba = MathTex("=").move_to(RIGHT * 0.5)
        times_ba = MathTex(r"\times").move_to(LEFT * 2)

        group_ba = VGroup(matrix_b2, times_ba, matrix_a2, equals_ba, matrix_d).move_to(self.main_region.get_center() + DOWN * 1.5)

        self.play(Transform(matrix_a, matrix_b2), Transform(matrix_b, matrix_a2), Transform(equals_ab, equals_ba))
        self.play(Write(matrix_d), Transform(times_ab, times_ba))
        self.wait(1)

        not_equal = MathTex(r"\neq").move_to(self.main_region.get_center())
        self.play(Write(not_equal))
        self.wait(1)
        self.play(FadeOut(not_equal))

        # Application icons
        cube = Cube(side_length=1).move_to(LEFT * 4 + DOWN * 1.5).rotate(PI/4, axis=RIGHT)
        graph = Axes().plot(lambda x: np.sin(x)).scale(0.5).move_to(DOWN * 1.5)
        neuron = Circle(radius=0.5).move_to(RIGHT * 4 + DOWN * 1.5)

        self.play(Create(cube))
        self.play(Create(graph))
        self.play(Create(neuron))
        self.wait(1)

        self.play(FadeOut(cube), FadeOut(graph), FadeOut(neuron), FadeOut(group_ab), FadeOut(group_ba))

        # End screen
        end_title = self.create_textbox("Matrix Multiplication", width=self.main_region.width * 0.8, height=self.main_region.height * 0.3)
        end_title.move_to(self.main_region.get_center() + UP * 0.5)
        thank_you = Text("Thank You!").move_to(self.main_region.get_center() + DOWN * 0.5)

        self.play(Write(end_title))
        self.play(Write(thank_you))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''One crucial thing to remember about matrix multiplication is that it\'s generally not commutative. That means A times B is usually not the same as B times A. The order matters! This is a big difference from multiplying regular numbers. So, always pay attention to the order. To recap, check compatibility, then systematically multiply rows by columns, summing the products. Mastering this operation opens doors to understanding complex transformations in graphics, solving systems of equations, and powering modern AI algorithms. Keep practicing, and you\'ll master it in no time!'''
Scene4.audio_duration = 5.0
