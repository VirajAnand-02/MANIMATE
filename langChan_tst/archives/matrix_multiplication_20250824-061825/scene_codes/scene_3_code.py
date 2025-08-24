```python
from manim import *

class GeneratedScene_3(Scene):
    def construct(self):
        # Define matrices A and B
        matrix_a_data = [[1, 2], [3, 4]]
        matrix_b_data = [[5, 6], [7, 8]]

        matrix_a = Matrix(matrix_a_data, element_to_mobject=MathTex)
        matrix_b = Matrix(matrix_b_data, element_to_mobject=MathTex)

        # Position matrices A and B
        matrix_a.to_edge(UP + LEFT)
        matrix_b.to_edge(UP + RIGHT)

        # Create blank result matrix C
        matrix_c_data = [["?", "?"], ["?", "?"]]
        matrix_c = Matrix(matrix_c_data, element_to_mobject=MathTex)
        matrix_c.to_edge(DOWN)

        # Add matrices to the scene
        self.play(Create(matrix_a), Create(matrix_b), Create(matrix_c))
        self.wait(1)

        # C11 calculation
        self.highlight_row_column(matrix_a, 0, matrix_b, 0)
        c11_calc = MathTex("(1*5) + (2*7) = 5 + 14 = 19").scale(0.7).next_to(matrix_c, UP)
        self.play(Write(c11_calc))
        self.wait(1)
        self.fill_matrix_element(matrix_c, 0, 0, "19")
        self.play(FadeOut(c11_calc))
        self.reset_highlight(matrix_a, matrix_b)
        self.wait(0.5)

        # C12 calculation
        self.highlight_row_column(matrix_a, 0, matrix_b, 1)
        c12_calc = MathTex("(1*6) + (2*8) = 6 + 16 = 22").scale(0.7).next_to(matrix_c, UP)
        self.play(Write(c12_calc))
        self.wait(1)
        self.fill_matrix_element(matrix_c, 0, 1, "22")
        self.play(FadeOut(c12_calc))
        self.reset_highlight(matrix_a, matrix_b)
        self.wait(0.5)

        # C21 calculation
        self.highlight_row_column(matrix_a, 1, matrix_b, 0)
        c21_calc = MathTex("(3*5) + (4*7) = 15 + 28 = 43").scale(0.7).next_to(matrix_c, UP)
        self.play(Write(c21_calc))
        self.wait(1)
        self.fill_matrix_element(matrix_c, 1, 0, "43")
        self.play(FadeOut(c21_calc))
        self.reset_highlight(matrix_a, matrix_b)
        self.wait(0.5)

        # C22 calculation
        self.highlight_row_column(matrix_a, 1, matrix_b, 1)
        c22_calc = MathTex("(3*6) + (4*8) = 18 + 32 = 50").scale(0.7).next_to(matrix_c, UP)
        self.play(Write(c22_calc))
        self.wait(1)
        self.fill_matrix_element(matrix_c, 1, 1, "50")
        self.play(FadeOut(c22_calc))
        self.reset_highlight(matrix_a, matrix_b)
        self.wait(1)

        self.wait(2)

    def highlight_row_column(self, matrix_a, row_index, matrix_b, col_index):
        self.play(
            matrix_a.get_rows()[row_index].animate.set_color(YELLOW),
            matrix_b.get_columns()[col_index].animate.set_color(YELLOW)
        )

    def reset_highlight(self, matrix_a, matrix_b):
        self.play(
            matrix_a.get_rows().animate.set_color(WHITE),
            matrix_b.get_columns().animate.set_color(WHITE)
        )

    def fill_matrix_element(self, matrix, row, col, value):
        matrix.add_updater(lambda m: m.become(Matrix([["19" if i==0 and j==0 else m.matrix[i][j].expression for j in range(len(m.matrix[0]))] if i==0 else ["22" if i==1 and j==0 else m.matrix[i][j].expression for j in range(len(m.matrix[0]))] if i==1 else ["43" if i==0 and j==1 else m.matrix[i][j].expression for j in range(len(m.matrix[0]))] if i==2 else ["50" if i==1 and j==1 else m.matrix[i][j].expression for j in range(len(m.matrix[0]))] for i in range(len(m.matrix))], element_to_mobject=MathTex)))
        self.play(matrix.animate.change_element([row, col], value))
        matrix.clear_updaters()
        self.remove(matrix)
        matrix_data = [["19" if i==0 and col_index==0 else "?" for col_index in range(2)] if i==0 else ["43" if i==1 and col_index==0 else "?" for col_index in range(2)] if i==1 else ["22" if i==0 and col_index==1 else "?" for col_index in range(2)] if i==2 else ["50" if i==1 and col_index==1 else "?" for col_index in range(2)] for i in range(2)]
        matrix = Matrix(matrix_data, element_to_mobject=MathTex)
        matrix.to_edge(DOWN)
        self.add(matrix)
```