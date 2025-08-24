```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices A and B
        matrix_a_data = [[1, 2, 3], [4, 5, 6]]
        matrix_b_data = [[7, 8], [9, 10], [11, 12]]

        matrix_a = Matrix(matrix_a_data)
        matrix_b = Matrix(matrix_b_data)

        # Position matrices
        matrix_a.to_edge(LEFT)
        matrix_b.to_edge(RIGHT)

        # Compatibility rule text
        compatibility_text = Tex("Columns of A = Rows of B", color=YELLOW)
        compatibility_text.move_to(UP)

        # Highlight compatibility
        rect_a = Rectangle(width=0.5, height=matrix_a.get_height() + 0.5).move_to(matrix_a.get_right() + RIGHT * 0.25)
        rect_b = Rectangle(width=matrix_b.get_width() + 0.5, height=0.5).move_to(matrix_b.get_top() + UP * 0.25)
        rect_a.set_color(YELLOW)
        rect_b.set_color(YELLOW)

        # Show matrices and compatibility
        self.play(Write(matrix_a), Write(matrix_b))
        self.play(Write(compatibility_text))
        self.play(Create(rect_a), Create(rect_b))
        self.wait(1)

        # Animate calculation of first element (0,0)
        result_matrix = Matrix([[0, 0], [0, 0]])
        result_matrix.move_to(DOWN)
        self.play(FadeOut(compatibility_text), FadeOut(rect_a), FadeOut(rect_b))
        self.play(Write(result_matrix))

        # Highlight first row of A and first column of B
        row_a = SurroundingRectangle(matrix_a.get_rows()[0], color=GREEN)
        col_b = SurroundingRectangle(matrix_b.get_columns()[0], color=GREEN)

        self.play(Create(row_a), Create(col_b))
        self.wait(0.5)

        # Element-wise multiplication and arrows
        arrow1 = Arrow(matrix_a.get_entries()[0].get_center(), matrix_b.get_entries()[0].get_center(), color=BLUE)
        arrow2 = Arrow(matrix_a.get_entries()[1].get_center(), matrix_b.get_entries()[2].get_center(), color=BLUE)
        arrow3 = Arrow(matrix_a.get_entries()[2].get_center(), matrix_b.get_entries()[4].get_center(), color=BLUE)

        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.wait(0.5)

        # Summation
        sum_text = MathTex("1*7 + 2*9 + 3*11 = 58", color=ORANGE).move_to(DOWN + DOWN * 2)
        self.play(Write(sum_text))
        self.wait(0.5)

        # Update result matrix
        self.play(Transform(result_matrix.get_entries()[0], MathTex("58").move_to(result_matrix.get_entries()[0].get_center())))
        self.wait(1)

        # Fade out first element calculation
        self.play(FadeOut(row_a), FadeOut(col_b), FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(sum_text))

        # Animate calculation of second element (0,1)
        row_a = SurroundingRectangle(matrix_a.get_rows()[0], color=GREEN)
        col_b = SurroundingRectangle(matrix_b.get_columns()[1], color=GREEN)

        self.play(Create(row_a), Create(col_b))
        self.wait(0.5)

        # Element-wise multiplication and arrows
        arrow1 = Arrow(matrix_a.get_entries()[0].get_center(), matrix_b.get_entries()[1].get_center(), color=BLUE)
        arrow2 = Arrow(matrix_a.get_entries()[1].get_center(), matrix_b.get_entries()[3].get_center(), color=BLUE)
        arrow3 = Arrow(matrix_a.get_entries()[2].get_center(), matrix_b.get_entries()[5].get_center(), color=BLUE)

        self.play(Create(arrow1), Create(arrow2), Create(arrow3))
        self.wait(0.5)

        # Summation
        sum_text = MathTex("1*8 + 2*10 + 3*12 = 64", color=ORANGE).move_to(DOWN + DOWN * 2)
        self.play(Write(sum_text))
        self.wait(0.5)

        # Update result matrix
        self.play(Transform(result_matrix.get_entries()[1], MathTex("64").move_to(result_matrix.get_entries()[1].get_center())))
        self.wait(1)

        # Fade out second element calculation
        self.play(FadeOut(row_a), FadeOut(col_b), FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(sum_text))

        # Fade out everything
        self.play(FadeOut(matrix_a), FadeOut(matrix_b), FadeOut(result_matrix))
        self.wait(1)
```