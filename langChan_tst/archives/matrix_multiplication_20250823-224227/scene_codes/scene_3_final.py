# Scene 3 - Final Combined Code
# Layout: split_screen
# Generated at: 2025-08-23 22:46:40

import sys
sys.path.append('..')
from layouts import SplitScreen

class Scene3(SplitScreen):
    def construct_scene(self):
        text_content = "To find an element in the product matrix, you take a row from the first matrix and a column from the second matrix. Multiply corresponding elements and sum the results. For example, to get the element in row 1, column 1 of the product, you multiply row 1 of the first matrix by column 1 of the second matrix."
        textbox = self.create_textbox(text_content, self.left_region.width * 0.9, self.left_region.height * 0.9)
        textbox.move_to(self.left_region.get_center())
        self.play(Write(textbox), run_time=2)
        self.wait(1)
        
        mat_A = Matrix([["a_{11}", "a_{12}"], ["a_{21}", "a_{22}"]], v_buff=1.2, h_buff=1.2, left_bracket="[", right_bracket="]")
        mat_B = Matrix([["b_{11}", "b_{12}"], ["b_{21}", "b_{22}"]], v_buff=1.2, h_buff=1.2, left_bracket="[", right_bracket="]")
        mat_C = Matrix([["?", "?"], ["?", "?"]], v_buff=1.2, h_buff=1.2, left_bracket="[", right_bracket="]")
        
        label_A = MathTex("A =").next_to(mat_A, LEFT)
        label_B = MathTex("B =").next_to(mat_B, LEFT)
        label_C = MathTex("C =").next_to(mat_C, LEFT)
        
        group_A = VGroup(label_A, mat_A)
        group_B = VGroup(label_B, mat_B)
        group_C = VGroup(label_C, mat_C)
        
        eq_group = VGroup(group_A, group_B).arrange(RIGHT, buff=1.5)
        final_group = VGroup(eq_group, group_C).arrange(DOWN, buff=1.5)
        final_group.move_to(self.right_region.get_center()).shift(UP)
        self.play(Write(group_A), Write(group_B))
        self.wait(0.5)
        
        row1_A = mat_A.get_rows()[0]
        col1_B = mat_B.get_columns()[0]
        highlight_row1_A = SurroundingRectangle(row1_A, color=BLUE, buff=0.15)
        highlight_col1_B = SurroundingRectangle(col1_B, color=YELLOW, buff=0.15)
        
        self.play(Create(highlight_row1_A), Create(highlight_col1_B))
        self.wait(1)
        
        calc_text_1 = MathTex(
            "c_{11}", "=", "a_{11}", "\\times", "b_{11}", "+", "a_{12}", "\\times", "b_{21}"
        ).scale(0.9)
        calc_text_1.next_to(final_group, DOWN, buff=1)
        
        c11_target = mat_C.get_entries()[0]
        highlight_c11 = SurroundingRectangle(c11_target, color=GREEN, buff=0.15)
        
        self.play(TransformFromCopy(VGroup(mat_A.get_entries()[0], mat_B.get_entries()[0]), VGroup(calc_text_1.get_part_by_tex("a_{11}"), calc_text_1.get_part_by_tex("b_{11}"))))
        self.play(Write(VGroup(calc_text_1.get_part_by_tex("="), calc_text_1.get_part_by_tex("\\times")[0], calc_text_1.get_part_by_tex("+"))))
        self.play(TransformFromCopy(VGroup(mat_A.get_entries()[1], mat_B.get_entries()[2]), VGroup(calc_text_1.get_part_by_tex("a_{12}"), calc_text_1.get_part_by_tex("b_{21}"))))
        self.play(Write(calc_text_1.get_part_by_tex("\\times")[1]))
        self.wait(1)
        
        self.play(Write(group_C))
        self.play(Create(highlight_c11))
        self.play(ReplacementTransform(calc_text_1, MathTex("c_{11}").move_to(c11_target)))
        self.wait(1.5)
        
        self.play(FadeOut(highlight_c11, highlight_row1_A, highlight_col1_B))
        self.wait(0.5)
        
        col2_B = mat_B.get_columns()[1]
        highlight_col2_B = SurroundingRectangle(col2_B, color=YELLOW, buff=0.15)
        self.play(Create(highlight_row1_A), Create(highlight_col2_B))
        self.wait(1)
        
        calc_text_2 = MathTex(
            "c_{12}", "=", "a_{11}", "\\times", "b_{12}", "+", "a_{12}", "\\times", "b_{22}"
        ).scale(0.9)
        calc_text_2.next_to(final_group, DOWN, buff=1)
        
        c12_target = mat_C.get_entries()[1]
        highlight_c12 = SurroundingRectangle(c12_target, color=GREEN, buff=0.15)
        
        self.play(TransformFromCopy(VGroup(mat_A.get_entries()[0], mat_B.get_entries()[1]), VGroup(calc_text_2.get_part_by_tex("a_{11}"), calc_text_2.get_part_by_tex("b_{12}"))))
        self.play(Write(VGroup(calc_text_2.get_part_by_tex("="), calc_text_2.get_part_by_tex("\\times")[0], calc_text_2.get_part_by_tex("+"))))
        self.play(TransformFromCopy(VGroup(mat_A.get_entries()[1], mat_B.get_entries()[3]), VGroup(calc_text_2.get_part_by_tex("a_{12}"), calc_text_2.get_part_by_tex("b_{22}"))))
        self.play(Write(calc_text_2.get_part_by_tex("\\times")[1]))
        self.wait(1)
        
        self.play(Create(highlight_c12))
        self.play(ReplacementTransform(calc_text_2, MathTex("c_{12}").move_to(c12_target)))
        self.wait(1.5)
        
        self.play(FadeOut(highlight_c12, highlight_row1_A, highlight_col2_B))
        self.wait(2)

Scene3.narration_text = """To find an element in the product matrix, you take a row from the first matrix and a column from the second matrix. Multiply corresponding elements and sum the results. For example, to get the element in row 1, column 1 of the product, you multiply row 1 of the first matrix by column 1 of the second matrix."""
Scene3.audio_duration = 21.290958
