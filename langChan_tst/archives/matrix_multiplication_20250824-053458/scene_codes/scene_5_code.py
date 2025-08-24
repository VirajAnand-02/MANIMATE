import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Matrix Multiplication Recap", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Summary Slide
        rules = [
        "1. Check Dimensions (Inner Match)",
        "2. Result Dimensions (Outer Numbers)",
        "3. Dot Product (Row x Column)"
        ]
        rule_texts = [Text(rule, font_size=24) for rule in rules]
        rules_group = VGroup(*rule_texts).arrange(DOWN, aligned_edge=LEFT)
        rules_group.move_to(self.main_region.get_center())
        self.play(Write(rules_group))
        self.wait(2)

        # Applications Montage
        self.play(FadeOut(rules_group))

        # Spinning 3D Object (Placeholder)
        cube = Cube(side_length=2).move_to(self.main_region.get_center() + LEFT * 3)
        self.play(Rotate(cube, angle=PI/2, axis=UP, run_time=2))

        # Neural Network Diagram (Placeholder)
        dots = VGroup(*[Dot(point=np.random.rand(3)*2-1) for _ in range(10)]).move_to(self.main_region.get_center() + RIGHT * 3)
        self.play(Create(dots))

        self.wait(2)

        # Thank You Message
        thank_you_text = Text("Thank You!", font_size=48)
        thank_you_text.move_to(self.main_region.get_center())
        self.play(FadeOut(cube, dots))
        self.play(Write(thank_you_text))
        self.wait(1)

# Set narration and duration
Scene5.narration_text = '''So, to recap: check dimensions first – inner numbers must match. The result\'s dimensions are the outer numbers. Then, for each element in your new matrix, perform a dot product: a row from the first matrix multiplied by a column from the second. Matrix multiplication might seem complex at first, but with practice, it becomes a powerful tool. Keep practicing, and you\'ll be a matrix master in no time! Thanks for watching!'''
Scene5.audio_duration = 5.0
