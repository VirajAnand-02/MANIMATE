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

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text using the helper method and place it in the title region.
        title_text = self.create_textbox("Test Validation Fixes", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.add(title_text)

        # Define the 'Test Passed' icon (green square with a checkmark)
        passed_square = Square(side_length=1.5, color=GREEN, fill_opacity=0.8)
        check_mark = Check(color=WHITE).scale(0.8)
        passed_icon = VGroup(passed_square, check_mark)

        # Define the 'Test Failed' icon (red square with an X-mark)
        failed_square = Square(side_length=1.5, color=RED, fill_opacity=0.8)
        x_mark = XMark(color=WHITE).scale(0.8)
        failed_icon = VGroup(failed_square, x_mark)

        # Arrange initial icons side-by-side in the main region
        icon_group = VGroup(passed_icon, failed_icon).arrange(RIGHT, buff=1.5)
        # Position the group slightly above the center of the main region to make space for text below
        icon_group.move_to(self.main_region.get_center() + UP * 0.5)

        # 2. Create the main animation described in "anim"

        # Opens with a 'Test Passed' and 'Test Failed' icon.
        self.play(Create(passed_icon), Create(failed_icon))
        self.wait(6) # Corresponds to: "Welcome! In software development, tests are crucial for quality."

        # A 'Test Failed' icon then gets a large question mark over it
        question_mark = Tex("?", color=YELLOW).scale(2)
        question_mark.move_to(failed_icon.get_center()) # Position question mark over the failed icon
        self.play(FadeIn(question_mark, scale=0.5))
        self.wait(8) # Corresponds to: "But what happens when the test itself is flawed? That's where test validation fixes come in."

        # Define the 'Fix Test' text, which will replace the 'Test Failed' icon
        fix_test_text = Text("Fix Test", font_size=60, color=BLUE)
        # Set its final position: horizontally centered in main_region, slightly elevated
        fix_test_text.move_to(self.main_region.get_center() + UP * 1.5)

        # Transitioning the 'Test Failed' icon (with question mark) to a 'Fix Test' icon.
        # Also fade out the 'Test Passed' icon as the focus shifts.
        self.play(
        FadeOut(passed_icon),
        Transform(VGroup(failed_icon, question_mark), fix_test_text)
        )
        self.wait(4) # Corresponds to part of: "Test validation ensures our tests are accurate, reliable, and truly measure what they're supposed to."

        # Text highlights 'Test Validation' and 'Trustworthy Tests'.
        test_validation_label = Text("Test Validation", font_size=50, color=YELLOW)
        # Position below 'Fix Test' and align its left edge with 'Fix Test'
        test_validation_label.next_to(fix_test_text, DOWN, buff=0.8)
        test_validation_label.align_to(fix_test_text, LEFT)

        trustworthy_tests_label = Text("Trustworthy Tests", font_size=40, color=GREEN)
        # Position below 'Test Validation' and align its left edge with 'Fix Test'
        trustworthy_tests_label.next_to(test_validation_label, DOWN, buff=0.5)
        trustworthy_tests_label.align_to(fix_test_text, LEFT)

        self.play(Write(test_validation_label))
        self.wait(8) # Corresponds to: "Test validation ensures our tests are accurate, reliable, and truly measure what they're supposed to. Sometimes, a 'failed test' doesn't mean a bug in the code, but a bug in the test."

        self.play(Write(trustworthy_tests_label))
        self.wait(9) # Corresponds to: "Fixing these validation issues is essential to maintain trust in our testing process and deliver high-quality software."

# Set narration and duration
Scene1.narration_text = '''Welcome! In software development, tests are crucial for quality. But what happens when the test itself is flawed? That\'s where test validation fixes come in. Test validation ensures our tests are accurate, reliable, and truly measure what they\'re supposed to. Sometimes, a \'failed test\' doesn\'t mean a bug in the code, but a bug in the test. Fixing these validation issues is essential to maintain trust in our testing process and deliver high-quality software.'''
Scene1.audio_duration = 5.0