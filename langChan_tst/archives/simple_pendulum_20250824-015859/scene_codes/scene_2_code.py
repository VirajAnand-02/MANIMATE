import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import SplitScreen

class Scene2(SplitScreen):
    def construct_scene(self):
        ```python
                # Ideal Pendulum (Left Side)
                point = Dot(self.left_region.get_center() + UP * 2)
                string = Line(point.get_center(), self.left_region.get_center() + DOWN * 2)
                bob = Dot(self.left_region.get_center() + DOWN * 2, radius=0.2)

                ideal_pendulum = VGroup(point, string, bob)

                # Real Pendulum (Right Side)
                real_bob = Sphere(radius=0.2).move_to(self.right_region.get_center() + DOWN * 2)
                real_string = Line(self.right_region.get_center() + UP * 2, real_bob.get_center())
                real_point = Dot(self.right_region.get_center() + UP * 2)

                real_pendulum = VGroup(real_point, real_string, real_bob)

                # Labels
                ideal_label = Text("Ideal Pendulum", font_size=24).next_to(ideal_pendulum, UP)
                real_label = Text("Real Pendulum", font_size=24).next_to(real_pendulum, UP)

                # Differences labels
                point_mass_label = Text("Point Mass", font_size=18, color=GREEN).next_to(bob, RIGHT)
                small_dense_label = Text("Small, Dense Object", font_size=18, color=RED).next_to(real_bob, RIGHT)
                massless_string_label = Text("Massless String", font_size=18, color=GREEN).next_to(string, LEFT)
                light_string_label = Text("Light String", font_size=18, color=RED).next_to(real_string, LEFT)

                self.play(Create(ideal_pendulum), Write(ideal_label))
                self.play(Create(real_pendulum), Write(real_label))
                self.wait(0.5)
                self.play(Write(point_mass_label), Write(small_dense_label), Write(massless_string_label), Write(light_string_label))
                self.wait(2)
        ```

# Set narration and duration
Scene2.narration_text = '''A simple pendulum consists of a point mass, or \'bob\', suspended from a fixed point by a massless, inextensible string. In reality, we use a small, dense object attached to a light string. The key is that the mass of the bob is much larger than the mass of the string.'''
Scene2.audio_duration = 5.0
