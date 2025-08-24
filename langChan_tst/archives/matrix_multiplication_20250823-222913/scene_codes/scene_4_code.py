# Scene 4 - Generated via Batch Manim LLM
# Thinking used: False
# Generated at: 2025-08-23 22:32:51

self.wait(0.5)
text_str = "Let's illustrate with an example: a 2x2 matrix A multiplied by a 2x2 matrix B. We'll systematically calculate each element of the product. For the top-left element, we multiply the first row of A by the first column of B. For the top-right, the first row of A by the second column of B, and so on for all four positions."
textbox = self.create_textbox(text_str, self.left_region.width, self.left_region.height)
textbox.move_to(self.left_region.get_center())
self.play(Write(textbox))
self.wait(1)

mat_A = Matrix([["1", "2"], ["3", "4"]], h_buff=1.3)
mat_B = Matrix([["5", "6"], ["7", "8"]], h_buff=1.3)
mat_C_placeholders = Matrix([["?", "?"], ["?", "?"]], h_buff=1.3)

label_A = MathTex("A =").next_to(mat_A, LEFT)
label_B = MathTex("B =").next_to(mat_B, LEFT)
times_op = MathTex(r"\times").scale(1.5)
equals_op = MathTex("=").scale(1.5)

expression = VGroup(
    VGroup(label_A, mat_A).arrange(RIGHT),
    times_op,
    VGroup(label_B, mat_B).arrange(RIGHT),
    equals_op,
    mat_C_placeholders
).arrange(RIGHT, buff=0.4).move_to(self.right_region).scale(0.9)

self.play(FadeIn(expression, shift=UP))
self.wait(1)

c_entries = mat_C_placeholders.get_entries().copy()
final_c_group = VGroup()

# --- Calculate C[0,0] ---
row_A1 = mat_A.get_rows()[0]
col_B1 = mat_B.get_columns()[0]
highlight_A1 = SurroundingRectangle(row_A1, color=YELLOW)
highlight_B1 = SurroundingRectangle(col_B1, color=BLUE)

calc1_text = MathTex("1 \\times 5 + 2 \\times 7 = 19").next_to(expression, DOWN, buff=0.7)
result1 = MathTex("19").move_to(c_entries[0].get_center())

self.play(Create(highlight_A1), Create(highlight_B1))
self.play(Write(calc1_text))
self.wait(1)
self.play(
    ReplacementTransform(c_entries[0], result1),
    FadeOut(highlight_A1),
    FadeOut(highlight_B1)
)
final_c_group.add(result1)
self.play(FadeOut(calc1_text))
self.wait(0.5)

# --- Calculate C[0,1] ---
col_B2 = mat_B.get_columns()[1]
highlight_A2 = SurroundingRectangle(row_A1, color=YELLOW)
highlight_B2 = SurroundingRectangle(col_B2, color=BLUE)

calc2_text = MathTex("1 \\times 6 + 2 \\times 8 = 22").next_to(expression, DOWN, buff=0.7)
result2 = MathTex("22").move_to(c_entries[1].get_center())

self.play(Create(highlight_A2), Create(highlight_B2))
self.play(Write(calc2_text))
self.wait(1)
self.play(
    ReplacementTransform(c_entries[1], result2),
    FadeOut(highlight_A2),
    FadeOut(highlight_B2)
)
final_c_group.add(result2)
self.play(FadeOut(calc2_text))
self.wait(0.5)

# --- Calculate C[1,0] ---
row_A2 = mat_A.get_rows()[1]
highlight_A3 = SurroundingRectangle(row_A2, color=YELLOW)
highlight_B3 = SurroundingRectangle(col_B1, color=BLUE)

calc3_text = MathTex("3 \\times 5 + 4 \\times 7 = 43").next_to(expression, DOWN, buff=0.7)
result3 = MathTex("43").move_to(c_entries[2].get_center())

self.play(Create(highlight_A3), Create(highlight_B3))
self.play(Write(calc3_text))
self.wait(1)
self.play(
    ReplacementTransform(c_entries[2], result3),
    FadeOut(highlight_A3),
    FadeOut(highlight_B3)
)
final_c_group.add(result3)
self.play(FadeOut(calc3_text))
self.wait(0.5)

# --- Calculate C[1,1] ---
highlight_A4 = SurroundingRectangle(row_A2, color=YELLOW)
highlight_B4 = SurroundingRectangle(col_B2, color=BLUE)

calc4_text = MathTex("3 \\times 6 + 4 \\times 8 = 50").next_to(expression, DOWN, buff=0.7)
result4 = MathTex("50").move_to(c_entries[3].get_center())

self.play(Create(highlight_A4), Create(highlight_B4))
self.play(Write(calc4_text))
self.wait(1)
self.play(
    ReplacementTransform(c_entries[3], result4),
    FadeOut(highlight_A4),
    FadeOut(highlight_B4)
)
final_c_group.add(result4)
self.play(FadeOut(calc4_text))
self.wait(1)

# --- Final Result Emphasis ---
final_matrix_visual = VGroup(mat_C_placeholders.get_brackets(), final_c_group)
final_box = SurroundingRectangle(final_matrix_visual, color=GREEN, buff=0.2)
self.play(Create(final_box))
self.wait(2)
self.play(FadeOut(final_box))
self.wait(1)