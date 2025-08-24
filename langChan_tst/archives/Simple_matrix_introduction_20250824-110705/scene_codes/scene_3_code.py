```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # --- Sales Data Table ---
        table = Table(
            [["Product A", "Product B"],
             ["Day 1", "150", "200"],
             ["Day 2", "180", "220"]],
            col_labels=[Text("Product"), Text("Sales")],
            row_labels=[Text("Day"), Text(""), Text("")],
            include_outer_lines=True
        )
        table.scale(0.7)
        self.play(Create(table), run_time=2)
        self.wait(1)

        self.play(FadeOut(table), run_time=1)

        # --- 2D Square Transformation ---
        square = Square(side_length=2, color=BLUE)
        grid = NumberPlane()
        grid.scale(0.5)

        self.add(grid, square)
        self.play(square.animate.rotate(PI/4), run_time=1)
        self.play(square.animate.scale(1.5), run_time=1)
        self.play(square.animate.shift(RIGHT), run_time=1)
        self.wait(1)

        self.play(FadeOut(square, grid), run_time=1)

        # --- Solving Linear Equations ---
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=6,
            y_length=6
        )

        line1 = axes.plot(lambda x: 0.5 * x + 1, color=RED)
        line2 = axes.plot(lambda x: -x + 3, color=GREEN)

        self.play(Create(axes), Create(line1), Create(line2), run_time=2)

        intersection_point = Dot(axes.coords_to_point(4/3, 5/3), color=YELLOW)
        self.play(Create(intersection_point), run_time=0.5)

        label = MathTex("(4/3, 5/3)", color=YELLOW).next_to(intersection_point, UP)
        self.play(Write(label), run_time=0.5)

        self.wait(2)
```