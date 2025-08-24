import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
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
        from manim import *
        import numpy as np

        # The class definition and construct_scene method signature are provided by the template.
        # I only need to provide the body of construct_scene.

        # Assume self.title_region, self.main_region, self.create_textbox are available.

        # --- Start of construct_scene body ---

        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox("Best Practices for Test Reliability", width=self.title_region.width, height=self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text), run_time=1.5)
        self.wait(2)

        # 2. Create the main animation: Icons appear sequentially

        # 2.1. Single Responsibility Principle (S.R.P.)
        srp_text = Text("S.R.P.", font_size=48, color=BLUE)

        # 2.2. Independent Tests (Two distinct shapes)
        test1 = Circle(radius=0.5, color=GREEN, fill_opacity=0.8)
        test2 = Square(side_length=1, color=ORANGE, fill_opacity=0.8)
        independent_tests_group = VGroup(test1, test2).arrange(RIGHT, buff=0.5).scale(0.8)

        # 2.3. Code Review (Magnifying glass over code)
        code_block = Rectangle(width=2, height=1.5, color=GRAY, fill_opacity=0.2, stroke_color=LIGHT_GRAY)
        code_lines = VGroup(*[
        Line(code_block.get_corner(UL) + RIGHT * 0.2 + DOWN * i * 0.3,
        code_block.get_corner(UR) - RIGHT * 0.2 + DOWN * i * 0.3,
        color=LIGHT_GRAY, stroke_width=2)
        for i in range(1, 5)
        ])
        lens = Circle(radius=0.4, color=WHITE, fill_opacity=0.2, stroke_width=3)
        handle = Line(ORIGIN, DOWN * 0.8, stroke_width=4).shift(lens.get_bottom() + DOWN * 0.1)
        handle.rotate(PI/4, about_point=handle.get_start())
        magnifying_glass = VGroup(lens, handle).scale(0.7)
        magnifying_glass.next_to(code_block, UR, buff=0.1).shift(LEFT*0.2 + DOWN*0.2)
        code_review_group = VGroup(code_block, code_lines, magnifying_glass).scale(0.8)

        # 2.4. Regular Maintenance (Gear icon for maintenance)
        gear_outer = RegularPolygon(n=12, radius=0.8, color=YELLOW, fill_opacity=1, stroke_color=YELLOW)
        gear_inner = Circle(radius=0.3, color=BLACK, fill_opacity=1, stroke_color=BLACK)
        maintenance_icon = VGroup(gear_outer, gear_inner).scale(0.8)

        # Group all icons temporarily for initial arrangement and scaling
        initial_icons_for_arrangement = VGroup(srp_text, independent_tests_group, code_review_group, maintenance_icon)
        initial_icons_for_arrangement.scale_to_fit_width(self.main_region.width * 0.8)
        initial_icons_for_arrangement.scale_to_fit_height(self.main_region.height * 0.8)
        initial_icons_for_arrangement.arrange_in_grid(rows=2, cols=2, buff=1.0)
        initial_icons_for_arrangement.move_to(self.main_region.get_center())

        # Move individual icons to their calculated positions
        srp_text.move_to(initial_icons_for_arrangement[0].get_center())
        independent_tests_group.move_to(initial_icons_for_arrangement[1].get_center())
        code_review_group.move_to(initial_icons_for_arrangement[2].get_center())
        maintenance_icon.move_to(initial_icons_for_arrangement[3].get_center())

        # Play animations for icons appearing sequentially
        self.play(FadeIn(srp_text, shift=UP), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(independent_tests_group, shift=UP), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(code_review_group, shift=UP), run_time=1.5)
        self.play(FadeIn(maintenance_icon, shift=UP), run_time=1.5) # These two appear together
        self.wait(1)

        # 3. Icons then converge into a large 'Shield of Quality' icon, with a 'Trustworthy Tests' message.

        # Create a VGroup of the *actual mobjects currently on screen* for the transformation
        icons_on_screen = VGroup(srp_text, independent_tests_group, code_review_group, maintenance_icon)

        # Construct the Shield of Quality icon
        shield_points = [
        UP * 1.5,
        RIGHT * 1,
        RIGHT * 1 + DOWN * 1.5,
        ORIGIN + DOWN * 2, # Pointed bottom
        LEFT * 1 + DOWN * 1.5,
        LEFT * 1,
        UP * 1.5 # Close the polygon
        ]
        shield_of_quality = Polygon(*shield_points, color=GOLD, fill_opacity=0.8, stroke_width=5)
        shield_of_quality.scale_to_fit_width(self.main_region.width * 0.6)
        shield_of_quality.scale_to_fit_height(self.main_region.height * 0.6)
        shield_of_quality.move_to(self.main_region.get_center())

        # Create the 'Trustworthy Tests' message
        trustworthy_tests_text = Text("Trustworthy Tests", font_size=40, color=WHITE)
        trustworthy_tests_text.next_to(shield_of_quality, DOWN, buff=0.5)

        # Animate the convergence of the icons into the shield
        self.play(
        ReplacementTransform(icons_on_screen, shield_of_quality),
        run_time=2.5
        )
        self.play(Write(trustworthy_tests_text), run_time=1.5)
        self.wait(3)

        # --- End of construct_scene body ---

# Set narration and duration
Scene4.narration_text = '''To prevent future validation problems, adopt best practices from the start. Write tests that are clear, concise, and focused on a single responsibility. Ensure they are independent, meaning each test can run without affecting others. Regularly review and maintain your test suite, just like your production code. A well-validated and maintained test suite is your most reliable safeguard against regressions and a cornerstone of continuous delivery. Invest in your tests, and they\'ll invest in your product\'s quality.'''
Scene4.audio_duration = 5.0