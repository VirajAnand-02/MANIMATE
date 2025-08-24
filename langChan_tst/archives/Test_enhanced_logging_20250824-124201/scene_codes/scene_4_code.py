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
        import numpy as np
        import random

        def construct_scene(self):
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox(
        "Test Enhanced Logging in Complex Scenarios",
        self.title_region.width,
        self.title_region.height
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(0.5)

        # 2. Dashboard-like view with graphs and log entries
        dashboard_elements = VGroup()

        # Create two placeholder graphs
        graph1 = Rectangle(
        width=self.main_region.width * 0.4,
        height=self.main_region.height * 0.3,
        color=BLUE_A,
        fill_opacity=0.2,
        stroke_width=2
        )
        # Simulate data lines for graph1
        graph1_data = VGroup(*[
        Line(graph1.get_bottom() + RIGHT * (i * graph1.width / 10),
        graph1.get_bottom() + RIGHT * (i * graph1.width / 10) + UP * (np.sin(i / 2) + 1.5) * graph1.height / 3,
        color=BLUE_C, stroke_width=2)
        for i in range(10)
        ])
        graph1_data.move_to(graph1.get_center())
        graph1_group = VGroup(graph1, graph1_data)

        graph2 = Rectangle(
        width=self.main_region.width * 0.4,
        height=self.main_region.height * 0.3,
        color=GREEN_A,
        fill_opacity=0.2,
        stroke_width=2
        )
        # Simulate data lines for graph2
        graph2_data = VGroup(*[
        Line(graph2.get_bottom() + RIGHT * (i * graph2.width / 10),
        graph2.get_bottom() + RIGHT * (i * graph2.width / 10) + UP * (np.cos(i / 2) + 1.5) * graph2.height / 3,
        color=GREEN_C, stroke_width=2)
        for i in range(10)
        ])
        graph2_data.move_to(graph2.get_center())
        graph2_group = VGroup(graph2, graph2_data)

        # Create structured log entries
        log_entry1 = Text("{\"level\": \"INFO\", \"service\": \"auth\", \"message\": \"User logged in\"}", font_size=20, color=WHITE)
        log_entry2 = Text("{\"level\": \"ERROR\", \"service\": \"payment\", \"message\": \"Transaction failed: Insufficient funds\"}", font_size=20, color=RED_A)
        log_entry3 = Text("{\"level\": \"DEBUG\", \"service\": \"api\", \"message\": \"Request received: /data\"}", font_size=20, color=GRAY_A)
        log_entry4 = Text("{\"level\": \"WARN\", \"service\": \"data_proc\", \"message\": \"Sensitive data detected in payload\"}", font_size=20, color=YELLOW_A)

        log_lines = VGroup(log_entry1, log_entry2, log_entry3, log_entry4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        log_lines.set_width(self.main_region.width * 0.8) # Adjust width to fit

        # Arrange all dashboard elements
        dashboard_group = VGroup(
        VGroup(graph1_group, graph2_group).arrange(RIGHT, buff=0.5),
        log_lines
        ).arrange(DOWN, buff=0.8)
        dashboard_group.set_height(self.main_region.height * 0.8)
        dashboard_group.move_to(self.main_region.get_center())

        self.play(FadeIn(dashboard_group, shift=UP), run_time=2)
        self.wait(1)

        # Highlight a log entry
        error_box = SurroundingRectangle(log_entry2, color=RED, buff=0.1)
        self.play(Create(error_box))
        self.wait(2)

        # 3. 'Security Warning' icon flashes
        warning_icon_shape = Triangle(fill_opacity=1, color=YELLOW).scale(0.3)
        warning_icon_text = Text("!", color=BLACK, font_size=30).move_to(warning_icon_shape.get_center() + UP * 0.05)
        warning_icon = VGroup(warning_icon_shape, warning_icon_text)
        warning_icon.next_to(log_entry4, RIGHT, buff=0.2)
        warning_icon.shift(UP * 0.1) # Adjust vertical position slightly

        self.play(Flash(warning_icon, flash_radius=0.5, line_length=0.2, num_lines=10, color=ORANGE), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(error_box, warning_icon))

        # 4. 'Before' vs 'After' comparison
        before_text = Text("Before: Tangled Debugging", font_size=36, color=RED)
        after_text = Text("After: Organized Pipeline", font_size=36, color=GREEN)

        # Position texts
        before_text.move_to(self.main_region.get_center() + UP * self.main_region.height * 0.4 + LEFT * self.main_region.width * 0.25)
        after_text.move_to(self.main_region.get_center() + UP * self.main_region.height * 0.4 + RIGHT * self.main_region.width * 0.25)

        # Create 'Before' - tangled mess of wires
        mess_group = VGroup()
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE, TEAL]
        for _ in range(15):
        start_point = np.array([random.uniform(-3, 3), random.uniform(-2, 2), 0])
        end_point = np.array([random.uniform(-3, 3), random.uniform(-2, 2), 0])
        line = Line(start_point, end_point, color=random.choice(colors), stroke_width=random.uniform(1, 4))
        mess_group.add(line)
        mess_group.set_height(self.main_region.height * 0.5)
        mess_group.move_to(self.main_region.get_center() + LEFT * self.main_region.width * 0.25 + DOWN * self.main_region.height * 0.1)

        self.play(FadeOut(dashboard_group), FadeIn(before_text, mess_group), run_time=1.5)
        self.wait(1)

        # Create 'After' - clear, organized circuit board
        circuit_group = VGroup()
        chip_size = 0.8
        spacing = 0.4
        grid_rows = 3
        grid_cols = 3

        for i in range(grid_rows):
        for j in range(grid_cols):
        chip = Rectangle(width=chip_size, height=chip_size * 0.7, color=BLUE_D, fill_opacity=0.8, stroke_width=1)
        chip.move_to(np.array([
        (j - (grid_cols - 1) / 2) * (chip_size + spacing),
        (i - (grid_rows - 1) / 2) * (chip_size + spacing),
        0
        ]))
        circuit_group.add(chip)

        # Add connection lines
        if j < grid_cols - 1: # Horizontal connections
        line_h = Line(chip.get_right(), chip.get_right() + RIGHT * spacing, color=GRAY_B, stroke_width=2)
        circuit_group.add(line_h)
        if i < grid_rows - 1: # Vertical connections
        line_v = Line(chip.get_top(), chip.get_top() + UP * spacing, color=GRAY_B, stroke_width=2)
        circuit_group.add(line_v)

        circuit_group.set_height(self.main_region.height * 0.5)
        circuit_group.move_to(self.main_region.get_center() + RIGHT * self.main_region.width * 0.25 + DOWN * self.main_region.height * 0.1)

        self.play(
        Transform(mess_group, circuit_group),
        Transform(before_text, after_text),
        run_time=2
        )
        self.wait(2)

        # 5. Final frame: video title and call to action
        call_to_action = Text("Enhance Your Logs!", font_size=60, color=YELLOW)
        call_to_action.move_to(self.main_region.get_center() + DOWN * self.main_region.height * 0.3)

        self.play(
        FadeOut(mess_group, before_text), # before_text was transformed to after_text
        FadeIn(call_to_action),
        title_text.animate.move_to(self.title_region.get_center()), # Ensure title is still centered
        run_time=1.5
        )
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''Beyond basic unit tests, Test Enhanced Logging truly shines in complex scenarios like integration or end-to-end tests, where multiple services interact. It helps pinpoint exactly which part of a larger transaction failed. For best practices, always use structured logging formats like JSON for easy parsing and analysis by log management tools. Be mindful of log levels, ensuring critical test failures are easily identifiable. And crucially, never log sensitive user data without proper redaction or anonymization. By embracing Test Enhanced Logging, you\'re not just writing tests; you\'re building a more robust, debuggable, and transparent testing pipeline. Start enhancing your logs today and transform debugging from a chore into a precise, efficient process!'''
Scene4.audio_duration = 5.0
