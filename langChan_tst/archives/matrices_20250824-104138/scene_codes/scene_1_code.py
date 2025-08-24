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
        title_text = self.create_textbox("Understanding Matrices", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # 2x2 Matrix
        matrix_2x2 = MathTex(
        r"\begin{bmatrix} a & b \\ c & d \end{bmatrix}"
        ).move_to(self.main_region.get_center())
        self.play(Write(matrix_2x2))
        self.wait(0.5)

        # Highlight rows and columns
        row1 = SurroundingRectangle(matrix_2x2[0][1:4], color=RED)
        row2 = SurroundingRectangle(matrix_2x2[0][7:10], color=RED)
        col1 = SurroundingRectangle(VGroup(matrix_2x2[0][1], matrix_2x2[0][7]), color=BLUE)
        col2 = SurroundingRectangle(VGroup(matrix_2x2[0][3], matrix_2x2[0][9]), color=BLUE)

        self.play(Create(row1), Create(row2))
        self.wait(0.3)
        self.play(Create(col1), Create(col2))
        self.wait(0.5)
        self.play(FadeOut(row1), FadeOut(row2), FadeOut(col1), FadeOut(col2))
        self.wait(0.3)

        # 3x3 Matrix
        matrix_3x3 = MathTex(
        r"\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}"
        ).move_to(self.main_region.get_center())
        self.play(Transform(matrix_2x2, matrix_3x3))
        self.wait(1)

        # Examples of real-world data as matrices
        pixel_matrix = Matrix(
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]]
        ).scale(0.5).move_to(self.main_region.get_center() + LEFT * 3)
        stock_matrix = Matrix(
        [["AAPL", 150], ["GOOG", 2700], ["MSFT", 250]]
        ).scale(0.5).move_to(self.main_region.get_center() + RIGHT * 3)

        self.play(Transform(matrix_2x2, pixel_matrix), Write(stock_matrix))
        self.wait(2)

        self.play(FadeOut(matrix_2x2), FadeOut(stock_matrix), FadeOut(title_text))
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to the fascinating world of matrices! Ever wondered how complex data is organized or how stunning 3D graphics are rendered? Often, the answer lies with matrices. Simply put, a matrix is a rectangular array of numbers, symbols, or expressions, arranged in rows and columns. Think of it like a super-organized spreadsheet for advanced mathematics! Each individual item within the matrix is called an \'element\'. Matrices are not just abstract concepts; they are incredibly powerful tools used across diverse fields, from computer science to engineering and economics. They help us efficiently organize and manipulate large sets of data. Let\'s dive in and see how these mathematical grids work!'''
Scene1.audio_duration = 5.0
