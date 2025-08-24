```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices A and B
        matrix_a = Matrix([["a11", "a12"], ["a21", "a22"]], matrix_config={"bracket_h_buff": 0.75, "bracket_v_buff": 0.5})
        matrix_b = Matrix([["b11", "b12"], ["b21", "b22"]], matrix_config={"bracket_h_buff": 0.75, "bracket_v_buff": 0.5})
        matrix_c = Matrix([["c11", "c12"], ["c21", "c22"]], matrix_config={"bracket_h_buff": 0.75, "bracket_v_buff": 0.5})

        # Position matrices
        matrix_a.to_edge(LEFT)
        matrix_b.to_edge(RIGHT)
        matrix_c.move_to(DOWN)

        arrow = Arrow(matrix_b.get_right(), matrix_c.get_top(), buff=0.5)

        # Add matrices to the scene
        self.play(Create(matrix_a), Create(matrix_b), Create(arrow), Create(matrix_c))
        self.wait(1)

        # C11 calculation
        self.play(
            matrix_a.get_rows()[0].animate.set_color(RED),
            matrix_b.get_columns()[0].animate.set_color(BLUE)
        )
        c11_calculation = MathTex("a11 \\cdot b11 + a12 \\cdot b21").next_to(matrix_c, UP)
        self.play(Write(c11_calculation))
        self.wait(1)
        self.play(Transform(c11_calculation, MathTex("c11").move_to(c11_calculation.get_center())))
        self.play(FadeOut(c11_calculation))
        self.play(matrix_c.get_entries()[0].animate.become(MathTex("c11").move_to(matrix_c.get_entries()[0].get_center())))
        self.play(
            matrix_a.get_rows()[0].animate.set_color(WHITE),
            matrix_b.get_columns()[0].animate.set_color(WHITE)
        )
        self.wait(0.5)

        # C12 calculation
        self.play(
            matrix_a.get_rows()[0].animate.set_color(RED),
            matrix_b.get_columns()[1].animate.set_color(BLUE)
        )
        c12_calculation = MathTex("a11 \\cdot b12 + a12 \\cdot b22").next_to(matrix_c, UP)
        self.play(Write(c12_calculation))
        self.wait(1)
        self.play(Transform(c12_calculation, MathTex("c12").move_to(c12_calculation.get_center())))
        self.play(FadeOut(c12_calculation))
        self.play(matrix_c.get_entries()[1].animate.become(MathTex("c12").move_to(matrix_c.get_entries()[1].get_center())))
        self.play(
            matrix_a.get_rows()[0].animate.set_color(WHITE),
            matrix_b.get_columns()[1].animate.set_color(WHITE)
        )
        self.wait(0.5)

        # C21 calculation
        self.play(
            matrix_a.get_rows()[1].animate.set_color(RED),
            matrix_b.get_columns()[0].animate.set_color(BLUE)
        )
        c21_calculation = MathTex("a21 \\cdot b11 + a22 \\cdot b21").next_to(matrix_c, UP)
        self.play(Write(c21_calculation))
        self.wait(1)
        self.play(Transform(c21_calculation, MathTex("c21").move_to(c21_calculation.get_center())))
        self.play(FadeOut(c21_calculation))
        self.play(matrix_c.get_entries()[2].animate.become(MathTex("c21").move_to(matrix_c.get_entries()[2].get_center())))
        self.play(
            matrix_a.get_rows()[1].animate.set_color(WHITE),
            matrix_b.get_columns()[0].animate.set_color(WHITE)
        )
        self.wait(0.5)

        # C22 calculation
        self.play(
            matrix_a.get_rows()[1].animate.set_color(RED),
            matrix_b.get_columns()[1].animate.set_color(BLUE)
        )
        c22_calculation = MathTex("a21 \\cdot b12 + a22 \\cdot b22").next_to(matrix_c, UP)
        self.play(Write(c22_calculation))
        self.wait(1)
        self.play(Transform(c22_calculation, MathTex("c22").move_to(c22_calculation.get_center())))
        self.play(FadeOut(c22_calculation))
        self.play(matrix_c.get_entries()[3].animate.become(MathTex("c22").move_to(matrix_c.get_entries()[3].get_center())))
        self.play(
            matrix_a.get_rows()[1].animate.set_color(WHITE),
            matrix_b.get_columns()[1].animate.set_color(WHITE)
        )
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
```