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

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text using self.create_textbox and place it in the title/text region.
        title_text = self.create_textbox("The Pythagorean Theorem: Conclusion", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.add(title_text)

        # Define triangle vertices (using 3-4-5 right triangle for clear visualization)
        p_origin = ORIGIN
        p_right = 4 * RIGHT
        p_top = 3 * UP

        # Create the right-angled triangle
        triangle = Polygon(p_origin, p_right, p_top, color=WHITE, fill_opacity=0)

        # Create the original squares (initially as outlines)
        # Square on side 'a' (length 3, vertical side)
        square_a_orig = Square(side_length=3, color=RED, fill_opacity=0)
        square_a_orig.align_to(p_origin, RIGHT).align_to(p_top, DOWN) # Position to the left of AC

        # Square on side 'b' (length 4, horizontal side)
        square_b_orig = Square(side_length=4, color=YELLOW, fill_opacity=0)
        square_b_orig.align_to(p_origin, UP).align_to(p_right, LEFT) # Position below AB

        # Square on side 'c' (hypotenuse, length 5)
        side_c_line = Line(p_right, p_top)
        square_c_orig = Square(side_length=side_c_line.get_length(), color=BLUE, fill_opacity=0)
        # Rotate and position square_c_orig to be on the outside of the hypotenuse
        square_c_orig.rotate(side_c_line.get_angle() - PI/2, about_point=side_c_line.get_center())
        square_c_orig.shift(side_c_line.get_unit_vector() * side_c_line.get_length() / 2)

        # Create the "filled" state of square_c for the initial view
        # This represents the pieces of a^2 and b^2 filling c^2 from the previous scene
        square_c_filled_green = square_c_orig.copy().set_fill(GREEN, opacity=1).set_stroke(width=0) # No stroke for filled state

        # Group all diagram elements for scaling and positioning
        diagram_group = VGroup(triangle, square_a_orig, square_b_orig, square_c_orig, square_c_filled_green)

        # Scale and position the diagram to fit within self.main_region
        diagram_group.set(width=self.main_region.width * 0.8)
        diagram_group.move_to(self.main_region.get_center())

        # Set stroke width for outlines after scaling the group
        square_a_orig.set_stroke(width=2)
        square_b_orig.set_stroke(width=2)
        square_c_orig.set_stroke(width=2)
        triangle.set_stroke(width=2)

        # 2. Main animation
        # Initial state: triangle and the green filled square on 'c'
        self.add(triangle, square_c_filled_green)
        self.wait(4) # Hold for a moment as per description and narration

        # Dissolve the pieces (represented by fading out the filled green square)
        self.play(FadeOut(square_c_filled_green), run_time=2)

        # Reappear the original three solid squares (as outlines in this context)
        self.play(
        FadeIn(square_a_orig),
        FadeIn(square_b_orig),
        FadeIn(square_c_orig),
        run_time=3
        )
        self.wait(3)

        # Animate the equation 'a² + b² = c²'
        equation = MathTex("a^2 + b^2 = c^2", font_size=72, color=WHITE)
        # Position the equation below the diagram
        equation.next_to(diagram_group, DOWN, buff=1.0)
        equation.set(width=self.main_region.width * 0.7) # Ensure it fits horizontally
        if equation.height > self.main_region.height * 0.2: # Don't let it take too much vertical space
        equation.set(height=self.main_region.height * 0.2)

        self.play(Write(equation), run_time=2)
        self.wait(4)

        # Final title card and message
        # Fade out the current diagram and equation
        self.play(
        FadeOut(VGroup(triangle, square_a_orig, square_b_orig, square_c_orig, equation)),
        FadeOut(title_text), # Also fade out the initial title
        run_time=2
        )

        final_title_text = Text("The Pythagorean Theorem", font_size=72, color=BLUE_C)
        final_equation_text = MathTex("a^2 + b^2 = c^2", font_size=96, color=YELLOW_C)
        thanks_message = Text("Thanks for watching!", font_size=48, color=WHITE)

        final_card_group = VGroup(final_title_text, final_equation_text, thanks_message).arrange(DOWN, buff=0.8)
        final_card_group.set(width=self.main_region.width * 0.9)
        final_card_group.move_to(self.main_region.get_center())

        self.play(FadeIn(final_card_group[0]), FadeIn(final_card_group[1]), run_time=2)
        self.play(FadeIn(final_card_group[2]), run_time=1)
        self.wait(6)

# Set narration and duration
Scene4.narration_text = '''And there you have it! A dynamic, animated proof of the Pythagorean Theorem. We\'ve seen how the areas represented by a² and b² can be physically transformed to perfectly constitute the area of c². This isn\'t just a clever trick; it\'s a profound mathematical truth that has countless applications, from architecture and engineering to navigation and computer graphics. Remember, a² + b² = c² isn\'t just an equation to memorize; it\'s a visual relationship of areas within a right-angled triangle. Keep exploring the beauty of mathematics!'''
Scene4.audio_duration = 5.0
