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

class Scene4(SplitScreen):
    def construct_scene(self):
        # --- Matrix Setup ---
        matrix_a = MathTex(r"A_{m \times n}", color=BLUE)
        matrix_b = MathTex(r"B_{p \times q}", color=GREEN)
        matrix_result = MathTex(r"C_{m \times q}", color=YELLOW)

        matrix_a.move_to(self.left_region.get_center() + 1.5*UP)
        matrix_b.move_to(self.right_region.get_center() + 1.5*UP)
        matrix_result.move_to(self.left_region.get_center() + 1.5*DOWN)

        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(0.5)

        # --- Highlight n and p ---
        n_in_a = matrix_a[0][3]  # Index of 'n' in A_{m x n}
        p_in_b = matrix_b[0][1]  # Index of 'p' in B_{p x q}

        n_circle = Circle(color=BLUE, stroke_width=3).surround(n_in_a)
        p_circle = Circle(color=GREEN, stroke_width=3).surround(p_in_b)

        self.play(Create(n_circle), Create(p_circle))
        self.wait(0.5)

        # --- n = p rule ---
        equals_np = MathTex("n = p", color=RED).move_to(ORIGIN)
        self.play(
        Transform(n_circle.copy().move_to(LEFT*2), equals_np[0][0]),
        Transform(p_circle.copy().move_to(RIGHT*2), equals_np[0][2]),
        Write(equals_np[0][1])
        )
        self.wait(1)

        self.play(FadeOut(equals_np, n_circle, p_circle))

        # --- Highlight m and q ---
        m_in_a = matrix_a[0][1]
        q_in_b = matrix_b[0][5]

        m_circle = Circle(color=BLUE, stroke_width=3).surround(m_in_a)
        q_circle = Circle(color=GREEN, stroke_width=3).surround(q_in_b)

        self.play(Create(m_circle), Create(q_circle))
        self.wait(0.5)

        # --- Resulting Matrix ---
        self.play(Write(matrix_result))
        self.wait(0.5)

        m_arrow = Arrow(m_circle.get_center(), matrix_result[0][1].get_center(), color=BLUE)
        q_arrow = Arrow(q_circle.get_center(), matrix_result[0][3].get_center(), color=GREEN)

        self.play(Create(m_arrow), Create(q_arrow))
        self.wait(0.5)
        self.play(FadeOut(m_arrow, q_arrow, m_circle, q_circle))

        # --- Application Icons ---
        cube = Cube(side_length=1, fill_color=RED, fill_opacity=0.5).move_to(self.left_region.get_center() + 3*DOWN)
        scatter = DotCloud(np.random.normal(size=(100, 3)), colors=[BLUE, GREEN]).move_to(self.right_region.get_center() + 3*DOWN)
        neural = NeuralNetwork([3, 5, 3], color=YELLOW).move_to(self.left_region.get_center() + 5*DOWN).scale(0.5)

        self.play(Create(cube))
        self.play(Create(scatter))
        self.play(Create(neural))
        self.wait(2)

        self.play(FadeOut(matrix_a, matrix_b, matrix_result, cube, scatter, neural))
        self.wait(1)

# Set narration and duration
Scene4.narration_text = '''Before you multiply, always check the dimensions! For matrices A (m x n) and B (p x q) to be multiplied, the number of columns in A must equal the number of rows in B. That means \'n\' must equal \'p\'. The resulting matrix will have dimensions \'m x q\'. If the inner dimensions don\'t match, multiplication is impossible. Matrix multiplication is crucial in many fields: from 3D computer graphics for rotating and scaling objects, to solving systems of linear equations, and even powering machine learning algorithms. It\'s a fundamental concept for anyone delving deeper into mathematics or computer science.'''
Scene4.audio_duration = 5.0
