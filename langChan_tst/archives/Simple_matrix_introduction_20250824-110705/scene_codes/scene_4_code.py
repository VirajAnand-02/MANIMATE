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
        title_text = self.create_textbox("Matrix Operations", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Main Animation
        matrix1 = MathTex(r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}")
        matrix2 = MathTex(r"\begin{bmatrix} e & f \\ g & h \end{bmatrix}")
        plus_sign = MathTex("+")
        equals_sign = MathTex("=")
        empty_matrix = MathTex(r"\begin{bmatrix} ? & ? \\ ? & ? \end{bmatrix}")

        group_add = VGroup(matrix1, plus_sign, matrix2, equals_sign, empty_matrix).arrange(buff=0.5)
        group_add.move_to(self.main_region.get_center())

        self.play(Write(matrix1), Write(plus_sign), Write(matrix2))
        self.wait(0.5)
        self.play(Write(equals_sign), Write(empty_matrix))
        self.wait(1)
        self.play(FadeOut(group_add))

        minus_sign = MathTex("-")
        group_sub = VGroup(matrix1.copy(), minus_sign, matrix2.copy(), equals_sign.copy(), empty_matrix.copy()).arrange(buff=0.5)
        group_sub.move_to(self.main_region.get_center())
        self.play(Write(matrix1), Write(minus_sign), Write(matrix2))
        self.wait(0.5)
        self.play(Write(equals_sign), Write(empty_matrix))
        self.wait(1)
        self.play(FadeOut(group_sub))

        times_sign = MathTex(r"\times")
        group_mul = VGroup(matrix1.copy(), times_sign, matrix2.copy(), equals_sign.copy(), empty_matrix.copy()).arrange(buff=0.5)
        group_mul.move_to(self.main_region.get_center())
        self.play(Write(matrix1), Write(times_sign), Write(matrix2))
        self.wait(0.5)
        self.play(Write(equals_sign), Write(empty_matrix))
        self.wait(1)
        self.play(FadeOut(group_mul))

        future_topic = Text("Future Topic: Matrix Operations", font_size=36)
        future_topic.move_to(self.main_region.get_center())
        arrow = Arrow(future_topic.get_left(), future_topic.get_right(), buff=0.2)
        self.play(Write(future_topic), Create(arrow))
        self.wait(1.5)
        self.play(FadeOut(future_topic), FadeOut(arrow))

        thank_you = Text("Thank You for Watching!", font_size=48)
        thank_you.move_to(self.main_region.get_center())
        self.play(Write(thank_you))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''Just like regular numbers, matrices can be added, subtracted, and even multiplied, though matrix multiplication has its own unique rules! These operations allow us to manipulate entire datasets or geometric transformations in a structured way. For instance, adding two matrices might combine two different sets of data, while multiplying them could represent a sequence of transformations. We\'ll explore these operations in more detail in future videos, but for now, remember that matrices are not just static arrays; they are dynamic tools that can be operated on to achieve powerful results. You\'ve just taken your first step into the world of matrices!'''
Scene4.audio_duration = 5.0
