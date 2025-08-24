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

class Scene2(SplitScreen):
    def construct_scene(self):
        from manim import *

        def construct_scene(self):
        # 1. Create the title text
        title_text = self.create_textbox("Understanding 'Squared'", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Define a base right-angled triangle with legs along the x and y axes.
        # This setup simplifies calculating the positions for the squares.
        # The actual coordinates will be adjusted when placed in the regions.
        P1_base = ORIGIN
        P2_base = RIGHT * 3  # Represents leg 'b'
        P3_base = UP * 4     # Represents leg 'a'

        # Create the triangle for the left region (static reference)
        left_triangle = Polygon(P1_base, P2_base, P3_base, color=WHITE, fill_opacity=0.5)
        left_triangle.set_height(self.left_region.height * 0.8)
        left_triangle.move_to(self.left_region.get_center())
        self.add(left_triangle)

        # Create the elements for the right region, starting with the triangle
        right_triangle = Polygon(P1_base, P2_base, P3_base, color=WHITE, fill_opacity=0.5)

        # Define lines representing the legs of the base triangle for positioning squares
        leg_a_line = Line(P1_base, P3_base) # Vertical leg (length 4)
        leg_b_line = Line(P1_base, P2_base) # Horizontal leg (length 3)

        # Create the square for side 'a'
        square_a = Square(side_length=leg_a_line.get_length(), color=BLUE, fill_opacity=0.7)
        # Position it outwards from leg_a (to the left of the vertical leg)
        square_a.move_to(leg_a_line.get_center() + LEFT * (leg_a_line.get_length() / 2))

        # Create the text for 'a²'
        text_a_squared = MathTex("a^2", color=WHITE).scale(0.8)
        text_a_squared.move_to(square_a.get_center())
        text_a_squared.set_opacity(0) # Initially invisible

        # Create the square for side 'b'
        square_b = Square(side_length=leg_b_line.get_length(), color=YELLOW, fill_opacity=0.7)
        # Position it outwards from leg_b (below the horizontal leg)
        square_b.move_to(leg_b_line.get_center() + DOWN * (leg_b_line.get_length() / 2))

        # Create the text for 'b²'
        text_b_squared = MathTex("b^2", color=WHITE).scale(0.8)
        text_b_squared.move_to(square_b.get_center())
        text_b_squared.set_opacity(0) # Initially invisible

        # Group all right-side elements (triangle, squares, and text)
        # This allows them to be scaled and positioned together relative to self.right_region
        right_side_elements = VGroup(right_triangle, square_a, text_a_squared, square_b, text_b_squared)
        right_side_elements.set_height(self.right_region.height * 0.8) # Scale to fit the region
        right_side_elements.move_to(self.right_region.get_center()) # Move to the center of the right region

        # Add the right triangle to the scene (it's part of the group, so its position is already set)
        self.add(right_triangle)

        # Animate the squares and their labels
        # Narration: "Imagine a square built directly outwards from side 'a' of our triangle."
        self.play(Create(square_a), run_time=2)
        self.wait(1)

        # Narration: "Its area is a times a, or a²."
        self.play(FadeIn(text_a_squared), run_time=1)
        self.wait(2)

        # Narration: "Similarly, for side 'b', we can construct another square with an area of b²."
        self.play(Create(square_b), run_time=2)
        self.wait(1)

        # Narration: "These two squares represent the 'a²' and 'b²' parts of our equation."
        self.play(FadeIn(text_b_squared), run_time=1)
        self.wait(3) # Wait at the end of the scene

# Set narration and duration
Scene2.narration_text = '''To truly understand a² + b² = c², we need to think about what \'squared\' means. When we say \'a squared\', we\'re talking about the area of a square whose side length is \'a\'. Imagine a square built directly outwards from side \'a\' of our triangle. Its area is a times a, or a². Similarly, for side \'b\', we can construct another square with an area of b². These two squares represent the \'a²\' and \'b²\' parts of our equation. Notice how they perfectly extend from the legs of our right triangle.'''
Scene2.audio_duration = 5.0
