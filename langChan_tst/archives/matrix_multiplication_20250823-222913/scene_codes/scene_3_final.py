# Scene 3 - Final Combined Code
# Layout: split_screen
# Generated at: 2025-08-23 22:35:42

import sys
sys.path.append('..')
from layouts import SplitScreen

class Scene3(SplitScreen):
    def construct_scene(self):
        text_content = "To find any single element in the product matrix, say at row 'i' and column 'j', you take the 'i-th' row of the first matrix and the 'j-th' column of the second matrix. Then, you multiply corresponding elements from that row and column, and sum them all up. This is essentially a dot product operation."
                textbox = self.create_textbox(text_content, self.left_region.width, self.left_region.height)
                textbox.move_to(self.left_region)
                self.play(Write(textbox), run_time=3)
                self.wait(1)
        
                matrix_A = Matrix([["a_{i1}", "a_{i2}", r"\dots", "a_{in}"], ["", "", "", ""]],
                                  element_alignment_corner=DOWN,
                                  v_buff=2.5,
                                  h_buff=1.8,
                                  left_bracket="[",
                                  right_bracket="]").move_to(self.right_region).shift(LEFT * 4 + UP)
                matrix_A_label = MathTex("A").next_to(matrix_A, UP)
        
                matrix_B = Matrix([["b_{1j}"], ["b_{2j}"], [r"\vdots"], ["b_{nj}"]],
                                  element_alignment_corner=RIGHT,
                                  h_buff=2.5,
                                  left_bracket="[",
                                  right_bracket="]").next_to(matrix_A, RIGHT, buff=1)
                matrix_B_label = MathTex("B").next_to(matrix_B, UP)
        
                matrix_C = Matrix([["c_{ij}"]], left_bracket="[", right_bracket="]").next_to(matrix_B, RIGHT, buff=1.5)
                matrix_C_label = MathTex("C").next_to(matrix_C, UP)
        
                mult_sign = MathTex(r"\times").move_to(matrix_A.get_right() + (matrix_B.get_left() - matrix_A.get_right())/2)
                eq_sign = MathTex("=").move_to(matrix_B.get_right() + (matrix_C.get_left() - matrix_B.get_right())/2)
        
                self.play(
                    Write(VGroup(matrix_A_label, matrix_B_label, matrix_C_label)),
                    Create(matrix_A), Create(matrix_B), Create(matrix_C),
                    Write(mult_sign), Write(eq_sign)
                )
                self.wait(1)
        
                row_i = matrix_A.get_rows()[0]
                col_j = matrix_B.get_columns()[0]
        
                row_highlight = SurroundingRectangle(row_i, color=BLUE, buff=0.1)
                col_highlight = SurroundingRectangle(col_j, color=YELLOW, buff=0.1)
                self.play(Create(row_highlight), Create(col_highlight))
                self.wait(1)
        
                row_copies = row_i.copy()
                col_copies = col_j.copy()
                
                row_arrow = Arrow(row_highlight.get_bottom(), self.right_region.get_center() + DOWN, color=BLUE)
                col_arrow = Arrow(col_highlight.get_bottom(), self.right_region.get_center() + DOWN, color=YELLOW)
        
                self.play(
                    GrowArrow(row_arrow),
                    GrowArrow(col_arrow),
                    row_copies.animate.move_to(self.right_region.get_center() + DOWN + LEFT * 2.5).scale(0.9),
                    col_copies.animate.move_to(self.right_region.get_center() + DOWN + RIGHT * 2.5).scale(0.9)
                )
                self.wait(0.5)
        
                term1_A, term2_A, _, termN_A = row_copies
                term1_B, term2_B, _, termN_B = col_copies
                
                term_pairs = [
                    (term1_A, term1_B),
                    (term2_A, term2_B),
                    (termN_A, termN_B)
                ]
                
                products = VGroup()
                plus_signs = VGroup()
        
                for i, (termA, termB) in enumerate(term_pairs):
                    pair_group = VGroup(termA.copy(), termB.copy())
                    product_tex = MathTex(f"a_{'i'+str(i+1) if i < 2 else 'in'}", r"\cdot", f"b_{str(i+1)+'j' if i < 2 else 'nj'}")
                    if i == 2:
                        product_tex = MathTex("a_{in}", r"\cdot", "b_{nj}")
                    
                    if i == 0:
                        product_tex.move_to(row_arrow.get_end() + DOWN * 1.5 + LEFT * 2)
                    elif i == 1:
                        product_tex.next_to(products, RIGHT)
                        plus = MathTex("+").next_to(products, RIGHT)
                        plus_signs.add(plus)
                    else:
                        product_tex.next_to(products, RIGHT)
                        plus = MathTex("+ \dots +").next_to(products, RIGHT)
                        plus_signs.add(plus)
        
                    self.play(Transform(pair_group, product_tex))
                    products.add(product_tex)
                    if i > 0:
                        self.play(Write(plus))
                        products.add(plus)
        
                self.wait(1)
                
                final_sum_group = VGroup(*products, *plus_signs)
                target_cell = matrix_C.get_entries()[0]
                result_highlight = SurroundingRectangle(target_cell, color=GREEN)
                
                self.play(Create(result_highlight))
        
                sum_arrow = Arrow(final_sum_group.get_top(), target_cell.get_bottom(), color=GREEN, buff=0.2)
                
                self.play(
                    FadeOut(row_arrow, col_arrow, row_copies, col_copies),
                    GrowArrow(sum_arrow)
                )
                
                self.play(ReplacementTransform(final_sum_group, target_cell.copy().move_to(target_cell.get_center())))
                self.wait(2)
                
                self.play(
                    FadeOut(row_highlight),
                    FadeOut(col_highlight),
                    FadeOut(result_highlight),
                    FadeOut(sum_arrow)
                )
                self.wait(2)

Scene3.narration_text = """Let's dive into how it works. To find any single element in the product matrix, say at row 'i' and column 'j', you take the 'i-th' row of the first matrix and the 'j-th' column of the second matrix. Then, you multiply corresponding elements from that row and column, and sum them all up. This is essentially a dot product operation."""
Scene3.audio_duration = 23.210958
