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
        title_text = self.create_textbox("Introduction to Matrices", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        matrix.move_to(self.main_region.get_center())

        self.play(Create(matrix))
        self.wait(1)

        # Example of data points (brief visual)
        dots = VGroup(*[Dot(point=np.random.rand(3) * 2 - 1) for _ in range(20)])
        dots.move_to(self.main_region.get_center() + RIGHT * 3)
        self.play(FadeIn(dots))
        self.wait(0.5)
        self.play(FadeOut(dots))

        # Example of 2D shape transformation (brief visual)
        square = Square(side_length=1).move_to(self.main_region.get_center() + LEFT * 3)
        self.play(square.animate.rotate(PI/4))
        self.wait(0.5)
        self.play(FadeOut(square))

        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to a quick introduction to matrices! Ever wondered how computers handle complex data or graphics? Often, it\'s with the help of matrices. Simply put, a matrix is a rectangular array of numbers, symbols, or expressions, arranged in rows and columns. Think of it like a spreadsheet or a table, but with specific mathematical rules. They\'re fundamental tools in mathematics, science, engineering, and computer graphics, used to organize and manipulate data efficiently. Ready to dive in?'''
Scene1.audio_duration = 5.0
