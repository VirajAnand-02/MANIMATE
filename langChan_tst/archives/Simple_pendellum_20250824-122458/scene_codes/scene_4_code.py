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

class Scene4(SplitScreen):
    def construct_scene(self):
        # --- Left Region Setup ---
        left_center = self.left_region.get_center()
        left_width = self.left_region.width
        left_height = self.left_region.height

        # --- Right Region Setup ---
        right_center = self.right_region.get_center()
        right_width = self.right_region.width
        right_height = self.right_region.height

        # --- Right Side Text ---
        consistent_period_text = self.create_textbox('Consistent Period', width=right_width * 0.8, height=right_height * 0.1)
        timekeeping_devices_text = self.create_textbox('Timekeeping Devices', width=right_width * 0.8, height=right_height * 0.1)
        musical_tempo_text = self.create_textbox('Musical Tempo', width=right_width * 0.8, height=right_height * 0.1)
        earthquake_detection_text = self.create_textbox('Earthquake Detection', width=right_width * 0.8, height=right_height * 0.1)

        right_texts = VGroup(
        consistent_period_text,
        timekeeping_devices_text,
        musical_tempo_text,
        earthquake_detection_text
        ).arrange(DOWN, buff=0.5).move_to(right_center)

        # --- Grandfather Clock Pendulum ---
        clock_pivot_point = left_center + UP * left_height * 0.35
        clock_body_height = left_height * 0.4
        clock_body_width = left_width * 0.4
        clock_body = Rectangle(width=clock_body_width, height=clock_body_height, color=BROWN, fill_opacity=0.8)
        clock_body.move_to(clock_pivot_point + DOWN * clock_body_height / 2)

        pendulum_length_clock = clock_body_height * 0.6
        pendulum_rod_clock = Line(clock_pivot_point, clock_pivot_point + DOWN * pendulum_length_clock, color=GRAY_A, stroke_width=4)
        pendulum_bob_clock = Circle(radius=0.15, color=GOLD, fill_opacity=1).move_to(pendulum_rod_clock.get_end())

        clock_pendulum = VGroup(pendulum_rod_clock, pendulum_bob_clock)

        angle_tracker_clock = ValueTracker(PI/6) # Initial angle

        def update_clock_pendulum(mobj):
        rod, bob = mobj[0], mobj[1]
        angle = angle_tracker_clock.get_value()
        new_end = clock_pivot_point + rotate_vector(DOWN * pendulum_length_clock, angle)
        rod.put_start_and_end_on(clock_pivot_point, new_end)
        bob.move_to(new_end)

        clock_pendulum.add_updater(update_clock_pendulum)

        # --- Metronome ---
        metronome_pivot_point = left_center + DOWN * left_height * 0.05
        metronome_base_width = left_width * 0.3
        metronome_base_height = left_height * 0.15
        metronome_base = Polygon(
        metronome_pivot_point + LEFT * metronome_base_width / 2 + DOWN * metronome_base_height,
        metronome_pivot_point + RIGHT * metronome_base_width / 2 + DOWN * metronome_base_height,
        metronome_pivot_point,
        color=MAROON_E, fill_opacity=0.9
        )
        metronome_base.shift(DOWN * metronome_base_height * 0.5) # Adjust position
        metronome_pivot_point = metronome_base.get_top() # Recalculate after shift

        metronome_rod_length = left_height * 0.25
        metronome_rod = Line(metronome_pivot_point, metronome_pivot_point + DOWN * metronome_rod_length, color=GRAY_A, stroke_width=4)

        angle_tracker_metronome = ValueTracker(PI/8) # Initial angle

        def update_metronome_rod(mobj):
        angle = angle_tracker_metronome.get_value()
        new_end = metronome_pivot_point + rotate_vector(DOWN * metronome_rod_length, angle)
        mobj.put_start_and_end_on(metronome_pivot_point, new_end)

        metronome_rod.add_updater(update_metronome_rod)

        # --- Seismograph ---
        seismo_frame_center = left_center + DOWN * left_height * 0.35
        seismo_frame_width = left_width * 0.6
        seismo_frame_height = left_height * 0.2
        seismo_frame = Rectangle(width=seismo_frame_width, height=seismo_frame_height, color=BLUE_E, fill_opacity=0.7)
        seismo_frame.move_to(seismo_frame_center)

        seismo_pivot_offset = UP * seismo_frame_height * 0.3
        # This pivot point moves with the frame
        seismo_pivot_point = seismo_frame.get_center() + seismo_pivot_offset 

        seismo_pendulum_length = seismo_frame_height * 0.6
        seismo_pendulum_rod = Line(seismo_pivot_point, seismo_pivot_point + DOWN * seismo_pendulum_length, color=GRAY_A, stroke_width=3)
        seismo_bob = Dot(seismo_pendulum_rod.get_end(), radius=0.1, color=RED)
        seismo_pen = Triangle(fill_opacity=1, color=BLACK).scale(0.05).next_to(seismo_bob, DOWN, buff=0)

        seismo_pendulum_group = VGroup(seismo_pendulum_rod, seismo_bob, seismo_pen)

        # ValueTracker for the pendulum's relative swing (simulating inertia)
        seismo_angle_tracker = ValueTracker(0) 

        def update_seismo_pendulum_group(mobj):
        rod, bob, pen = mobj[0], mobj[1], mobj[2]
        # The pivot point for the pendulum is relative to the current frame position
        current_frame_pivot = seismo_frame.get_center() + seismo_pivot_offset
        angle = seismo_angle_tracker.get_value()

        new_end = current_frame_pivot + rotate_vector(DOWN * seismo_pendulum_length, angle)
        rod.put_start_and_end_on(current_frame_pivot, new_end)
        bob.move_to(new_end)
        pen.next_to(bob, DOWN, buff=0)

        seismo_pendulum_group.add_updater(update_seismo_pendulum_group)

        seismo_paper_width = seismo_frame_width * 0.8
        seismo_paper_height = seismo_frame_height * 0.3
        seismo_paper = Rectangle(width=seismo_paper_width, height=seismo_paper_height, color=WHITE, fill_opacity=1)
        seismo_paper.move_to(seismo_frame.get_bottom() + UP * seismo_paper_height / 2 + LEFT * seismo_frame_width * 0.05)

        # Trace for the seismograph, tracking the pen's position
        seismo_trace = TracedPath(seismo_pen.get_center, stroke_color=RED, stroke_width=3)

        # --- Animations ---

        # Intro and Clock (approx 15 seconds)
        self.play(
        Create(clock_body),
        Create(clock_pendulum),
        run_time=2
        )
        self.wait(3) # Narration: "Simple pendulums aren't just for physics classrooms; they have practical applications!"

        self.play(
        angle_tracker_clock.animate.set_value(-PI/6),
        run_time=2,
        rate_func=there_and_back
        )
        self.play(
        angle_tracker_clock.animate.set_value(PI/6),
        run_time=2,
        rate_func=there_and_back
        )
        self.play(
        angle_tracker_clock.animate.set_value(-PI/6),
        run_time=2,
        rate_func=there_and_back
        )
        self.wait(1) # Narration: "From the rhythmic tick-tock of old grandfather clocks, where the pendulum's consistent period keeps time,"

        self.play(
        FadeIn(consistent_period_text),
        FadeIn(timekeeping_devices_text),
        run_time=1
        )
        self.wait(1) # Text appears, short pause.

        # Metronome (approx 11 seconds)
        self.play(
        Create(metronome_base),
        Create(metronome_rod),
        run_time=1.5
        )
        self.wait(2.5) # Narration: "to metronomes that help musicians keep tempo,"

        self.play(
        angle_tracker_metronome.animate.set_value(-PI/8),
        run_time=1.5,
        rate_func=there_and_back
        )
        self.play(
        angle_tracker_metronome.animate.set_value(PI/8),
        run_time=1.5,
        rate_func=there_and_back
        )
        self.wait(1) # Narration: "pendulums are everywhere."

        self.play(
        FadeIn(musical_tempo_text),
        run_time=1
        )
        self.wait(1) # Text appears, short pause.

        # Seismograph (approx 24 seconds)
        # Remove updaters for previous animations to prevent them from continuing
        clock_pendulum.remove_updater(update_clock_pendulum)
        metronome_rod.remove_updater(update_metronome_rod)

        self.play(
        Create(seismo_frame),
        Create(seismo_pendulum_group), # Add the group with its updater
        Create(seismo_paper),
        run_time=2
        )
        self.add(seismo_trace) # Add trace after creation, before motion
        self.wait(6) # Narration: "Even seismographs, which detect earthquakes, use a pendulum-like principle to measure ground motion."

        # Animate the paper moving and the frame shaking
        seismo_moving_parts = VGroup(seismo_frame, seismo_paper)

        # Simulate ground motion and pendulum lag
        self.play(
        seismo_moving_parts.animate.shift(LEFT * 0.3),
        seismo_angle_tracker.animate.set_value(0.1), # Pendulum swings slightly right relative to frame
        run_time=0.75,
        rate_func=there_and_back
        )
        self.play(
        seismo_moving_parts.animate.shift(RIGHT * 0.4),
        seismo_angle_tracker.animate.set_value(-0.1), # Pendulum swings slightly left relative to frame
        run_time=0.75,
        rate_func=there_and_back
        )
        self.play(
        seismo_moving_parts.animate.shift(LEFT * 0.2),
        seismo_angle_tracker.animate.set_value(0.05), # Pendulum swings slightly right relative to frame
        run_time=0.75,
        rate_func=there_and_back
        )
        self.wait(3.75) # Narration: "Understanding the simple pendulum lays the groundwork for more complex oscillatory systems."

        # Continue paper scrolling for a longer duration, with minimal shaking
        self.play(
        seismo_moving_parts.animate.shift(LEFT * 2), # Move paper and frame further left
        seismo_angle_tracker.animate.set_value(0), # Pendulum returns to vertical
        run_time=5,
        rate_func=linear
        )
        self.wait(1) # Narration: "It's a beautiful example of how fundamental physics principles govern the world around us."

        self.play(
        FadeIn(earthquake_detection_text),
        run_time=1
        )
        self.wait(3) # Narration: "Earthquake Detection" + "Keep observing, keep questioning, and keep exploring!"

        # Final cleanup for updaters
        seismo_pendulum_group.remove_updater(update_seismo_pendulum_group)

# Set narration and duration
Scene4.narration_text = '''Simple pendulums aren\'t just for physics classrooms; they have practical applications! From the rhythmic tick-tock of old grandfather clocks, where the pendulum\'s consistent period keeps time, to metronomes that help musicians keep tempo, pendulums are everywhere. Even seismographs, which detect earthquakes, use a pendulum-like principle to measure ground motion. Understanding the simple pendulum lays the groundwork for more complex oscillatory systems. It\'s a beautiful example of how fundamental physics principles govern the world around us. Keep observing, keep questioning, and keep exploring!'''
Scene4.audio_duration = 5.0
