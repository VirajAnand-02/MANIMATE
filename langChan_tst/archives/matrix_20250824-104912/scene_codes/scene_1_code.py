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

        # Create a 3x2 matrix
        matrix_3x2 = Matrix([
        [1, 2, 3],
        [4, 5, 6]
        ])
        matrix_3x2.move_to(self.main_region.get_center())

        # Create the grid and populate it
        self.play(Create(matrix_3x2.get_brackets()))
        self.play(Write(matrix_3x2.get_entries()))
        self.wait(1)

        # Highlight rows
        for i in range(2):
        rect = Rectangle(width=matrix_3x2.get_entries().get_width(), height=matrix_3x2.get_entries()[i*3].get_height(), color=YELLOW, fill_opacity=0.3)
        rect.move_to(matrix_3x2.get_entries()[i*3].get_center()).shift(RIGHT * matrix_3x2.get_entries().get_width()/2)
        self.play(Create(rect))
        self.wait(0.5)
        self.play(FadeOut(rect))

        # Highlight columns
        for j in range(3):
        rect = Rectangle(width=matrix_3x2.get_entries()[0].get_width(), height=matrix_3x2.get_entries().get_height(), color=GREEN, fill_opacity=0.3)
        rect.move_to(matrix_3x2.get_entries()[j].get_center()).shift(DOWN * matrix_3x2.get_entries().get_height()/2)
        self.play(Create(rect))
        self.wait(0.5)
        self.play(FadeOut(rect))

        self.wait(1)

        # Create a 2x3 matrix example with m and n labels
        matrix_2x3 = Matrix([
        [7, 8],
        [9, 10],
        [11, 12]
        ])
        matrix_2x3.move_to(self.main_region.get_center())
        m_label = MathTex("m").next_to(matrix_2x3, LEFT)
        n_label = MathTex("n").next_to(matrix_2x3, DOWN)

        self.play(Transform(matrix_3x2, matrix_2x3), Write(m_label), Write(n_label))
        self.wait(1)

        # Transition to a real-world data table
        data_table = Matrix([
        ["Product A", 100, 150, 120],
        ["Product B", 80, 90, 110],
        ["Product C", 110, 120, 130]
        ])
        data_table.move_to(self.main_region.get_center())

        self.play(Transform(VGroup(matrix_2x3, m_label, n_label), data_table))
        self.wait(2)

# Set narration and duration
Scene1.narration_text = '''Ever wondered how complex data can be organized and manipulated efficiently? Meet the Matrix! In mathematics, a matrix is simply a rectangular array of numbers, symbols, or expressions arranged in rows and columns. Think of it like a structured table or a spreadsheet. Each item inside is called an element. We define a matrix by its order – the number of rows \'m\' by the number of columns \'n\', written as m x n. For example, a 2x3 matrix has two rows and three columns. Matrices are fundamental tools, allowing us to process large amounts of information, represent transformations, and solve complex systems in a structured way. Let\'s dive deeper into their world!'''
Scene1.audio_duration = 5.0
