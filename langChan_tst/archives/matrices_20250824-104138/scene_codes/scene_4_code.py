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
        title = self.create_textbox("Matrices: Real-World Applications", width=10, height=1)
        title.move_to(UP * 3.5)
        self.add(title)

        # Left Region: 3D Object Transformation
        cube = Cube(side_length=2, fill_opacity=0.5, fill_color=BLUE, stroke_color=WHITE)
        cube.move_to(self.left_region.get_center())

        matrix_bg = Matrix([["a", "b"], ["c", "d"]], h_buff=1.5, v_buff=1.0)
        matrix_bg.scale(0.5)
        matrix_bg.set_opacity(0.2)
        matrix_bg.move_to(self.left_region.get_center() + DOWN * 1.5)

        self.add(matrix_bg)
        self.add(cube)

        self.play(
        Rotate(cube, angle=PI / 4, axis=OUT, run_time=2),
        Scale(cube, scale_factor=1.2, run_time=2)
        )
        self.play(
        Rotate(cube, angle=-PI / 4, axis=OUT, run_time=2),
        Scale(cube, scale_factor=0.8, run_time=2)
        )

        # Right Region: Linear Equations to Matrix Equation
        equations = MathTex(
        r"2x + 3y = 7 \\",
        r"x - y = 1"
        )
        equations.move_to(self.right_region.get_center() + UP * 1)
        matrix_equation = MathTex(
        r"\begin{bmatrix} 2 & 3 \\ 1 & -1 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 7 \\ 1 \end{bmatrix}"
        )
        matrix_equation.move_to(self.right_region.get_center() + DOWN * 1)

        self.play(Write(equations))
        self.wait(1)
        self.play(Transform(equations, matrix_equation))
        self.wait(1)

        # Image Processing
        image_grid = VGroup(*[Square(side_length=0.1, fill_color=BLACK, fill_opacity=1, stroke_width=0) for _ in range(100)])
        image_grid.arrange_in_grid(10, 10, buff=0)
        image_grid.scale(0.8)
        image_grid.move_to(self.right_region.get_center() + DOWN * 1)
        image_grid.set_opacity(0)

        self.play(FadeOut(equations))
        self.play(FadeIn(image_grid))

        for i in range(10):
        self.play(image_grid[i].animate.set_fill(color=WHITE), run_time=0.1)
        self.wait(1)
        self.play(FadeOut(image_grid))

        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''So, why do we delve into these rectangular arrays? Because matrices are indispensable across countless real-world applications! In computer graphics, they\'re the backbone for transforming objects – scaling, rotating, and translating them in 2D and 3D space. Every time you play a video game, matrices are working tirelessly behind the scenes to render the world around you. They\'re also vital for solving large systems of linear equations, which appear in fields from engineering and physics to economics and statistics. Data scientists use matrices to represent and analyze vast datasets, powering everything from image processing and facial recognition to machine learning algorithms. Understanding matrices truly unlocks a new dimension of problem-solving capabilities!'''
Scene4.audio_duration = 5.0
