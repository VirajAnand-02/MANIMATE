# Scene 2 - Generated via Batch Manim LLM
# Thinking used: False
# Generated at: 2025-08-23 22:32:51

text = "Before we multiply, we must check if the matrices are compatible. For matrix A multiplied by matrix B, the number of columns in A must precisely equal the number of rows in B. The resulting product matrix will then have the number of rows from A and the number of columns from B."
textbox = self.create_textbox(text, width=self.left_region.width, height=self.left_region.height)
self.play(Write(textbox))
self.wait(1)

# Define Matrix A
matrix_a_rect = Rectangle(width=2.0, height=3.0, color=BLUE)
matrix_a_label = MathTex("A").move_to(matrix_a_rect.get_center())
dim_a_label = MathTex("m", r"\times", "n").next_to(matrix_a_rect, DOWN)
dim_a_label[0].set_color(BLUE)
dim_a_label[2].set_color(RED)
matrix_a = VGroup(matrix_a_rect, matrix_a_label, dim_a_label)

# Define Matrix B
matrix_b_rect = Rectangle(width=3.0, height=2.0, color=YELLOW)
matrix_b_label = MathTex("B").move_to(matrix_b_rect.get_center())
dim_b_label = MathTex("p", r"\times", "q").next_to(matrix_b_rect, DOWN)
dim_b_label[0].set_color(RED)
dim_b_label[2].set_color(YELLOW)
matrix_b = VGroup(matrix_b_rect, matrix_b_label, dim_b_label)

# Arrange A and B with a multiplication sign
times_sign = MathTex(r"\times").scale(2)
initial_group = VGroup(matrix_a, times_sign, matrix_b).arrange(RIGHT, buff=0.5)
initial_group.move_to(self.right_region.get_center()).shift(LEFT*2)

self.play(
    Create(matrix_a_rect),
    Write(matrix_a_label),
    Write(dim_a_label),
    Write(times_sign),
    Create(matrix_b_rect),
    Write(matrix_b_label),
    Write(dim_b_label)
)
self.wait(1)

# Highlight 'n' and 'p'
n_part = dim_a_label[2]
p_part = dim_b_label[0]
n_box = SurroundingRectangle(n_part, color=RED, buff=0.1)
p_box = SurroundingRectangle(p_part, color=RED, buff=0.1)
self.play(Create(n_box), Create(p_box))
self.wait(0.5)

# Show equality check
equals_sign = MathTex("=", color=RED).move_to((n_box.get_center() + p_box.get_center()) / 2)
check_mark = Checkmark(color=GREEN).next_to(equals_sign, RIGHT, buff=0.3)
self.play(Write(equals_sign))
self.play(Write(check_mark))
self.wait(2)

self.play(FadeOut(n_box, p_box, equals_sign, check_mark))
self.wait(0.5)

# Define and reveal result Matrix C
matrix_c_rect = Rectangle(width=3.0, height=3.0, color=GREEN)
matrix_c_label = MathTex("C").move_to(matrix_c_rect.get_center())
dim_c_label = MathTex("m", r"\times", "q").next_to(matrix_c_rect, DOWN)
dim_c_label[0].set_color(BLUE)
dim_c_label[2].set_color(YELLOW)
matrix_c = VGroup(matrix_c_rect, matrix_c_label, dim_c_label)

result_equals_sign = MathTex("=").scale(1.5)
final_group = VGroup(initial_group, result_equals_sign, matrix_c).arrange(RIGHT, buff=0.5).move_to(self.right_region.get_center())

# Animate the result
self.play(
    initial_group.animate.move_to(final_group[0].get_center()),
    Write(result_equals_sign.move_to(final_group[1].get_center()))
)
self.play(
    Create(matrix_c_rect),
    Write(matrix_c_label)
)
self.wait(1)

# Animate the transfer of dimensions
m_part_origin = dim_a_label[0]
q_part_origin = dim_b_label[2]
m_part_dest = dim_c_label[0]
q_part_dest = dim_c_label[2]
times_dest = dim_c_label[1]

m_indicator = SurroundingRectangle(m_part_origin, color=BLUE, buff=0.1)
q_indicator = SurroundingRectangle(q_part_origin, color=YELLOW, buff=0.1)

self.play(Create(m_indicator))
self.play(ReplacementTransform(m_indicator, m_part_dest))
self.wait(0.5)

self.play(Create(q_indicator))
self.play(ReplacementTransform(q_indicator, q_part_dest))
self.wait(0.5)

self.play(Write(times_dest))
self.wait(3)