# Scene 2 - Final Combined Code
# Layout: split_screen
# Generated at: 2025-08-23 22:46:02

import sys
sys.path.append('..')
from layouts import SplitScreen

class Scene2(SplitScreen):
    def construct_scene(self):
        # 1. Create Title Text
                text_content = "Before we multiply, there's an important rule: the number of columns in the first matrix must equal the number of rows in the second matrix. If you have an M by N matrix and an N by P matrix, the result will be an M by P matrix. Otherwise, multiplication is not possible!"
                textbox = self.create_textbox(text_content, self.left_region.width * 0.9, self.left_region.height)
                textbox.move_to(self.left_region.get_center())
                self.play(Write(textbox))
                self.wait(1)
        
                # 2. Create Matching Matrices (A and B)
                matrix_A_mob = Matrix([["a", "b", "c"], ["d", "e", "f"]], h_buff=1.5)
                label_A = MathTex("A").next_to(matrix_A_mob, UP)
                dims_A = MathTex("2 \\times 3").next_to(matrix_A_mob, DOWN)
                group_A = VGroup(label_A, matrix_A_mob, dims_A)
        
                matrix_B_mob = Matrix([["u", "v"], ["w", "x"], ["y", "z"]], v_buff=1.3)
                label_B = MathTex("B").next_to(matrix_B_mob, UP)
                dims_B = MathTex("3 \\times 2").next_to(matrix_B_mob, DOWN)
                group_B = VGroup(label_B, matrix_B_mob, dims_B)
        
                times_symbol_1 = MathTex("\\times").scale(2)
                
                valid_pair = VGroup(group_A, times_symbol_1, group_B).arrange(RIGHT, buff=0.8)
                valid_pair.move_to(self.right_region.get_center()).shift(UP * 2)
        
                self.play(
                    Create(matrix_A_mob),
                    Write(label_A),
                    Write(dims_A),
                )
                self.wait(0.5)
                self.play(
                    Write(times_symbol_1),
                    Create(matrix_B_mob),
                    Write(label_B),
                    Write(dims_B)
                )
                self.wait(1)
        
                # 3. Highlight Matching Inner Dimensions
                inner_dim_A = dims_A[0][2]
                inner_dim_B = dims_B[0][0]
                
                highlight_box_A = SurroundingRectangle(inner_dim_A, color=GREEN, buff=0.1)
                highlight_box_B = SurroundingRectangle(inner_dim_B, color=GREEN, buff=0.1)
                
                match_text = Text("Match!", color=GREEN).next_to(valid_pair, DOWN, buff=0.5)
        
                self.play(
                    Create(highlight_box_A),
                    Create(highlight_box_B)
                )
                self.play(Write(match_text))
                self.wait(2)
                
                self.play(
                    FadeOut(highlight_box_A),
                    FadeOut(highlight_box_B),
                    FadeOut(match_text)
                )
                self.wait(0.5)
        
                # 4. Create Non-Matching Matrices (C and D)
                matrix_C_mob = Matrix([["g", "h"], ["i", "j"]])
                label_C = MathTex("C").next_to(matrix_C_mob, UP)
                dims_C = MathTex("2 \\times 2").next_to(matrix_C_mob, DOWN)
                group_C = VGroup(label_C, matrix_C_mob, dims_C)
        
                matrix_D_mob = Matrix([["u", "v"], ["w", "x"], ["y", "z"]], v_buff=1.3)
                label_D = MathTex("D").next_to(matrix_D_mob, UP)
                dims_D = MathTex("3 \\times 2").next_to(matrix_D_mob, DOWN)
                group_D = VGroup(label_D, matrix_D_mob, dims_D)
                
                times_symbol_2 = MathTex("\\times").scale(2)
        
                invalid_pair = VGroup(group_C, times_symbol_2, group_D).arrange(RIGHT, buff=0.8)
                invalid_pair.move_to(self.right_region.get_center()).shift(DOWN * 2)
                
                self.play(
                    ReplacementTransform(group_A.copy(), group_C),
                    ReplacementTransform(times_symbol_1.copy(), times_symbol_2),
                    ReplacementTransform(group_B.copy(), group_D),
                )
                self.wait(1)
        
                # 5. Highlight Mismatch and show Red X
                inner_dim_C = dims_C[0][2]
                inner_dim_D = dims_D[0][0]
        
                highlight_box_C = SurroundingRectangle(inner_dim_C, color=RED, buff=0.1)
                highlight_box_D = SurroundingRectangle(inner_dim_D, color=RED, buff=0.1)
        
                red_X = Cross(invalid_pair, stroke_color=RED, stroke_width=8)
                
                self.play(
                    Create(highlight_box_C),
                    Create(highlight_box_D)
                )
                self.wait(1)
                self.play(Create(red_X))
                self.wait(2)

Scene2.narration_text = """Before we multiply, there's an important rule: the number of columns in the first matrix must equal the number of rows in the second matrix. If you have an M by N matrix and an N by P matrix, the result will be an M by P matrix. Otherwise, multiplication is not possible!"""
Scene2.audio_duration = 21.050958
