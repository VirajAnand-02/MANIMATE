```python
from manim import *
import numpy as np

class Scene3(Scene):
    def construct(self):
        # --- Setup Argand Plane ---
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            x_length=14,
            y_length=8,
            axis_config={"color": GRAY},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.5}
        ).add_coordinates()
        self.play(Create(plane, run_time=1.5))
        self.wait(0.5)

        # --- Define Complex Numbers ---
        # z1: magnitude 2, angle 0 (purely real for clear scaling visualization)
        z1_val = complex(2, 0)
        # z2: magnitude 3, angle PI/4
        z2_val = complex(3 * np.cos(PI/4), 3 * np.sin(PI/4))
        # z1 * z2: magnitude |z1|*|z2|=6, angle 0+PI/4=PI/4
        z_product_val = z1_val * z2_val

        # Helper to convert complex number to Manim vector coordinates
        def c_to_v(z):
            return plane.c2p(z.real, z.imag)

        # --- Mobjects for z1 ---
        z1_arrow = Arrow(ORIGIN, c_to_v(z1_val), buff=0, color=BLUE, tip_length=0.2)
        z1_label = MathTex("z_1", color=BLUE).next_to(z1_arrow, UP + RIGHT, buff=0.1)
        z1_magnitude_text = MathTex("|z_1| = 2", color=BLUE).to_corner(UL).shift(DOWN * 0.5)

        # --- Mobjects for z2 ---
        z2_arrow = Arrow(ORIGIN, c_to_v(z2_val), buff=0, color=GREEN, tip_length=0.2)
        z2_label = MathTex("z_2", color=GREEN).next_to(z2_arrow, UP + LEFT, buff=0.1)
        z2_magnitude_text = MathTex("|z_2| = 3", color=GREEN).next_to(z1_magnitude_text, DOWN, aligned_edge=LEFT)

        # --- Display z1 and its magnitude ---
        self.play(
            GrowArrow(z1_arrow),
            Write(z1_label),
            run_time=1.5
        )
        self.play(Write(z1_magnitude_text))
        self.wait(0.5)

        # --- Display z2 and its magnitude ---
        self.play(
            GrowArrow(z2_arrow),
            Write(z2_label),
            run_time=1.5
        )
        self.play(Write(z2_magnitude_text))
        self.wait(1)

        # --- Introduce the scaling principle ---
        scaling_principle = MathTex(
            "|z_1 \\cdot z_2|", "=", "|z_1|", "\\cdot", "|z_2|",
            font_size=50
        ).next_to(plane, DOWN, buff=0.8)
        self.play(Write(scaling_principle))
        self.wait(1)

        # --- Substitute values and show resultant magnitude ---
        product_magnitudes = MathTex(
            "|z_1 \\cdot z_2|", "=", "2", "\\cdot", "3", "=", "6",
            font_size=50
        ).move_to(scaling_principle)

        self.play(
            TransformMatchingTex(
                scaling_principle,
                product_magnitudes,
                transform_mismatched_parts=True
            )
        )
        self.wait(1.5)

        # --- Visual demonstration of scaling ---
        # Fade out z2 and its label to focus on z1 scaling
        self.play(FadeOut(z2_arrow, z2_label, z2_magnitude_text))
        self.wait(0.5)

        # Create a temporary vector that is z1 scaled by |z2| (magnitude 3)
        # This vector has magnitude 6 and the same angle as z1 (0 degrees)
        temp_scaled_z1_val = z1_val * abs(z2_val) # complex(6, 0)
        temp_scaled_z1_arrow = Arrow(ORIGIN, c_to_v(temp_scaled_z1_val), buff=0, color=YELLOW, tip_length=0.2)
        temp_scaled_z1_label = MathTex("|z_1| \\cdot |z_2|", color=YELLOW).next_to(temp_scaled_z1_arrow, UP, buff=0.1)

        # Animate z1_arrow scaling to temp_scaled_z1_arrow
        # This visually shows z1's length being stretched by the factor |z2|
        self.play(
            Transform(z1_arrow, temp_scaled_z1_arrow),
            FadeOut(z1_label), # z1 label is no longer accurate for the scaled vector
            Write(temp_scaled_z1_label),
            run_time=2
        )
        self.wait(1)

        # --- Show the final product vector ---
        z_product_arrow = Arrow(ORIGIN, c_to_v(z_product_val), buff=0, color=RED, tip_length=0.2)
        z_product_label = MathTex("z_1 \\cdot z_2", color=RED).next_to(z_product_arrow, UP + RIGHT, buff=0.1)
        # Position the product magnitude text where z2's magnitude text was
        z_product_magnitude_text = MathTex("|z_1 \\cdot z_2| = 6", color=RED).move_to(z1_magnitude_text.get_center() + DOWN * 1.0)


        # Transform the scaled z1 (yellow) into the actual product (red)
        # This implicitly shows the rotation, but the magnitude remains 6.
        self.play(
            Transform(temp_scaled_z1_arrow, z_product_arrow),
            FadeOut(temp_scaled_z1_label),
            Write(z_product_label),
            Write(z_product_magnitude_text),
            run_time=2
        )
        self.wait(1)

        # Clean up
        self.play(
            FadeOut(plane, z1_magnitude_text, z_product_magnitude_text, product_magnitudes, z_product_label, z_product_arrow),
            run_time=2
        )
        self.wait(0.5)
```