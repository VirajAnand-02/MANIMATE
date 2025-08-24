import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        # Title
                title_text = self.create_textbox("The Simple Pendulum", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
                title_text.move_to(self.title_region.get_center())
                self.play(Write(title_text))
                self.wait(1)

                # Pendulum animation
                L = 3  # Length of pendulum
                g = 9.81  # Acceleration due to gravity
                T = 2 * PI * np.sqrt(L / g)  # Period of pendulum

                bob_radius = 0.2
                string = Line(start=UP * 3, end=DOWN * L, stroke_width=3)
                bob = Circle(radius=bob_radius, color=RED, fill_opacity=1)
                pendulum = VGroup(string, bob).move_to(self.main_region.get_center())

                def update_pendulum(mob, alpha):
                    angle = np.sin(TAU * alpha / T)
                    mob[1].move_to(mob[0].get_end() + bob_radius * np.array([np.sin(angle), -np.cos(angle), 0]))
                    mob[0].rotate(angle - mob[0].get_angle(), about_point=mob[0].get_start())

                self.add(pendulum)

                # Equation
                equation = MathTex(r"T = 2\pi\sqrt{\frac{L}{g}}").next_to(pendulum, UP)
                self.play(Write(equation))
                self.wait(2)

                self.play(
                    UpdateFromAlphaFunc(pendulum, update_pendulum),
                    run_time=5,
                    rate_func=linear
                )

                self.wait(1)
                self.play(FadeOut(pendulum, equation, title_text))

                # Thank you screen
                thank_you_text = self.create_textbox("Thanks for watching!\nCredits & Resources in description.", width=self.main_region.width * 0.8, height=self.main_region.height * 0.8)
                thank_you_text.move_to(self.main_region.get_center())
                self.play(Write(thank_you_text))
                self.wait(3)

# Set narration and duration
Scene5.narration_text = '''So, the next time you see a pendulum swinging, remember the simple yet elegant physics at play. The length, gravity, and the bob\'s journey create a beautiful dance between potential and kinetic energy. Thanks for watching!'''
Scene5.audio_duration = 5.0
