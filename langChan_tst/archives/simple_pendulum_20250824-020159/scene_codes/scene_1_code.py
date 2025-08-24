import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("Understanding the Simple Pendulum", self.title_region.width, self.title_region.height)
                title_text.move_to(self.title_region.get_center())

                self.play(Write(title_text))
                self.wait(2)

                # Montage (Placeholder - replace with actual images/videos)
                clock = Square(side_length=2, color=BLUE).shift(LEFT * 3)
                swing = Circle(radius=1, color=GREEN).shift(UP * 1.5)
                art = Triangle(color=RED).shift(RIGHT * 3)

                clock_text = Text("Grandfather Clock", font_size=20).next_to(clock, DOWN)
                swing_text = Text("Playground Swing", font_size=20).next_to(swing, DOWN)
                art_text = Text("Pendulum Art", font_size=20).next_to(art, DOWN)

                group = VGroup(clock, swing, art, clock_text, swing_text, art_text).move_to(self.main_region.get_center())

                self.play(Create(clock), Write(clock_text))
                self.play(Create(swing), Write(swing_text))
                self.play(Create(art), Write(art_text))
                self.wait(3)
                self.play(FadeOut(group))
                self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Hey everyone, welcome! Today we\'re diving into the fascinating world of physics to explore the simple pendulum. We\'ll learn what it is, how it works, and what factors influence its motion. Get ready for some swinging good science!'''
Scene1.audio_duration = 5.0
