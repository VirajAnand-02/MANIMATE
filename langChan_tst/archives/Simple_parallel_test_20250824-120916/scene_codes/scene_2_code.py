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
        from manim import *

        class GeneratedScene_2(Scene):
        def construct(self):
        # Assume self.left_region and self.right_region are Mobjects (e.g., Rectangles)
        # Assume self.create_textbox(text, width, height) is available.
        # For this example, we'll define dummy regions and create_textbox if they don't exist
        # in the environment where this code is run standalone.
        # In the actual template, these would be provided.
        if not hasattr(self, 'left_region'):
        self.left_region = Rectangle(width=config.frame_width / 2 - 0.5, height=config.frame_height - 2, color=GRAY).to_edge(LEFT, buff=0.25).shift(DOWN*0.5)
        self.right_region = Rectangle(width=config.frame_width / 2 - 0.5, height=config.frame_height - 2, color=GRAY).to_edge(RIGHT, buff=0.25).shift(DOWN*0.5)
        # self.add(self.left_region, self.right_region) # For debugging regions
        if not hasattr(self, 'create_textbox'):
        def _create_textbox(text_str, width, height):
        # Simple Text for standalone execution
        text_mobj = Text(text_str, font_size=48)
        if text_mobj.width > width:
        text_mobj.width = width
        if text_mobj.height > height:
        text_mobj.height = height
        return text_mobj
        self.create_textbox = _create_textbox

        # 1. Create the title text
        title = self.create_textbox("How does it work?", width=config.frame_width * 0.8, height=1)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # Define common properties for boards and fixtures
        board_width = 1.5
        board_height = 1
        fixture_width = 2
        fixture_height = 1.5
        board_color = BLUE_E
        fixture_color = GRAY_A
        fill_opacity_board = 0.8
        fill_opacity_fixture = 0.3

        # --- Left Side: Sequential Testing ---
        label_left = Text("Sequential Testing", font_size=36).next_to(self.left_region, UP, buff=0.5)
        board_left = Rectangle(width=board_width, height=board_height, color=board_color, fill_opacity=fill_opacity_board)
        fixture_left = Rectangle(width=fixture_width, height=fixture_height, color=fixture_color, fill_opacity=fill_opacity_fixture)

        # Position elements within the left region
        fixture_left.move_to(self.left_region.get_center() + DOWN * 0.5)
        board_left.move_to(fixture_left.get_center() + UP * (fixture_height / 2 + board_height / 2 + 0.5)) # Start above fixture

        # Progress bar for left side
        test_bar_left_outline = Rectangle(width=fixture_width, height=0.3, color=WHITE)
        test_bar_left_outline.next_to(fixture_left, DOWN, buff=0.5)
        test_bar_left_fill = Rectangle(width=0.01, height=0.3, color=GREEN, fill_opacity=1).align_to(test_bar_left_outline, LEFT)
        test_text_left = Text("Test in Progress", font_size=24).next_to(test_bar_left_outline, UP, buff=0.1)

        # --- Right Side: Parallel Testing ---
        label_right = Text("Parallel Testing", font_size=36).next_to(self.right_region, UP, buff=0.5)

        # Create three identical boards and fixtures
        num_parallel_tests = 3
        boards_right = VGroup(*[
        Rectangle(width=board_width * 0.8, height=board_height * 0.8, color=board_color, fill_opacity=fill_opacity_board)
        for _ in range(num_parallel_tests)
        ]).arrange(RIGHT, buff=0.8)

        fixtures_right = VGroup(*[
        Rectangle(width=fixture_width * 0.8, height=fixture_height * 0.8, color=fixture_color, fill_opacity=fill_opacity_fixture)
        for _ in range(num_parallel_tests)
        ]).arrange(RIGHT, buff=0.5)

        # Position elements within the right region
        fixtures_right.move_to(self.right_region.get_center() + DOWN * 0.5)
        boards_right.move_to(fixtures_right.get_center() + UP * (fixture_height * 0.8 / 2 + board_height * 0.8 / 2 + 0.5)) # Start above fixtures

        # Progress bars for right side
        test_bars_right_outline = VGroup(*[
        Rectangle(width=fixture_width * 0.8, height=0.25, color=WHITE)
        for _ in range(num_parallel_tests)
        ]).arrange(RIGHT, buff=0.5)
        test_bars_right_outline.next_to(fixtures_right, DOWN, buff=0.3)

        test_bars_right_fill = VGroup(*[
        Rectangle(width=0.01, height=0.25, color=GREEN, fill_opacity=1).align_to(outline, LEFT)
        for outline in test_bars_right_outline
        ])

        test_texts_right = VGroup(*[
        Text("Test in Progress", font_size=18).next_to(outline, UP, buff=0.1)
        for outline in test_bars_right_outline
        ])

        # Data stream arrows for right side
        arrows = VGroup()
        for i in range(num_parallel_tests):
        arrow = Arrow(
        start=boards_right[i].get_bottom() + DOWN * 0.1,
        end=test_bars_right_outline[i].get_top() + UP * 0.1,
        buff=0.1,
        color=YELLOW,
        stroke_width=5,
        max_tip_length_to_length_ratio=0.15
        )
        arrows.add(arrow)
        arrows.set_opacity(0) # Start invisible

        # --- Animations ---

        # Introduce all static elements
        self.play(
        FadeIn(label_left, board_left, fixture_left),
        FadeIn(label_right, boards_right, fixtures_right),
        run_time=3
        )
        self.wait(1)

        # Move boards into fixtures
        self.play(
        board_left.animate.next_to(fixture_left, UP, buff=0.1),
        boards_right.animate.next_to(fixtures_right, UP, buff=0.1),
        run_time=2
        )
        self.wait(1)

        # Introduce progress bars
        self.play(
        Create(test_bar_left_outline), Write(test_text_left),
        Create(test_bars_right_outline), Write(test_texts_right),
        run_time=2
        )
        self.wait(1)

        # Create the final state of the fill bars for Transform
        final_bar_left_fill = Rectangle(width=fixture_width, height=0.3, color=GREEN, fill_opacity=1).align_to(test_bar_left_outline, LEFT)
        final_bars_right_fill = VGroup(*[
        Rectangle(width=fixture_width * 0.8, height=0.25, color=GREEN, fill_opacity=1).align_to(outline, LEFT)
        for outline in test_bars_right_outline
        ])

        # Play the right side animations (fill and arrows) concurrently with the start of the left side fill
        # The total run_time for this combined play will be determined by the longest animation within it.
        # We want the right side to finish quickly, while the left side continues.

        # We'll use a ValueTracker for the left bar to control its fill independently
        left_fill_tracker = ValueTracker(0)
        test_bar_left_fill.add_updater(
        lambda m: m.become(
        Rectangle(
        width=fixture_width * left_fill_tracker.get_value(),
        height=0.3,
        color=GREEN,
        fill_opacity=1
        ).align_to(test_bar_left_outline, LEFT)
        )
        )
        self.add(test_bar_left_fill) # Add the initial (empty) fill bar to the scene

        self.play(
        left_fill_tracker.animate.set_value(1), # Start left bar filling (will continue for 20s)
        AnimationGroup( # Group for parallel right-side animations
        Transform(test_bars_right_fill[0], final_bars_right_fill[0]),
        Transform(test_bars_right_fill[1], final_bars_right_fill[1]),
        Transform(test_bars_right_fill[2], final_bars_right_fill[2]),
        lag_ratio=0.1, # Small lag for visual appeal between parallel bars
        run_time=5, rate_func=linear # Right side finishes in 5 seconds
        ),
        FadeIn(arrows, shift=UP, run_time=2), # Arrows appear quickly
        run_time=20 # The overall play duration is set by the longest animation (left_fill_tracker)
        )

        # Remove updater for left bar after its animation is complete
        test_bar_left_fill.remove_updater(test_bar_left_fill.updaters[0])

        self.wait(1) # Wait a bit after all tests are visually complete

        # Clean up
        self.play(
        FadeOut(test_bar_left_outline, test_bar_left_fill, test_text_left, board_left),
        FadeOut(test_bars_right_outline, test_bars_right_fill, test_texts_right, arrows, boards_right),
        run_time=2
        )
        self.wait(1)

        self.play(
        FadeOut(title, label_left, fixture_left, label_right, fixtures_right),
        run_time=2
        )
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''So, how does it work? Imagine you have three identical items to test. Instead of testing item A, waiting for it to finish, then testing item B, and so on, simple parallel testing means you test item A, item B, and item C at the exact same time. Each item goes through its own independent test sequence, even if they share some common resources or are managed by a single system. The key is that their tests run concurrently, not sequentially. Think of it like a supermarket with multiple checkout lanes instead of just one – vastly increasing throughput.'''
Scene2.audio_duration = 5.0
