import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import SplitScreen
import numpy as np

class Scene2(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Matrix Operations", width=6, height=1)
        title.move_to(self.title_region.get_center())

        matrix_a = Matrix([["a", "b"], ["c", "d"]])
        matrix_b = Matrix([["e", "f"], ["g", "h"]])
        matrix_result = Matrix([["a+e", "b+f"], ["c+g", "d+h"]])
        scalar_matrix = Matrix([["1", "2"], ["3", "4"]])

        matrix_a.move_to(self.left_region.get_center() + LEFT * 2)
        matrix_b.move_to(self.right_region.get_center() + LEFT * 2)
        matrix_result.move_to(self.right_region.get_center() + RIGHT * 2)
        scalar_matrix.move_to(self.left_region.get_center() + RIGHT * 2)

        plus_sign = MathTex("+").move_to(self.left_region.get_center() + RIGHT * 2)
        equals_sign = MathTex("=").move_to(self.right_region.get_center() - LEFT * 2)

        self.play(Write(matrix_a), Write(matrix_b))
        self.play(Write(plus_sign), Write(equals_sign))
        self.wait(1)

        self.play(TransformMatchingShapes(matrix_a.copy(), matrix_result), TransformMatchingShapes(matrix_b.copy(), matrix_result))
        self.wait(2)

        scalar = MathTex("2").move_to(self.left_region.get_center() + LEFT * 4)
        scalar_mult_equals = MathTex("=").move_to(self.right_region.get_center() + LEFT * 4)
        scalar_result = Matrix([["2", "4"], ["6", "8"]])
        scalar_result.move_to(self.right_region.get_center() + RIGHT * 2)

        self.play(Write(scalar), Write(scalar_matrix))
        self.play(Write(scalar_mult_equals))

        for i in range(2):
        for j in range(2):
        self.play(Transform(scalar_matrix.entries[i][j].copy(), scalar_result.entries[i][j]))
        self.wait(2)

# Set narration and duration
Scene2.narration_text = '''Just like regular numbers, matrices can be added, subtracted, and multiplied by a scalar. For addition and subtraction, there\'s a crucial rule: matrices must have the exact same dimensions – meaning the same number of rows and columns. If they do, you simply add or subtract their corresponding elements, one by one. It\'s like combining two identical grids! Scalar multiplication is even simpler: you just multiply every single element within the matrix by that one single number. These fundamental operations are the essential building blocks for tackling more complex matrix manipulations.'''
Scene2.audio_duration = 5.0
