import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # Title
                title_text = self.create_textbox("Understanding the Simple Pendulum", self.title_region.width, self.title_region.height)
                title_text.move_to(self.title_region.get_center())

                # Pendulum animation
                pivot = Dot(self.main_region.get_center() + UP * 2)
                length = 2
                bob_position = self.main_region.get_center() + DOWN * length
                bob = Dot(bob_position, radius=0.2, color=BLUE)
                string = Line(pivot.get_center(), bob.get_center(), color=WHITE)

                def update_bob(mob, angle=0.5 * PI * np.sin(self.time)):
                    new_x = pivot.get_x() + length * np.sin(angle)
                    new_y = pivot.get_y() - length * np.cos(angle)
                    mob.move_to([new_x, new_y, 0])
                    string.become(Line(pivot.get_center(), mob.get_center(), color=WHITE))

                bob.add_updater(update_bob)
                self.add(pivot, string, bob)

                self.add(title_text)
                self.wait(5)

# Set narration and duration
Scene1.narration_text = '''Welcome! Today, we\'ll explore the fascinating world of the simple pendulum. We\'ll learn what it is, how it works, and the factors that influence its motion. Get ready to swing into action!'''
Scene1.audio_duration = 5.0
