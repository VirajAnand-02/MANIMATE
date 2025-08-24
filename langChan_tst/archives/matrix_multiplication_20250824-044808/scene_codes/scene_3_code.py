```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices
        matrix_a = Matrix([[1, 2], [3, 4]], bracket_h_buff=0.5, bracket_v_buff=0.5)
        matrix_b = Matrix([[5, 6], [7, 8]], bracket_h_buff=0.5, bracket_v_buff=0.5)
        matrix_c = Matrix([["?", "?"], ["?", "?"]], bracket_h_buff=0.5, bracket_v_buff=0.5)

        # Position matrices
        matrix_a.to_edge(UP + LEFT)
        matrix_b.to_edge(UP + RIGHT)
        matrix_c.to_edge(DOWN)

        # Add matrices to the scene
        self.play(Write(matrix_a), Write(matrix_b))
        self.wait(1)

        # C11 calculation
        self.play(
            Indicate(matrix_a.get_rows()[0], color=RED),
            Indicate(matrix_b.get_columns()[0], color=GREEN),
            run_time=1
        )
        self.wait(0.5)

        calculation_c11 = MathTex("(1 \\times 5) + (2 \\times 7) = 5 + 14 = 19")
        calculation_c11.next_to(matrix_b, DOWN)
        self.play(Write(calculation_c11))
        self.wait(1)

        self.play(matrix_c.entries[0].animate.set_value(19))
        self.play(FadeOut(calculation_c11))
        self.wait(0.5)

        # C12 calculation
        self.play(
            Indicate(matrix_a.get_rows()[0], color=RED),
            Indicate(matrix_b.get_columns()[1], color=GREEN),
            run_time=1
        )
        self.wait(0.5)

        calculation_c12 = MathTex("(1 \\times 6) + (2 \\times 8) = 6 + 16 = 22")
        calculation_c12.next_to(matrix_b, DOWN)
        self.play(Write(calculation_c12))
        self.wait(1)

        self.play(matrix_c.entries[1].animate.set_value(22))
        self.play(FadeOut(calculation_c12))
        self.wait(0.5)

        # C21 calculation
        self.play(
            Indicate(matrix_a.get_rows()[1], color=RED),
            Indicate(matrix_b.get_columns()[0], color=GREEN),
            run_time=1
        )
        self.wait(0.5)

        calculation_c21 = MathTex("(3 \\times 5) + (4 \\times 7) = 15 + 28 = 43")
        calculation_c21.next_to(matrix_b, DOWN)
        self.play(Write(calculation_c21))
        self.wait(1)

        self.play(matrix_c.entries[2].animate.set_value(43))
        self.play(FadeOut(calculation_c21))
        self.wait(0.5)

        # C22 calculation
        self.play(
            Indicate(matrix_a.get_rows()[1], color=RED),
            Indicate(matrix_b.get_columns()[1], color=GREEN),
            run_time=1
        )
        self.wait(0.5)

        calculation_c22 = MathTex("(3 \\times 6) + (4 \\times 8) = 18 + 32 = 50")
        calculation_c22.next_to(matrix_b, DOWN)
        self.play(Write(calculation_c22))
        self.wait(1)

        self.play(matrix_c.entries[3].animate.set_value(50))
        self.play(FadeOut(calculation_c22))
        self.wait(0.5)

        # Final matrix C
        final_matrix_c = Matrix([[19, 22], [43, 50]], bracket_h_buff=0.5, bracket_v_buff=0.5)
        final_matrix_c.to_edge(DOWN)
        self.play(Transform(matrix_c, final_matrix_c))
        self.wait(2)
```