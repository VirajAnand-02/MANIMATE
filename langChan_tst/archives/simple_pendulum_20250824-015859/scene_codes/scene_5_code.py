```python
from manim import *

class GeneratedScene_5(Scene):
    def construct(self):
        # Formula
        formula = MathTex(r"T = 2\pi\sqrt{\frac{L}{g}}")
        self.play(Write(formula))
        self.wait(2)

        # Small angle pendulum
        small_angle_pendulum = VGroup()
        string_length = 2
        bob_radius = 0.2
        pivot = np.array([0, 2, 0])
        bob_position = pivot + np.array([0, -string_length, 0])
        string = Line(pivot, bob_position)
        bob = Circle(radius=bob_radius, color=RED, fill_opacity=1).move_to(bob_position)
        small_angle_pendulum.add(string, bob)
        small_angle = 0.2  # radians

        def update_small_angle_pendulum(mob, alpha):
            angle = small_angle * np.sin(alpha * TAU)
            new_bob_position = pivot + np.array([string_length * np.sin(angle), -string_length * np.cos(angle), 0])
            mob[0].become(Line(pivot, new_bob_position))
            mob[1].move_to(new_bob_position)

        small_angle_pendulum.move_to(LEFT * 3)
        self.play(Create(small_angle_pendulum))
        self.play(UpdateFromAlphaFunc(small_angle_pendulum, update_small_angle_pendulum), run_time=3, rate_func=linear)
        self.wait(1)

        # Large angle pendulum
        large_angle_pendulum = VGroup()
        bob_position = pivot + np.array([0, -string_length, 0])
        string = Line(pivot, bob_position)
        bob = Circle(radius=bob_radius, color=RED, fill_opacity=1).move_to(bob_position)
        large_angle_pendulum.add(string, bob)
        large_angle = 1.2  # radians

        def update_large_angle_pendulum(mob, alpha):
            angle = large_angle * np.sin(alpha * TAU)
            new_bob_position = pivot + np.array([string_length * np.sin(angle), -string_length * np.cos(angle), 0])
            mob[0].become(Line(pivot, new_bob_position))
            mob[1].move_to(new_bob_position)

        large_angle_pendulum.move_to(RIGHT * 3)
        self.play(Create(large_angle_pendulum))
        self.play(UpdateFromAlphaFunc(large_angle_pendulum, update_large_angle_pendulum), run_time=3, rate_func=linear)
        self.wait(1)

        # Text explaining limitations
        limitations_text = Text("Formula is an approximation for small angles.", font_size=24)
        limitations_text.to_edge(DOWN)
        self.play(Write(limitations_text))
        self.wait(3)

        self.play(FadeOut(formula, small_angle_pendulum, large_angle_pendulum, limitations_text))
        self.wait(1)
```