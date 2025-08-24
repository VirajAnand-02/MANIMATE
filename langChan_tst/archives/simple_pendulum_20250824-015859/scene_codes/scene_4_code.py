import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import SplitScreen

class Scene4(SplitScreen):
    def construct_scene(self):
        ```python
                title = self.create_textbox("Pendulum Period", width=self.left_region.width, height=self.left_region.height/3)
                title.move_to(self.left_region.get_center())

                text = self.create_textbox("Period depends on length and gravity. Mass has almost no effect!", width=self.left_region.width, height=self.left_region.height*2/3)
                text.move_to(self.left_region.get_center() + DOWN * self.left_region.height/3)

                self.play(Write(title))
                self.play(Write(text))
                self.wait(1)

                # Pendulums of different lengths
                l1 = 2
                l2 = 4
                g = 9.81
                t1 = 2 * PI * np.sqrt(l1 / g)
                t2 = 2 * PI * np.sqrt(l2 / g)

                pendulum1 = self.create_pendulum(length=l1, bob_radius=0.2, color=BLUE)
                pendulum2 = self.create_pendulum(length=l2, bob_radius=0.2, color=RED)

                pendulum1.move_to(self.right_region.get_center() + LEFT * 2)
                pendulum2.move_to(self.right_region.get_center() + RIGHT * 2)

                self.add(pendulum1, pendulum2)

                self.play(
                    self.swing(pendulum1, angle=PI/4, duration=t1),
                    self.swing(pendulum2, angle=PI/4, duration=t2),
                    run_time=max(t1, t2) * 2
                )

                self.wait(1)

                # Pendulums of same length, different mass
                l3 = 3
                pendulum3 = self.create_pendulum(length=l3, bob_radius=0.1, color=GREEN, mass=1)
                pendulum4 = self.create_pendulum(length=l3, bob_radius=0.3, color=YELLOW, mass=5)

                pendulum3.move_to(self.right_region.get_center() + LEFT * 2)
                pendulum4.move_to(self.right_region.get_center() + RIGHT * 2)

                self.play(
                    Transform(pendulum1, pendulum3),
                    Transform(pendulum2, pendulum4),
                    run_time=1
                )

                t3 = 2 * PI * np.sqrt(l3 / g)

                self.play(
                    self.swing(pendulum3, angle=PI/4, duration=t3),
                    self.swing(pendulum4, angle=PI/4, duration=t3),
                    run_time=t3 * 2
                )

                self.wait(2)

            def create_pendulum(self, length, bob_radius, color, mass=1):
                rod = Line(start=UP * length, end=DOWN * 0, color=color, stroke_width=3)
                bob = Circle(radius=bob_radius, color=color, fill_color=color, fill_opacity=1)
                bob.shift(DOWN * length)
                pendulum = VGroup(rod, bob)
                return pendulum

            def swing(self, pendulum, angle, duration):
                return pendulum.animate(rate_func=there_and_back, run_time=duration).rotate(angle)
        ```

# Set narration and duration
Scene4.narration_text = '''The time it takes for one complete swing, going back and forth, is called the period. Interestingly, the period of a simple pendulum depends primarily on its length and the acceleration due to gravity. The mass of the bob has almost no effect!'''
Scene4.audio_duration = 5.0
