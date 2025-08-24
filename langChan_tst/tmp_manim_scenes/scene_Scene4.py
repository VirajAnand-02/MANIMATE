
from manim import *
import numpy as np

class Scene4(Scene):
    def construct(self):
        # --- Configuration: Complex Plane ---
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_numbers": True},
            background_line_style={"stroke_opacity": 0.5}
        ).add_coordinates()
        self.add(plane)

        # --- Complex Numbers ---
        # z1 at 30 degrees, magnitude 2
        z1_val = 2 * np.exp(1j * 30 * DEGREES)
        # z2 at 60 degrees, magnitude 1.5
        z2_val = 1.5 * np.exp(1j * 60 * DEGREES)
        # Product z1 * z2 will be at 90 degrees, magnitude 3
        z_product_val = z1_val * z2_val

        # --- Mobjects: Vectors ---
        z1_vec = Arrow(ORIGIN, plane.c2p(z1_val), buff=0, color=BLUE, tip_length=0.2)
        z2_vec = Arrow(ORIGIN, plane.c2p(z2_val), buff=0, color=RED, tip_length=0.2)
        z_product_vec = Arrow(ORIGIN, plane.c2p(z_product_val), buff=0, color=GREEN, tip_length=0.2)

        # --- Mobjects: Labels for Vectors ---
        z1_label = MathTex("z_1").next_to(z1_vec, UP + RIGHT, buff=0.1).set_color(BLUE)
        z2_label = MathTex("z_2").next_to(z2_vec, UP + LEFT, buff=0.1).set_color(RED)
        z_product_label = MathTex("z_1 z_2").next_to(z_product_vec, UP + RIGHT, buff=0.1).set_color(GREEN)

        # --- Mobjects: Angles ---
        # Helper line for angle reference (positive x-axis)
        x_axis_line = Line(ORIGIN, plane.c2p(plane.x_range[1], 0))

        arg_z1_arc = Angle(x_axis_line, z1_vec, radius=0.5, color=YELLOW)
        arg_z2_arc = Angle(x_axis_line, z2_vec, radius=0.7, color=ORANGE)
        arg_product_arc = Angle(x_axis_line, z_product_vec, radius=0.9, color=GREEN)

        # --- Mobjects: Labels for Angles ---
        arg_z1_label = arg_z1_arc.get_label(MathTex("30^\\circ")).set_color(YELLOW)
        arg_z2_label = arg_z2_arc.get_label(MathTex("60^\\circ")).set_color(ORANGE)
        arg_product_label = arg_product_arc.get_label(MathTex("90^\\circ")).set_color(GREEN)

        # --- Introduction of z1 ---
        self.play(Create(z1_vec), Write(z1_label), run_time=1)
        self.play(Create(arg_z1_arc), Write(arg_z1_label), run_time=1)
        self.wait(0.5)

        # --- Introduction of z2 ---
        self.play(Create(z2_vec), Write(z2_label), run_time=1)
        self.play(Create(arg_z2_arc), Write(arg_z2_label), run_time=1)
        self.wait(0.5)

        # --- Text Explanation 1 ---
        text1_line1 = Text(
            "Next, let's explore the rotation. The argument, or angle, of the product 'z1 * z2'",
            font_size=28, disable_ligatures=True
        ).to_edge(UP)
        text1_line2 = Text(
            "is the sum of the individual arguments of 'z1' and 'z2'.",
            font_size=28, disable_ligatures=True
        ).next_to(text1_line1, DOWN)
        self.play(Write(text1_line1))
        self.play(Write(text1_line2))
        self.wait(2)
        self.play(FadeOut(text1_line1, text1_line2))

        # --- Formula ---
        formula = MathTex(r"\arg(z_1 z_2) = \arg(z_1) + \arg(z_2)", font_size=48).to_edge(UP)
        self.play(Write(formula))
        self.wait(1.5)
        self.play(FadeOut(formula))

        # --- Text Explanation 2 (Specific Angles) ---
        text2_line1 = Text(
            "If 'z1' makes an angle of 30 degrees and 'z2' makes an angle of 60 degrees,",
            font_size=28, disable_ligatures=True
        ).to_edge(UP)
        text2_line2 = Text(
            "their product 'z1 * z2' will make an angle of 90 degrees.",
            font_size=28, disable_ligatures=True
        ).next_to(text2_line1, DOWN)
        self.play(Write(text2_line1))
        self.play(Write(text2_line2))
        self.wait(2)
        self.play(FadeOut(text2_line1, text2_line2))

        # --- Animate Rotation ---
        # Dim z1 and its angle, keep z2 and its angle for reference
        self.play(
            z1_vec.animate.set_opacity(0.5),
            z1_label.animate.set_opacity(0.5),
            arg_z1_arc.animate.set_opacity(0.5),
            arg_z1_label.animate.set_opacity(0.5),
            run_time=0.7
        )

        # Create a copy of z1_vec and its angle to animate
        z1_vec_copy = Arrow(ORIGIN, plane.c2p(z1_val), buff=0, color=BLUE, tip_length=0.2)
        arg_z1_arc_copy = Angle(x_axis_line, z1_vec_copy, radius=0.5, color=YELLOW)
        arg_z1_label_copy = arg_z1_arc_copy.get_label(MathTex("30^\\circ")).set_color(YELLOW)
        self.add(z1_vec_copy, arg_z1_arc_copy, arg_z1_label_copy)

        # Text explanation for rotation
        text3_line1 = Text(
            "This means the vector 'z1' is effectively rotated by the angle of 'z2'",
            font_size=28, disable_ligatures=True
        ).to_edge(UP)
        text3_line2 = Text(
            "around the origin.",
            font_size=28, disable_ligatures=True
        ).next_to(text3_line1, DOWN)
        self.play(Write(text3_line1))
        self.play(Write(text3_line2))
        self.wait(1)

        # Animate z1_vec_copy rotating by arg(z2)
        # Simultaneously, animate arg_z1_arc_copy extending to arg_product_arc
        # Also, fade out z2_vec and its angle as z1 rotates by its angle
        self.play(
            Rotate(z1_vec_copy, angle=np.angle(z2_val), about_point=ORIGIN, rate_func=smooth),
            Transform(arg_z1_arc_copy, arg_product_arc),
            Transform(arg_z1_label_copy, arg_product_label),
            FadeOut(z2_vec, z2_label, arg_z2_arc, arg_z2_label),
            run_time=3
        )
        self.wait(0.5)
        self.play(FadeOut(text3_line1, text3_line2))

        # Final text
        text4 = Text(
            "It's like 'z2' tells 'z1' how much to turn!",
            font_size=28, disable_ligatures=True
        ).to_edge(UP)
        self.play(Write(text4))
        self.wait(1)

        # Show the final product vector
        self.play(
            ReplacementTransform(z1_vec_copy, z_product_vec),
            Write(z_product_label),
            run_time=1.5
        )
        self.wait(2)

        # --- Clean up ---
        self.play(FadeOut(*self.mobjects))
