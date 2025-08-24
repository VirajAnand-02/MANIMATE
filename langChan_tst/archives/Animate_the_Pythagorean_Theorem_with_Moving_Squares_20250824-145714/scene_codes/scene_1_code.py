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

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # Create the title text and place it in the title region
        title_text = self.create_textbox("Animate the Pythagorean Theorem", self.title_region.width * 0.9, self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())

        # --- Title Card Animation ---
        self.play(Write(title_text), run_time=3)
        self.wait(5) # Wait for the initial part of the narration

        # Define triangle dimensions for a 3-4-5 right triangle
        a_val = 3
        b_val = 4

        # Define vertices for a right triangle with the right angle at (0,0)
        v1 = ORIGIN
        v2 = a_val * RIGHT
        v3 = b_val * UP

        # Create the lines for the legs and hypotenuse
        leg_a_mobj = Line(v1, v2, color=BLUE, stroke_width=5)
        leg_b_mobj = Line(v1, v3, color=GREEN, stroke_width=5)
        hypotenuse_c_mobj = Line(v2, v3, color=RED, stroke_width=5)

        # Create the right angle indicator
        right_angle_square = Square(side_length=0.3, color=WHITE, fill_opacity=0.5, stroke_width=2)
        right_angle_square.move_to(v1 + 0.15 * RIGHT + 0.15 * UP)

        # Create the triangle fill (background)
        triangle_fill = Polygon(v1, v2, v3, color=WHITE, fill_opacity=0.2, stroke_width=0)

        # Group the visual elements of the triangle for scaling and positioning
        # Labels are not included yet as they will be positioned relative to scaled lines
        triangle_visuals = VGroup(triangle_fill, leg_a_mobj, leg_b_mobj, hypotenuse_c_mobj, right_angle_square)

        # Scale the triangle to fit within the main_region with some padding
        current_width = a_val
        current_height = b_val

        max_region_width = self.main_region.width * 0.8
        max_region_height = self.main_region.height * 0.8

        scale_factor_w = max_region_width / current_width
        scale_factor_h = max_region_height / current_height
        scale_factor = min(scale_factor_w, scale_factor_h)

        triangle_visuals.scale(scale_factor)
        triangle_visuals.move_to(self.main_region.get_center())

        # Extract the scaled mobjects for individual animation and label positioning
        scaled_triangle_fill = triangle_visuals[0]
        scaled_leg_a = triangle_visuals[1]
        scaled_leg_b = triangle_visuals[2]
        scaled_hypotenuse_c = triangle_visuals[3]
        scaled_right_angle_square = triangle_visuals[4]

        # Create the text labels for sides 'a', 'b', 'c'
        label_a_text = MathTex("a", font_size=48, color=BLUE).next_to(scaled_leg_a, DOWN, buff=0.2)
        label_b_text = MathTex("b", font_size=48, color=GREEN).next_to(scaled_leg_b, LEFT, buff=0.2)
        label_c_text = MathTex("c", font_size=48, color=RED).next_to(scaled_hypotenuse_c, UP + RIGHT, buff=0.2).shift(0.1 * LEFT)

        # --- Triangle and Labels Animation ---
        self.play(Create(scaled_triangle_fill), run_time=3) # Animate the triangle fill
        self.play(
        Create(scaled_leg_a),
        Create(scaled_leg_b),
        Create(scaled_hypotenuse_c),
        Create(scaled_right_angle_square),
        run_time=6 # Duration for creating the lines and right angle
        )
        self.wait(4) # Wait for narration about the theorem's description

        self.play(Write(label_a_text), run_time=2)
        self.wait(1)
        self.play(Write(label_b_text), run_time=2)
        self.wait(1)
        self.play(Write(label_c_text), run_time=2)
        self.wait(5) # Wait for the concluding part of the narration

# Set narration and duration
Scene1.narration_text = '''Hello geometry enthusiasts! Today, we\'re going to bring one of the most famous mathematical theorems to life: the Pythagorean Theorem. You might know it as a² + b² = c². This powerful equation describes a fundamental relationship in geometry, specifically for right-angled triangles. It tells us that in any right triangle, the square of the length of the hypotenuse, \'c\', is equal to the sum of the squares of the lengths of the other two sides, \'a\' and \'b\'. Let\'s dive in and see this magic unfold visually!'''
Scene1.audio_duration = 5.0
