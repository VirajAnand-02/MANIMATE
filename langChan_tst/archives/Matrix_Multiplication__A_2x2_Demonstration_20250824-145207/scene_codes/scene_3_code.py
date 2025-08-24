import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import SplitScreen
import numpy as np

class Scene3(SplitScreen):
    def construct_scene(self):
        from manim import *

        def construct_scene(self):
        # --- Setup Matrices ---
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C_initial = Matrix([["?", "?"], ["?", "?"]]) # Placeholder for result matrix

        mult_sign = MathTex("\\times")
        eq_sign = MathTex("=")

        # Arrange matrices horizontally in the left region
        matrices_group = VGroup(A, mult_sign, B, eq_sign, C_initial).arrange(RIGHT, buff=0.7)
        matrices_group.move_to(self.left_region.get_center())

        # Display initial matrices
        self.play(
        FadeIn(A, shift=LEFT),
        FadeIn(mult_sign),
        FadeIn(B, shift=RIGHT),
        FadeIn(eq_sign),
        FadeIn(C_initial, shift=RIGHT)
        )
        self.wait(0.5)

        # --- C12 Calculation ---
        # Highlight row 1 of A and column 2 of B
        rect_A_row1 = SurroundingRectangle(A.get_rows()[0], color=YELLOW, buff=0.1)
        rect_B_col2 = SurroundingRectangle(B.get_columns()[1], color=YELLOW, buff=0.1)
        self.play(Create(rect_A_row1), Create(rect_B_col2))
        self.wait(0.5)

        # Show calculation steps on the right
        calc_c12_line1 = MathTex("(1 \\times 6) + (2 \\times 8)")
        calc_c12_line2 = MathTex("= 6 + 16")
        calc_c12_line3 = MathTex("= 22")

        # Arrange calculation lines and position in the right region
        calc_c12_group = VGroup(calc_c12_line1, calc_c12_line2, calc_c12_line3).arrange(DOWN, aligned_edge=LEFT)
        calc_c12_group.move_to(self.right_region.get_center())

        self.play(Write(calc_c12_line1))
        self.wait(0.5)
        self.play(TransformMatchingTex(calc_c12_line1, calc_c12_line2))
        self.wait(0.5)
        self.play(TransformMatchingTex(calc_c12_line2, calc_c12_line3))
        self.wait(0.5)

        # Animate '22' sliding into the C12 position of matrix C
        # C[0][1] is the second element in the flat list of entries (index 1)
        c12_target_pos = C_initial.get_entries()[1].get_center() 
        result_22_mobj = calc_c12_line3.copy().move_to(c12_target_pos) # Create a copy to move

        self.play(
        Transform(C_initial.get_entries()[1], result_22_mobj), # Transform the '?' mobject to '22'
        FadeOut(calc_c12_line3), # Fade out the original calculation result
        FadeOut(rect_A_row1),
        FadeOut(rect_B_col2)
        )
        self.wait(0.5)

        # --- C21 Calculation ---
        # Highlight row 2 of A and column 1 of B
        rect_A_row2 = SurroundingRectangle(A.get_rows()[1], color=YELLOW, buff=0.1)
        rect_B_col1 = SurroundingRectangle(B.get_columns()[0], color=YELLOW, buff=0.1)
        self.play(Create(rect_A_row2), Create(rect_B_col1))
        self.wait(0.5)

        # Show calculation steps on the right
        calc_c21_line1 = MathTex("(3 \\times 5) + (4 \\times 7)")
        calc_c21_line2 = MathTex("= 15 + 28")
        calc_c21_line3 = MathTex("= 43")

        # Arrange calculation lines and position in the right region
        calc_c21_group = VGroup(calc_c21_line1, calc_c21_line2, calc_c21_line3).arrange(DOWN, aligned_edge=LEFT)
        calc_c21_group.move_to(self.right_region.get_center())

        self.play(Write(calc_c21_line1))
        self.wait(0.5)
        self.play(TransformMatchingTex(calc_c21_line1, calc_c21_line2))
        self.wait(0.5)
        self.play(TransformMatchingTex(calc_c21_line2, calc_c21_line3))
        self.wait(0.5)

        # Animate '43' sliding into the C21 position of matrix C
        # C[1][0] is the third element in the flat list of entries (index 2)
        c21_target_pos = C_initial.get_entries()[2].get_center() 
        result_43_mobj = calc_c21_line3.copy().move_to(c21_target_pos)

        self.play(
        Transform(C_initial.get_entries()[2], result_43_mobj), # Transform the '?' mobject to '43'
        FadeOut(calc_c21_line3), # Fade out the original calculation result
        FadeOut(rect_A_row2),
        FadeOut(rect_B_col1)
        )
        self.wait(1) # Final wait

# Set narration and duration
Scene3.narration_text = '''Next, let\'s find C12, the element in the first row, second column of C. We use the first row of A again, but this time, the second column of B. So, it\'s (1 times 6) plus (2 times 8). That\'s 6 plus 16, resulting in 22. This goes into the C12 spot. Now for C21, second row, first column. We take the second row of A, which is [3, 4], and the first column of B, [5, 7]. This gives us (3 times 5) plus (4 times 7). That\'s 15 plus 28, totaling 43. And that fills our C21 position.'''
Scene3.audio_duration = 5.0
