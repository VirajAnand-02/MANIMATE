import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title = self.create_textbox(
        "Complex Number Multiplication: Geometric Interpretation",
        self.title_region.width,
        self.title_region.height
        ).move_to(self.title_region.get_center())
        self.play(Write(title))
        self.wait(0.5)

        # Setup NumberPlane
        plane = NumberPlane(
        x_range=[-4, 4, 1],
        y_range=[-4, 4, 1],
        x_length=self.main_region.width * 0.9,
        y_length=self.main_region.height * 0.9,
        background_line_style={"stroke_opacity": 0.5},
        axis_config={"color": GRAY}
        ).move_to(self.main_region.get_center())
        self.play(Create(plane), run_time=1.5)

        # Define complex numbers
        z1_val = complex(2, 1)
        z2_val = complex(1, 2)
        z_product_val = z1_val * z2_val  # Result: 5j

        # Vectors
        # Using c2p (complex to point) for positioning on the plane
        z1_vec = Arrow(ORIGIN, plane.c2p(z1_val), buff=0, color=BLUE, tip_length=0.2, stroke_width=6)
        z2_vec = Arrow(ORIGIN, plane.c2p(z2_val), buff=0, color=GREEN, tip_length=0.2, stroke_width=6)
        # The final product vector, used as a target for transformation
        z_product_vec_target = Arrow(ORIGIN, plane.c2p(z_product_val), buff=0, color=RED, tip_length=0.2, stroke_width=6)

        # Labels
        z1_label = MathTex("z_1").next_to(z1_vec, RIGHT, buff=0.1).shift(0.2 * UP).set_color(BLUE)
        z2_label = MathTex("z_2").next_to(z2_vec, UP, buff=0.1).shift(0.2 * RIGHT).set_color(GREEN)

        self.play(GrowArrow(z1_vec), Write(z1_label))
        self.play(GrowArrow(z2_vec), Write(z2_label))
        self.wait(1.5)

        # Step 1: Scale z1 by |z2|
        magnitude_z2 = abs(z2_val)
        z1_scaled_val = z1_val * magnitude_z2
        z1_scaled_vec_target = Arrow(ORIGIN, plane.c2p(z1_scaled_val), buff=0, color=BLUE, tip_length=0.2, stroke_width=6)

        scaling_text = Text(
        f"1. Scale z1 by |z2| = {magnitude_z2:.2f}",
        font_size=36,
        color=YELLOW
        ).move_to(self.main_region.get_center() + UP * self.main_region.height * 0.4)
        self.play(Write(scaling_text))

        # Animate z1_vec transforming to its scaled version
        self.play(Transform(z1_vec, z1_scaled_vec_target), FadeOut(z1_label), run_time=2)
        z1_scaled_label = MathTex("z_1 \\cdot |z_2|").next_to(z1_vec, RIGHT, buff=0.1).shift(0.2 * UP).set_color(BLUE)
        self.play(Write(z1_scaled_label))
        self.wait(1.5)
        self.play(FadeOut(scaling_text))

        # Step 2: Rotate scaled z1 by arg(z2)
        angle_z2 = np.angle(z2_val)  # in radians

        rotation_text = Text(
        f"2. Rotate scaled z1 by arg(z2) = {np.degrees(angle_z2):.1f}°",
        font_size=36,
        color=YELLOW
        ).move_to(self.main_region.get_center() + UP * self.main_region.height * 0.4)
        self.play(Write(rotation_text))

        # Create an arc to show the rotation
        current_angle_z1_scaled = np.angle(z1_scaled_val)
        arc_radius = np.linalg.norm(plane.c2p(z1_scaled_val)) * 0.3  # Smaller radius for the arc
        rotation_arc = Arc(
        start_angle=current_angle_z1_scaled,
        angle=angle_z2,
        radius=arc_radius,
        arc_center=ORIGIN,
        color=YELLOW,
        stroke_width=4
        )
        # Position arc label slightly outside the arc at its midpoint
        arc_label = MathTex(r"\arg(z_2)").set_color(YELLOW)
        arc_label.move_to(rotation_arc.point_from_proportion(0.5))
        arc_label.shift((rotation_arc.point_from_proportion(0.5) - rotation_arc.get_arc_center()).normalize() * 0.5)

        self.play(Create(rotation_arc), Write(arc_label))
        self.play(z1_vec.animate.rotate(angle_z2, about_point=ORIGIN), FadeOut(z1_scaled_label), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(rotation_text), FadeOut(rotation_arc), FadeOut(arc_label))

        # Step 3: Final product z1 * z2
        product_text = Text(
        "3. The final vector is z1 * z2",
        font_size=36,
        color=YELLOW
        ).move_to(self.main_region.get_center() + UP * self.main_region.height * 0.4)
        self.play(Write(product_text))

        # The z1_vec has been rotated. Now transform it to the final product vector.
        self.play(Transform(z1_vec, z_product_vec_target), run_time=1.5)
        z_product_label = MathTex("z_1 \\cdot z_2").next_to(z1_vec, RIGHT, buff=0.1).set_color(RED)
        self.play(Write(z_product_label))
        self.wait(2.5)
        self.play(FadeOut(product_text))

        # Conclude with summary rules
        self.play(
        FadeOut(z1_vec),
        FadeOut(z2_vec),
        FadeOut(z_product_label),
        FadeOut(z2_label),
        FadeOut(plane),
        run_time=1.5
        )

        rule1 = Tex("Multiply Magnitudes", font_size=60, color=BLUE)
        rule2 = Tex("Add Arguments", font_size=60, color=GREEN)
        rules_group = VGroup(rule1, rule2).arrange(RIGHT, buff=1.5).move_to(self.main_region.get_center())

        self.play(Write(rules_group))
        self.wait(3.5)

        # Final cleanup
        self.play(FadeOut(rules_group), FadeOut(title))

# Set narration and duration
Scene5.narration_text = '''So, to multiply \'z1\' by \'z2\', you first scale \'z1\' by the magnitude of \'z2\', and then rotate that scaled vector by the argument of \'z2\'. The final vector is your product, \'z1 * z2\'. This elegant geometric interpretation reveals why complex numbers are so fundamental in fields like electrical engineering, physics, and computer graphics, especially for operations involving rotations and transformations. Remember: multiply magnitudes, add arguments!'''
Scene5.audio_duration = 5.0
