import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("Matrix Multiplication!", self.title_region.width, self.title_region.height)
        title.move_to(self.title_region.get_center())

        matrix_a = Matrix([["a", "b"], ["c", "d"]])
        matrix_b = Matrix([["e", "f"], ["g", "h"]])
        matrix_c = Matrix([["ae+bg", "af+bh"], ["ce+dg", "cf+dh"]])

        matrix_a.move_to(LEFT * 3)
        matrix_b.move_to(RIGHT * 3)
        matrix_c.move_to(DOWN * 2)

        equals1 = MathTex("=").move_to((matrix_a.get_right() + matrix_b.get_left()) / 2)
        times = MathTex("\\times").move_to(UP * 2)
        equals2 = MathTex("=").move_to((times.get_right() + matrix_c.get_left()) / 2 + UP * 2)

        group = VGroup(matrix_a, times, matrix_b, equals2, matrix_c)
        group.move_to(self.main_region.get_center())

        practice_text = Text("Practice Makes Perfect!", color=GREEN).scale(1.2)
        practice_text.move_to(UP * 2)

        thumb_up = ImageMobject("thumb_up.png").scale(0.5).next_to(practice_text, LEFT)
        star1 = ImageMobject("star.png").scale(0.3).next_to(practice_text, RIGHT)
        star2 = ImageMobject("star.png").scale(0.3).next_to(star1, RIGHT)

        self.play(Write(title))
        self.wait(1)
        self.play(Create(matrix_a), Create(matrix_b), Write(times), Write(equals2))
        self.wait(2)
        self.play(Write(matrix_c))
        self.wait(2)
        self.play(Write(practice_text))
        self.play(FadeIn(thumb_up, shift=LEFT), FadeIn(star1, shift=RIGHT), FadeIn(star2, shift=RIGHT))
        self.play(thumb_up.animate.shift(UP * 0.5).rotate(PI/6), star1.animate.shift(UP * 0.5), star2.animate.shift(UP * 0.5))
        self.wait(3)

# Set narration and duration
Scene5.narration_text = '''And that\'s matrix multiplication! Remember to check that your matrices are compatible, and carefully multiply corresponding rows and columns. Keep practicing, and you\'ll be a pro in no time!'''
Scene5.audio_duration = 5.0
