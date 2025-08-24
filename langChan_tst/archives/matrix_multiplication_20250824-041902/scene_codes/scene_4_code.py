import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene4(SplitScreen):
    def construct_scene(self):
        # --- Left Region: Matrix Multiplication Example ---
        # 1. Initial State: Matrices A, B, and partially filled C
        matrix_A = Matrix([[1, 2], [3, 4]])
        matrix_B = Matrix([[5, 6], [7, 8]])
        matrix_C_partial = Matrix([[19, 22], [43, "?"]])

        # Scale matrices to fit and arrange them in the left region
        matrix_A.scale(0.8)
        matrix_B.scale(0.8)
        matrix_C_partial.scale(0.8)

        # Create the multiplication and equals signs
        times_sign = MathTex("\\times").scale(1.5)
        equals_sign = MathTex("=").scale(1.5)

        # Arrange A, times, B, equals, C
        matrix_A_B_C_group = VGroup(matrix_A, times_sign, matrix_B, equals_sign, matrix_C_partial)
        matrix_A_B_C_group.arrange(RIGHT, buff=0.5)
        matrix_A_B_C_group.move_to(self.left_region.get_center())

        self.play(FadeIn(matrix_A_B_C_group), run_time=3)
        self.wait(3) # Narration: "Let's complete our example and reveal the full product matrix."

        # 2. Highlight second row of A and second column of B
        self.play(
        Indicate(matrix_A.get_rows()[1], color=YELLOW, scale_factor=1.1),
        Indicate(matrix_B.get_columns()[1], color=YELLOW, scale_factor=1.1),
        run_time=3
        )
        self.wait(2) # Narration: "For C_22, we combine the second row of A with the second column of B."

        # 3. Show calculation
        calculation_tex = MathTex(
        "(3", "\\times", "6)", "+", "(4", "\\times", "8)", "=", "18", "+", "32", "=", "50"
        )
        calculation_tex.scale(0.8)
        calculation_tex.next_to(matrix_C_partial, DOWN, buff=0.8)

        self.play(Write(calculation_tex[0:3]), run_time=2) # (3 * 6)
        self.play(Write(calculation_tex[3:7]), run_time=2) # + (4 * 8)
        self.play(Write(calculation_tex[7:]), run_time=2) # = 18 + 32 = 50
        self.wait(3)

        # 4. Fill C_22, completing the matrix
        matrix_C_completed = Matrix([[19, 22], [43, 50]])
        matrix_C_completed.scale(0.8)
        matrix_C_completed.move_to(matrix_C_partial) # Ensure it's in the same position

        # Transform the partial C matrix into the completed one
        self.play(Transform(matrix_C_partial, matrix_C_completed), run_time=2)
        self.wait(3) # Narration: "...completing the matrix C."

        # --- Transition to Right Region: Rules of Matrix Multiplication ---
        self.play(
        FadeOut(matrix_A_B_C_group, calculation_tex),
        run_time=2
        )

        # 5. Dimension Rule
        dimension_rule_tex = MathTex(
        "(m \\times n)", "\\cdot", "(n \\times p)", "\\rightarrow", "(m \\times p)"
        )
        dimension_rule_tex.scale(0.9)
        dimension_rule_tex.move_to(self.right_region.get_center())

        self.play(Write(dimension_rule_tex), run_time=4)
        self.wait(2) # Narration: "An important rule to remember: for two matrices A (m x n) and B (p x q) to be multiplied, the number of columns in A must equal the number of rows in B – so 'n' must equal 'p'."

        # 6. Highlight matching 'n's and resulting 'm x p'
        # Indexing for MathTex("(m \\times n)", "\\cdot", "(n \\times p)", "\\rightarrow", "(m \\times p)")
        # (m \times n) is dimension_rule_tex[0]
        # (n \times p) is dimension_rule_tex[2]
        # (m \times p) is dimension_rule_tex[4]
        # Inside each, e.g., (m \times n): ( is [0], m is [1], \times is [2], n is [3], ) is [4]

        # Highlight the 'n' from (m x n) and the 'n' from (n x p)
        self.play(
        Indicate(dimension_rule_tex[0][3], color=GREEN, scale_factor=1.2), # 'n' in (m x n)
        Indicate(dimension_rule_tex[2][1], color=GREEN, scale_factor=1.2), # 'n' in (n x p)
        run_time=3
        )
        self.wait(2) # Narration: "The resulting matrix C will have dimensions 'm x q'." (Note: animation shows 'm x p')

        # Highlight the 'm' from (m x n) and the 'p' from (m x p)
        self.play(
        Indicate(dimension_rule_tex[0][1], color=BLUE, scale_factor=1.2), # 'm' in (m x n)
        Indicate(dimension_rule_tex[4][3], color=BLUE, scale_factor=1.2), # 'p' in (m x p)
        run_time=3
        )
        self.wait(2)

        # 7. Non-Commutativity
        non_commutative_tex = MathTex("A \\cdot B \\neq B \\cdot A")
        non_commutative_tex.scale(0.9)
        non_commutative_tex.next_to(dimension_rule_tex, DOWN, buff=1.0)

        self.play(Write(non_commutative_tex), run_time=3)
        self.wait(3) # Narration: "Matrix multiplication is not commutative, meaning A times B is generally not equal to B times A. Keep practicing, and you'll master this essential operation!"

# Set narration and duration
Scene4.narration_text = '''Let\'s complete our example and reveal the full product matrix. For C_22, we combine the second row of A with the second column of B. An important rule to remember: for two matrices A (m x n) and B (p x q) to be multiplied, the number of columns in A must equal the number of rows in B – so \'n\' must equal \'p\'. The resulting matrix C will have dimensions \'m x q\'. Matrix multiplication is not commutative, meaning A times B is generally not equal to B times A. Keep practicing, and you\'ll master this essential operation!'''
Scene4.audio_duration = 5.0
