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
        title_text = self.create_textbox("Matrix Multiplication: The Essential Guide", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        matrix_2x2 = MathTex(r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}")
        matrix_3x3 = MathTex(r"\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}")

        matrix_2x2.move_to(self.main_region.get_center())
        self.play(Create(matrix_2x2))
        self.wait(1)

        graphics_text = Text("Computer Graphics").scale(0.5).next_to(matrix_2x2, UP + LEFT)
        data_text = Text("Data Science").scale(0.5).next_to(matrix_2x2, DOWN)
        physics_text = Text("Physics").scale(0.5).next_to(matrix_2x2, UP + RIGHT)

        self.play(Write(graphics_text), Write(data_text), Write(physics_text))
        self.wait(1)

        self.play(Transform(matrix_2x2, matrix_3x3), FadeOut(graphics_text), FadeOut(data_text), FadeOut(physics_text))
        matrix_3x3.move_to(self.main_region.get_center())
        self.wait(2)

# Set narration and duration
Scene1.narration_text = '''Welcome to our deep dive into matrix multiplication! You might be familiar with matrices as rectangular arrays of numbers. But when it comes to multiplying them, it\'s not as simple as multiplying corresponding elements. Matrix multiplication is a fundamental operation in mathematics, crucial for everything from computer graphics and data science to physics and engineering. It allows us to perform complex transformations and solve systems of equations efficiently. So, let\'s unlock the secrets of this powerful operation!'''
Scene1.audio_duration = 5.0
