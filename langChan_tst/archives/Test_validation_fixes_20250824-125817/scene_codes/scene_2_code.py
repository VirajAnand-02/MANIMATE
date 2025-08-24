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
        # 1. Create and display the title
        title_text = "Identifying Test Validation Problems"
        title = self.create_textbox(title_text, width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(Write(title), run_time=3)
        self.wait(0.5)

        # 2. Left Side: Flaky Test Graph
        # Define axes for the left region
        left_axes_width = self.left_region.width * 0.9
        left_axes_height = self.left_region.height * 0.7

        axes = Axes(
        x_range=[0, 10, 1],
        y_range=[0, 1.1, 1], # 0 for Fail, 1 for Pass
        x_length=left_axes_width,
        y_length=left_axes_height,
        axis_config={"color": GRAY, "stroke_width": 2},
        x_axis_config={"numbers_to_include": []}, # No numbers on x-axis for simplicity
        y_axis_config={"numbers_to_include": [0, 1]},
        tips=False
        )
        axes.move_to(self.left_region.get_center())

        # Add labels for Pass/Fail
        fail_label = Text("Fail", font_size=28, color=RED).next_to(axes.y_axis.get_tick_marks()[0], LEFT, buff=0.2)
        pass_label = Text("Pass", font_size=28, color=GREEN).next_to(axes.y_axis.get_tick_marks()[1], LEFT, buff=0.2)

        # Create a "flaky" line representing inconsistent pass/fail
        flaky_points_data = [
        (0, 0.1), (1, 0.9), (2, 0.1), (3, 0.9), (4, 0.1), (5, 0.9),
        (6, 0.5), (7, 0.9), (8, 0.1), (9, 0.9), (10, 0.1)
        ]
        flaky_graph = axes.plot_line_graph(
        x_values=[p[0] for p in flaky_points_data],
        y_values=[p[1] for p in flaky_points_data],
        line_color=YELLOW,
        add_vertex_dots=False
        )

        self.play(Create(axes), Write(fail_label), Write(pass_label), run_time=3)
        self.play(Create(flaky_graph), run_time=6)
        self.wait(1)

        # 3. Right Side: Puzzled Developer & False Positives/Negatives
        report_text = Text("Test Failed!", color=RED, font_size=48)
        app_works_text = Text("Application Works Correctly", color=GREEN, font_size=36)
        question_mark = Text("?", color=YELLOW, font_size=60)

        # Arrange these elements in the upper part of the right region
        report_text.move_to(self.right_region.get_center() + UP * self.right_region.height * 0.3)
        app_works_text.next_to(report_text, DOWN, buff=0.4)
        question_mark.next_to(report_text, UP, buff=0.3)

        self.play(Write(report_text), run_time=2)
        self.play(FadeIn(app_works_text), run_time=2)
        self.play(FadeIn(question_mark), run_time=1.5)
        self.wait(2)

        # Introduce "False Positive" and "False Negative" concepts
        false_positive_title = Text("False Positive", color=ORANGE, font_size=32)
        fp_desc_test = VGroup(Cross(color=RED).scale(0.3), Text("Test Fails", color=RED, font_size=24)).arrange(RIGHT, buff=0.2)
        fp_desc_app = VGroup(CheckSquare(color=GREEN).scale(0.3), Text("App Works", color=GREEN, font_size=24)).arrange(RIGHT, buff=0.2)
        fp_group_content = VGroup(
        false_positive_title,
        fp_desc_test,
        fp_desc_app
        ).arrange(DOWN, buff=0.2)

        false_negative_title = Text("False Negative", color=PURPLE, font_size=32)
        fn_desc_test = VGroup(CheckSquare(color=GREEN).scale(0.3), Text("Test Passes", color=GREEN, font_size=24)).arrange(RIGHT, buff=0.2)
        fn_desc_app = VGroup(Cross(color=RED).scale(0.3), Text("Bug Exists", color=RED, font_size=24)).arrange(RIGHT, buff=0.2)
        fn_group_content = VGroup(
        false_negative_title,
        fn_desc_test,
        fn_desc_app
        ).arrange(DOWN, buff=0.2)

        # Arrange FP and FN side-by-side in the lower part of the right region
        fp_fn_container = VGroup(fp_group_content, fn_group_content).arrange(RIGHT, buff=0.8)
        fp_fn_container.move_to(self.right_region.get_center() + DOWN * self.right_region.height * 0.3)

        # Scale down if the combined group is too wide for the region
        if fp_fn_container.width > self.right_region.width * 0.9:
        fp_fn_container.scale(self.right_region.width * 0.9 / fp_fn_container.width)
        fp_fn_container.move_to(self.right_region.get_center() + DOWN * self.right_region.height * 0.3)

        self.play(FadeIn(fp_group_content), run_time=4)
        self.wait(0.5)
        self.play(FadeIn(fn_group_content), run_time=4)
        self.wait(4)

# Set narration and duration
Scene2.narration_text = '''Identifying a test validation problem is the first step. Look for tests that consistently fail on stable code, or produce \'flaky\' results – passing sometimes, failing others, without any code changes. Be wary of false positives, where a test passes but a bug still exists, or false negatives, where a test fails but there\'s no actual issue. These often stem from outdated assumptions, incorrect data, or environmental inconsistencies that distort the test\'s true purpose.'''
Scene2.audio_duration = 5.0
