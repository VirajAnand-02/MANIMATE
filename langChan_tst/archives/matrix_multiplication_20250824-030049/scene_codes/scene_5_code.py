import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene5(SplitScreen):
    def construct_scene(self):
        # Left side: A * B calculated (using previous example).
        matrix_a = Matrix([[1, 2], [3, 4]])
        matrix_b = Matrix([[5, 6], [7, 8]])
        result_ab = Matrix([[19, 22], [43, 50]])

        # Right side: B * A calculated (showing a different result).
        matrix_ba = Matrix([[5, 6], [7, 8]])  # Reusing matrix_b for clarity
        matrix_a2 = Matrix([[1, 2], [3, 4]])  # Reusing matrix_a for clarity
        result_ba = Matrix([[23, 34], [31, 46]])

        # Text 'A * B ≠ B * A' is displayed prominently.
        neq_text = MathTex("A \\cdot B \\neq B \\cdot A")

        # Montage of different matrix sizes being multiplied, encouraging practice.
        matrix_c = Matrix([[1, 2, 3], [4, 5, 6]])
        matrix_d = Matrix([[7, 8], [9, 10], [11, 12]])
        matrix_e = Matrix([[1, 2], [3, 4], [5, 6]])
        matrix_f = Matrix([[7, 8, 9], [10, 11, 12]])

        # Positioning
        matrix_a.move_to(self.left_region.get_center() + LEFT * 2)
        matrix_b.move_to(self.left_region.get_center())
        result_ab.move_to(self.left_region.get_center() + RIGHT * 2)

        matrix_ba.move_to(self.right_region.get_center() + LEFT * 2)
        matrix_a2.move_to(self.right_region.get_center())
        result_ba.move_to(self.right_region.get_center() + RIGHT * 2)

        neq_text.move_to(UP * 2)

        matrix_c.scale(0.7).move_to(DOWN * 1 + LEFT * 3)
        matrix_d.scale(0.7).move_to(DOWN * 1 + LEFT * 1)
        matrix_e.scale(0.7).move_to(DOWN * 1 + RIGHT * 1)
        matrix_f.scale(0.7).move_to(DOWN * 1 + RIGHT * 3)

        # Animations
        self.play(Write(matrix_a), Write(matrix_b), Write(result_ab), Write(matrix_ba), Write(matrix_a2), Write(result_ba))
        self.wait(1)
        self.play(Write(neq_text))
        self.wait(1)
        self.play(Write(matrix_c), Write(matrix_d), Write(matrix_e), Write(matrix_f))
        self.wait(2)

# Set narration and duration
Scene5.narration_text = '''Remember, matrix multiplication is not commutative, meaning A * B is generally not equal to B * A. Also, practice makes perfect! Work through examples and explore different matrix sizes to solidify your understanding. Good luck!'''
Scene5.audio_duration = 5.0
