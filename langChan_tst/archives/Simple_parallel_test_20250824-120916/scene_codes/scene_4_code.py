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
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox(
        "Setting up a simple parallel test doesn't have to be overly complex.",
        width=self.title_region.width * 0.9,
        height=self.title_region.height * 0.8
        ).move_to(self.title_region.get_center())
        self.play(Write(title_text), run_time=2)
        self.wait(0.5)

        # Define colors for consistency
        UUT_COLOR = BLUE_C
        FIXTURE_COLOR = GREEN_C
        INSTRUMENT_COLOR = ORANGE_C
        SOFTWARE_COLOR = PURPLE_C
        TEXT_COLOR = WHITE

        # --- Part 1: Multiple Units Under Test (UUTs) ---
        # Create 4 identical circuit boards (rectangles)
        board_width = self.main_region.width * 0.15
        board_height = self.main_region.height * 0.15
        board1 = Rectangle(width=board_width, height=board_height, color=UUT_COLOR, fill_opacity=0.8)
        board2 = board1.copy()
        board3 = board1.copy()
        board4 = board1.copy()

        # Arrange them in a 2x2 grid
        uut_group = VGroup(board1, board2, board3, board4).arrange_in_grid(rows=2, cols=2, buff=0.5)
        uut_group.scale_to_fit_width(self.main_region.width * 0.6)
        uut_group.move_to(self.main_region.get_center() + UP * self.main_region.height * 0.1)

        uut_label = Text("Multiple Units Under Test (UUTs)", font_size=30, color=TEXT_COLOR)
        uut_label.next_to(uut_group, DOWN, buff=0.5)

        self.play(
        FadeIn(uut_group, shift=UP),
        Write(uut_label),
        run_time=3
        )
        self.wait(1.5)

        # --- Part 2: Multi-Unit Test Fixture ---
        # Create a larger rectangle for the fixture, with pogo pins
        fixture_rect = Rectangle(
        width=self.main_region.width * 0.7,
        height=self.main_region.height * 0.5,
        color=FIXTURE_COLOR,
        fill_opacity=0.6,
        stroke_width=3
        )
        # Add some small circles to represent pogo pins
        pogo_pins = VGroup(*[
        Dot(radius=0.05, color=GREY_BROWN, fill_opacity=1).shift(x * RIGHT + y * UP)
        for x in np.linspace(-fixture_rect.width / 2 * 0.8, fixture_rect.width / 2 * 0.8, 5)
        for y in np.linspace(-fixture_rect.height / 2 * 0.8, fixture_rect.height / 2 * 0.8, 4)
        ])
        fixture_group = VGroup(fixture_rect, pogo_pins).move_to(self.main_region.get_center() + UP * self.main_region.height * 0.1)

        fixture_label = Text("Multi-Unit Test Fixture", font_size=30, color=TEXT_COLOR)
        fixture_label.next_to(fixture_group, DOWN, buff=0.5)

        self.play(
        ReplacementTransform(uut_group, fixture_group),
        ReplacementTransform(uut_label, fixture_label),
        run_time=4
        )
        self.wait(1.5)

        # --- Part 3: Shared or Dedicated Instrumentation ---
        # Create a stack of rectangles for test instruments
        instrument_width = self.main_region.width * 0.4
        instrument_height = self.main_region.height * 0.1
        instrument1 = Rectangle(width=instrument_width, height=instrument_height, color=INSTRUMENT_COLOR, fill_opacity=0.7)
        instrument2 = instrument1.copy().set_color(INSTRUMENT_COLOR.lighter(0.5))
        instrument3 = instrument1.copy().set_color(INSTRUMENT_COLOR.darker(0.5))

        instrument_stack = VGroup(instrument1, instrument2, instrument3).arrange(DOWN, buff=0.1)
        instrument_stack.scale_to_fit_height(self.main_region.height * 0.6)
        instrument_stack.move_to(self.main_region.get_center() + UP * self.main_region.height * 0.1)

        instrument_label = Text("Shared or Dedicated Instrumentation", font_size=30, color=TEXT_COLOR)
        instrument_label.next_to(instrument_stack, DOWN, buff=0.5)

        self.play(
        ReplacementTransform(fixture_group, instrument_stack),
        ReplacementTransform(fixture_label, instrument_label),
        run_time=4
        )
        self.wait(1.5)

        # --- Part 4: Test Executive Software ---
        # Create a computer screen with a simple flowchart
        screen_rect = Rectangle(
        width=self.main_region.width * 0.6,
        height=self.main_region.height * 0.5,
        color=SOFTWARE_COLOR,
        fill_opacity=0.7,
        stroke_width=3
        )
        # Simple flowchart inside
        flow_start = Circle(radius=0.15, color=WHITE, fill_opacity=1).set_x(0).set_y(screen_rect.get_top()[1] - 0.5)
        flow_step1 = Rectangle(width=1.5, height=0.5, color=WHITE, fill_opacity=1).next_to(flow_start, DOWN, buff=0.3)
        flow_step2 = Rectangle(width=1.5, height=0.5, color=WHITE, fill_opacity=1).next_to(flow_step1, DOWN, buff=0.3)
        flow_end = Circle(radius=0.15, color=WHITE, fill_opacity=1).next_to(flow_step2, DOWN, buff=0.3)

        arrow1 = Arrow(flow_start.get_bottom(), flow_step1.get_top(), buff=0.1, color=WHITE)
        arrow2 = Arrow(flow_step1.get_bottom(), flow_step2.get_top(), buff=0.1, color=WHITE)
        arrow3 = Arrow(flow_step2.get_bottom(), flow_end.get_top(), buff=0.1, color=WHITE)

        flow_chart = VGroup(flow_start, flow_step1, flow_step2, flow_end, arrow1, arrow2, arrow3)
        flow_chart.scale_to_fit_width(screen_rect.width * 0.6)
        flow_chart.move_to(screen_rect.get_center())

        software_group = VGroup(screen_rect, flow_chart).move_to(self.main_region.get_center() + UP * self.main_region.height * 0.1)

        software_label = Text("Test Executive Software", font_size=30, color=TEXT_COLOR)
        software_label.next_to(software_group, DOWN, buff=0.5)

        self.play(
        ReplacementTransform(instrument_stack, software_group),
        ReplacementTransform(instrument_label, software_label),
        run_time=5
        )
        self.wait(1.5)

        # --- Part 5: Assemble into a cohesive diagram ---
        # Define target positions for each component in the final diagram
        final_fixture_pos = self.main_region.get_center() + LEFT * self.main_region.width * 0.25
        final_instrument_pos = self.main_region.get_center() + RIGHT * self.main_region.width * 0.25 + UP * self.main_region.height * 0.15
        final_software_pos = self.main_region.get_center() + RIGHT * self.main_region.width * 0.25 + DOWN * self.main_region.height * 0.15

        # Scale down components for the final diagram
        fixture_group.scale(0.6).move_to(final_fixture_pos)
        instrument_stack.scale(0.6).move_to(final_instrument_pos)
        software_group.scale(0.6).move_to(final_software_pos)

        # Update labels to match new positions
        fixture_label.next_to(fixture_group, DOWN, buff=0.3).scale(0.7)
        instrument_label.next_to(instrument_stack, DOWN, buff=0.3).scale(0.7)
        software_label.next_to(software_group, DOWN, buff=0.3).scale(0.7)

        # Create new instances for the final assembly if needed, or re-use and transform
        # For simplicity, let's re-create the fixture and instrumentation from their original definitions
        # and then transform the current software_group into its final position.

        # Re-create fixture and instrumentation for the final layout
        final_fixture_rect = Rectangle(
        width=self.main_region.width * 0.7 * 0.6, # scaled
        height=self.main_region.height * 0.5 * 0.6, # scaled
        color=FIXTURE_COLOR,
        fill_opacity=0.6,
        stroke_width=3
        )
        final_pogo_pins = VGroup(*[
        Dot(radius=0.05 * 0.6, color=GREY_BROWN, fill_opacity=1).shift(x * RIGHT + y * UP)
        for x in np.linspace(-final_fixture_rect.width / 2 * 0.8, final_fixture_rect.width / 2 * 0.8, 5)
        for y in np.linspace(-final_fixture_rect.height / 2 * 0.8, final_fixture_rect.height / 2 * 0.8, 4)
        ])
        final_fixture_group = VGroup(final_fixture_rect, final_pogo_pins).move_to(final_fixture_pos)
        final_fixture_label = Text("Multi-Unit Test Fixture", font_size=30 * 0.7, color=TEXT_COLOR).next_to(final_fixture_group, DOWN, buff=0.3)

        final_instrument1 = Rectangle(width=instrument_width * 0.6, height=instrument_height * 0.6, color=INSTRUMENT_COLOR, fill_opacity=0.7)
        final_instrument2 = final_instrument1.copy().set_color(INSTRUMENT_COLOR.lighter(0.5))
        final_instrument3 = final_instrument1.copy().set_color(INSTRUMENT_COLOR.darker(0.5))
        final_instrument_stack = VGroup(final_instrument1, final_instrument2, final_instrument3).arrange(DOWN, buff=0.1 * 0.6)
        final_instrument_stack.move_to(final_instrument_pos)
        final_instrument_label = Text("Instrumentation", font_size=30 * 0.7, color=TEXT_COLOR).next_to(final_instrument_stack, DOWN, buff=0.3)

        final_software_group = software_group.copy().scale(0.6).move_to(final_software_pos)
        final_software_label = Text("Test Executive", font_size=30 * 0.7, color=TEXT_COLOR).next_to(final_software_group, DOWN, buff=0.3)

        # Arrows connecting them
        arrow_fixture_to_instrument = Arrow(
        final_fixture_group.get_right(),
        final_instrument_stack.get_left(),
        buff=0.1,
        color=WHITE,
        stroke_width=4
        )
        arrow_instrument_to_software = Arrow(
        final_instrument_stack.get_right(),
        final_software_group.get_left(),
        buff=0.1,
        color=WHITE,
        stroke_width=4
        )
        arrow_software_to_fixture = Arrow(
        final_software_group.get_bottom(),
        final_fixture_group.get_right() + DOWN * 0.5, # Adjust for better visual flow
        buff=0.1,
        color=WHITE,
        stroke_width=4
        ).set_points_as_corners([
        final_software_group.get_bottom(),
        final_software_group.get_bottom() + DOWN * 0.5,
        final_fixture_group.get_right() + DOWN * 0.5,
        final_fixture_group.get_right()
        ])


        self.play(
        Transform(software_group, final_software_group),
        Transform(software_label, final_software_label),
        FadeOut(fixture_group, shift=LEFT), # Fade out previous, fade in new for clarity
        FadeOut(fixture_label, shift=LEFT),
        FadeOut(instrument_stack, shift=LEFT),
        FadeOut(instrument_label, shift=LEFT),
        FadeIn(final_fixture_group, shift=LEFT),
        FadeIn(final_fixture_label, shift=LEFT),
        FadeIn(final_instrument_stack, shift=LEFT),
        FadeIn(final_instrument_label, shift=LEFT),
        run_time=3
        )

        self.play(
        Create(arrow_fixture_to_instrument),
        Create(arrow_instrument_to_software),
        Create(arrow_software_to_fixture),
        run_time=2
        )

        # Add a final encompassing label
        final_diagram_label = Text(
        "Simple Parallel Test Station",
        font_size=40,
        color=YELLOW
        ).next_to(final_fixture_group, UP, buff=0.8).align_to(self.main_region, LEFT)

        self.play(Write(final_diagram_label), run_time=1.5)
        self.wait(3)

# Set narration and duration
Scene4.narration_text = '''Setting up a simple parallel test doesn\'t have to be overly complex. You typically need a multi-unit test fixture or multiple identical fixtures, which physically hold and connect to your units under test. You\'ll also need test instrumentation – this could be shared resources like a power supply or dedicated instruments for each station. Finally, a test executive software is crucial. This software orchestrates the parallel test sequences, manages data logging for each unit, and provides a unified interface. By carefully designing these components, you can efficiently scale up your testing without a massive investment in entirely separate test systems.'''
Scene4.audio_duration = 5.0
