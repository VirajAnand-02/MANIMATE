import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
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
        # 1. Title
        title = self.create_textbox("Test Enhanced Logging", width=config.frame_width * 0.8, height=1.0)
        title.move_to(UP * (config.frame_height / 2 - 0.5)) # Position at top
        self.play(Write(title))
        self.wait(0.5)

        # 2. Left Side: Code Snippet
        code_str = """
        class CheckoutProcessTest:
        def testGuestUserCheckout(self, userId=123, scenario="empty cart"):
        # ... test logic ...
        log.error("Database connection failed",
        testName=self._testMethodName,
        userId=userId,
        scenario=scenario,
        testId="TC-456")
        """
        code_block = Code(
        code=code_str,
        tab_width=4,
        background_stroke_width=1,
        background_stroke_color=WHITE,
        line_spacing=0.8,
        font_size=20,
        insert_line_no=False,
        style="monokai"
        )

        # Adjust code_block to fit self.left_region
        code_block.set_width(self.left_region.width * 0.9)
        code_block.set_height(self.left_region.height * 0.9)
        code_block.move_to(self.left_region.get_center())

        # Get specific parts of the code for highlighting
        code_lines = code_block.get_content() # This returns a VGroup of lines.

        # Line indices:
        # 0: class CheckoutProcessTest:
        # 1:     def testGuestUserCheckout(self, userId=123, scenario="empty cart"):
        # 2:         # ... test logic ...
        # 3:         log.error("Database connection failed",
        # 4:                   testName=self._testMethodName,
        # 5:                   userId=userId,
        # 6:                   scenario=scenario,
        # 7:                   testId="TC-456")

        code_method_name_line = code_lines[1]
        code_method_name = code_method_name_line[4:23] # "testGuestUserCheckout"

        code_userid_line = code_lines[5]
        code_userid = code_userid_line[18:25] # "userId=userId"

        code_scenario_line = code_lines[6]
        code_scenario = code_scenario_line[18:33] # "scenario=scenario"

        code_testid_line = code_lines[7]
        code_testid = code_testid_line[18:30] # "testId="TC-456""

        # 3. Right Side: Log Output
        generic_log_str = "Error: Database connection failed"
        generic_log = Text(generic_log_str, font_size=30, color=RED)
        generic_log.set_width(self.right_region.width * 0.9)
        generic_log.move_to(self.right_region.get_center())

        # Enhanced log (using MarkupText for easy part access)
        enhanced_log_markup_str = (
        f"Error: Database connection failed in <span fgcolor='{YELLOW}'>CheckoutProcessTest.testGuestUserCheckout()</span> "
        f"with <span fgcolor='{BLUE}'>userId: 123</span>, "
        f"<span fgcolor='{GREEN}'>scenario: 'empty cart'</span>, "
        f"test ID: <span fgcolor='{RED}'>'TC-456'</span>."
        )
        enhanced_log = MarkupText(enhanced_log_markup_str, font_size=28)
        enhanced_log.set_width(self.right_region.width * 0.9)
        enhanced_log.move_to(self.right_region.get_center())

        # Get parts of the enhanced log
        log_method_name = enhanced_log.get_parts_by_tex("CheckoutProcessTest.testGuestUserCheckout()")
        log_userid = enhanced_log.get_parts_by_tex("userId: 123")
        log_scenario = enhanced_log.get_parts_by_tex("scenario: 'empty cart'")
        log_testid = enhanced_log.get_parts_by_tex("TC-456")

        # Initial display
        self.play(FadeIn(code_block), FadeIn(generic_log))
        self.wait(8) # Narration: "At its heart, Test Enhanced Logging means enriching your application's logs with specific details from the test environment as your tests execute."

        # Narration Part 1: "Imagine your logs not just saying 'Error: Database connection failed', but 'Error: Database connection failed in CheckoutProcessTest.testGuestUserCheckout() with userId: 123, scenario: 'empty cart', test ID: 'TC-456'."
        # Highlight code method name
        highlight_code_method = SurroundingRectangle(code_method_name, color=YELLOW, buff=0.05)
        self.play(Create(highlight_code_method))
        self.wait(1)

        # Transform generic log to enhanced log
        self.play(ReplacementTransform(generic_log, enhanced_log), run_time=1.5)
        self.wait(1)

        # Highlight log method name
        highlight_log_method = SurroundingRectangle(log_method_name, color=YELLOW, buff=0.05)
        self.play(Create(highlight_log_method))
        self.wait(1)

        # Arrow from code method to log method
        arrow1 = Arrow(highlight_code_method.get_right(), highlight_log_method.get_left(), buff=0.1, color=YELLOW)
        self.play(Create(arrow1))
        self.wait(8.5) # Continue narration

        # Narration Part 2: "We can inject a variety of context: the test method name, a unique test run ID, input parameters used, the user story being tested, or even associated bug IDs."
        # Highlight userId
        highlight_code_userid = SurroundingRectangle(code_userid, color=BLUE, buff=0.05)
        highlight_log_userid = SurroundingRectangle(log_userid, color=BLUE, buff=0.05)
        arrow2 = Arrow(highlight_code_userid.get_right(), highlight_log_userid.get_left(), buff=0.1, color=BLUE)
        self.play(
        Create(highlight_code_userid),
        Create(highlight_log_userid),
        Create(arrow2),
        run_time=1.5
        )
        self.wait(2)

        # Highlight scenario
        highlight_code_scenario = SurroundingRectangle(code_scenario, color=GREEN, buff=0.05)
        highlight_log_scenario = SurroundingRectangle(log_scenario, color=GREEN, buff=0.05)
        arrow3 = Arrow(highlight_code_scenario.get_right(), highlight_log_scenario.get_left(), buff=0.1, color=GREEN)
        self.play(
        Create(highlight_code_scenario),
        Create(highlight_log_scenario),
        Create(arrow3),
        run_time=1.5
        )
        self.wait(2)

        # Highlight testId
        highlight_code_testid = SurroundingRectangle(code_testid, color=RED, buff=0.05)
        highlight_log_testid = SurroundingRectangle(log_testid, color=RED, buff=0.05)
        arrow4 = Arrow(highlight_code_testid.get_right(), highlight_log_testid.get_left(), buff=0.1, color=RED)
        self.play(
        Create(highlight_code_testid),
        Create(highlight_log_testid),
        Create(arrow4),
        run_time=1.5
        )
        self.wait(1.5) # Continue narration

        # Narration Part 3: "This immediate context tells you *what* test failed, *under what conditions*, and *with what data*, drastically cutting down debugging time and helping you pinpoint the root cause faster."
        # Circumscribe the entire enhanced log
        self.play(Circumscribe(enhanced_log, color=WHITE, buff=0.1), run_time=1.5)
        self.wait(2)

        # Fade out all highlights and arrows
        all_highlights = VGroup(
        highlight_code_method, highlight_log_method,
        highlight_code_userid, highlight_log_userid,
        highlight_code_scenario, highlight_log_scenario,
        highlight_code_testid, highlight_log_testid
        )
        all_arrows = VGroup(arrow1, arrow2, arrow3, arrow4)

        self.play(
        FadeOut(all_highlights),
        FadeOut(all_arrows),
        run_time=1.5
        )
        self.wait(2)

        # Final fade out of main content and title
        self.play(FadeOut(code_block), FadeOut(enhanced_log), FadeOut(title), run_time=1.5)
        self.wait(1.5)

# Set narration and duration
Scene2.narration_text = '''At its heart, Test Enhanced Logging means enriching your application\'s logs with specific details from the test environment as your tests execute. Imagine your logs not just saying \'Error: Database connection failed\', but \'Error: Database connection failed in `CheckoutProcessTest.testGuestUserCheckout()` with userId: 123, scenario: \'empty cart\', test ID: \'TC-456\'. We can inject a variety of context: the test method name, a unique test run ID, input parameters used, the user story being tested, or even associated bug IDs. This immediate context tells you *what* test failed, *under what conditions*, and *with what data*, drastically cutting down debugging time and helping you pinpoint the root cause faster.'''
Scene2.audio_duration = 5.0
