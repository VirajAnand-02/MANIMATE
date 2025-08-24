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

class Scene3(SplitScreen):
    def construct_scene(self):
        # Narration: "The benefits of this approach are clear."
        title_text = self.create_textbox(
        "The benefits of this approach are clear.",
        width=self.left_region.width * 0.9,
        height=self.left_region.height * 0.15
        )
        title_text.move_to(self.left_region.get_top() - UP * title_text.height / 2 - UP * 0.2)
        self.play(Write(title_text), run_time=1.5)
        self.wait(0.5)

        # --- Left Side: Bar Graph for Throughput ---
        # Narration: "First, significantly increased throughput."
        # "You can test more units in the same amount of time, or the same number of units in much less time."
        # "This translates directly to reduced manufacturing costs and faster time-to-market."

        # Define the plotting area within the left region
        graph_area = Rectangle(
        width=self.left_region.width * 0.9,
        height=self.left_region.height * 0.6,
        color=BLACK,
        fill_opacity=0
        ).move_to(self.left_region.get_center() + DOWN * 0.1)

        axes = Axes(
        x_range=[0, 2, 1],
        y_range=[0, 100, 20],
        x_length=graph_area.width * 0.8,
        y_length=graph_area.height * 0.8,
        axis_config={"color": GRAY, "stroke_width": 2},
        x_axis_config={"numbers_to_include": [0.5, 1.5]},
        y_axis_config={"numbers_to_include": [0, 20, 40, 60, 80, 100]},
        tips=False
        ).move_to(graph_area.get_center())

        x_labels = VGroup(
        Text("Before", font_size=28).next_to(axes.x_axis.get_tick_marks()[0], DOWN),
        Text("After", font_size=28).next_to(axes.x_axis.get_tick_marks()[1], DOWN)
        )
        y_label = Text("Units per Hour", font_size=28).next_to(axes.y_axis, LEFT, buff=0.2).rotate(90 * DEGREES)

        # Initial bar (Before)
        bar_width = axes.x_axis.get_unit_size() * 0.6
        before_bar = Rectangle(
        width=bar_width,
        height=axes.coords_to_point(0.5, 30)[1] - axes.coords_to_point(0.5, 0)[1],
        fill_opacity=0.8,
        color=BLUE_D,
        stroke_width=0
        ).move_to(axes.coords_to_point(0.5, 15))

        # Target bar (After)
        after_bar_target = Rectangle(
        width=bar_width,
        height=axes.coords_to_point(1.5, 90)[1] - axes.coords_to_point(1.5, 0)[1],
        fill_opacity=0.8,
        color=GREEN_D,
        stroke_width=0
        ).move_to(axes.coords_to_point(1.5, 45))

        # Initial 'After' bar (short, for animation)
        after_bar_initial = Rectangle(
        width=bar_width,
        height=axes.coords_to_point(1.5, 30)[1] - axes.coords_to_point(1.5, 0)[1],
        fill_opacity=0.8,
        color=GREEN_D,
        stroke_width=0
        ).move_to(axes.coords_to_point(1.5, 15))

        throughput_text = Text("Increased Throughput", font_size=36, color=YELLOW).next_to(axes, UP, buff=0.5)
        reduced_cost_text = Text("Reduced Cost", font_size=32, color=ORANGE).next_to(throughput_text, DOWN, buff=0.3).align_to(throughput_text, LEFT)
        faster_time_text = Text("Faster Time-to-Market", font_size=32, color=RED).next_to(reduced_cost_text, DOWN, buff=0.3).align_to(throughput_text, LEFT)

        self.play(
        Create(axes),
        Write(x_labels),
        Write(y_label),
        FadeIn(before_bar),
        FadeIn(after_bar_initial),
        run_time=2
        )
        self.wait(1) # "First, significantly increased throughput."

        self.play(
        Transform(after_bar_initial, after_bar_target),
        FadeIn(throughput_text, shift=UP),
        run_time=3
        )
        self.wait(2) # "You can test more units..."

        self.play(
        FadeIn(reduced_cost_text, shift=UP),
        FadeIn(faster_time_text, shift=UP),
        run_time=2
        )
        self.wait(2) # "This translates directly..."

        # --- Right Side: Parallel Testing Jig ---
        # Narration: "Second, better utilization of test equipment and personnel."
        # "Instead of one operator waiting for a test to complete, they can manage multiple tests running in parallel."
        # "This method is perfect for applications like functional testing of multiple identical circuit boards, calibrating several sensors at once, or even burning in batches of devices simultaneously."

        # Clear left side for next animation or keep it faded
        self.play(
        FadeOut(VGroup(axes, x_labels, y_label, before_bar, after_bar_initial, throughput_text, reduced_cost_text, faster_time_text)),
        FadeOut(title_text),
        run_time=1.5
        )

        jig_base = RoundedRectangle(
        width=self.right_region.width * 0.9,
        height=self.right_region.height * 0.7,
        corner_radius=0.2,
        fill_color=GREY_BROWN,
        fill_opacity=0.8,
        stroke_color=GREY_A,
        stroke_width=3
        ).move_to(self.right_region.get_center())

        device_slots = VGroup(*[
        RoundedRectangle(
        width=jig_base.width * 0.3,
        height=jig_base.height * 0.2,
        corner_radius=0.05,
        fill_color=GREY_E,
        fill_opacity=1,
        stroke_color=GREY_A,
        stroke_width=1
        ) for _ in range(4)
        ]).arrange_in_grid(rows=2, cols=2, buff=0.5).move_to(jig_base.get_center())

        devices = VGroup(*[
        RoundedRectangle(
        width=slot.width * 0.8,
        height=slot.height * 0.8,
        corner_radius=0.03,
        fill_color=BLUE_E,
        fill_opacity=1,
        stroke_color=BLUE_A,
        stroke_width=1
        ) for slot in device_slots
        ])

        # Initial positions for devices to animate placement
        initial_device_positions = VGroup(*[
        device.copy().shift(UP * 2 + (LEFT if i % 2 == 0 else RIGHT) * 0.5) for i, device in enumerate(devices)
        ])

        indicators = VGroup(*[
        Dot(radius=0.1, color=GREY_B).next_to(slot, UP, buff=0.1) for slot in device_slots
        ])

        connections = VGroup(*[
        Line(device.get_top(), indicator.get_bottom(), color=YELLOW_A, stroke_width=2)
        for device, indicator in zip(devices, indicators)
        ])

        self.play(
        FadeIn(jig_base),
        LaggedStart(*[FadeIn(slot) for slot in device_slots], lag_ratio=0.2),
        run_time=2
        )
        self.wait(1) # "Second, better utilization..."

        # Animate placing devices
        self.play(
        LaggedStart(*[
        TransformFromCopy(initial_device_positions[i], devices[i])
        for i in range(4)
        ], lag_ratio=0.3, run_time=3)
        )
        self.wait(1) # "Instead of one operator..."

        self.play(
        LaggedStart(*[Create(conn) for conn in connections], lag_ratio=0.1),
        run_time=2
        )
        self.wait(1)

        # Animate indicators lighting up
        self.play(
        LaggedStart(*[FadeIn(ind) for ind in indicators], lag_ratio=0.1),
        run_time=1
        )
        self.play(
        LaggedStart(*[ind.animate.set_color(GREEN_E) for ind in indicators], lag_ratio=0.1),
        run_time=2
        )
        self.wait(3) # "This method is perfect for applications..."

        self.play(
        FadeOut(jig_base),
        FadeOut(device_slots),
        FadeOut(devices),
        FadeOut(indicators),
        FadeOut(connections),
        run_time=1.5
        )
        self.wait(0.5)

# Set narration and duration
Scene3.narration_text = '''The benefits of this approach are clear. First, significantly increased throughput. You can test more units in the same amount of time, or the same number of units in much less time. This translates directly to reduced manufacturing costs and faster time-to-market. Second, better utilization of test equipment and personnel. Instead of one operator waiting for a test to complete, they can manage multiple tests running in parallel. This method is perfect for applications like functional testing of multiple identical circuit boards, calibrating several sensors at once, or even burning in batches of devices simultaneously.'''
Scene3.audio_duration = 5.0
