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

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text
        title_text = self.create_textbox(
        "Practical Applications of Pendulums",
        self.title_region.width * 0.9,
        self.title_region.height * 0.8
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # 2. Grandfather Clock Pendulum
        # Create a frame for the clock
        clock_frame = Rectangle(
        width=self.main_region.width * 0.3,
        height=self.main_region.height * 0.8,
        color=BROWN,
        fill_opacity=0.2
        )
        clock_frame.move_to(self.main_region.get_center())

        # Pendulum components
        pivot_point_clock = clock_frame.get_top() + DOWN * 0.5
        rod_clock = Line(pivot_point_clock, pivot_point_clock + DOWN * 2, stroke_width=4, color=GRAY)
        bob_clock = Circle(radius=0.3, color=GOLD, fill_opacity=1).move_to(rod_clock.get_end())
        pendulum_clock = VGroup(rod_clock, bob_clock)

        # Initial rotation for the swing
        initial_angle_clock = 20 * DEGREES
        pendulum_clock.rotate(-initial_angle_clock, about_point=pivot_point_clock, axis=OUT)

        self.play(FadeIn(clock_frame))
        self.play(Create(pendulum_clock))

        # Pendulum swing animation using ValueTracker and updater
        angle_tracker_clock = ValueTracker(initial_angle_clock)
        pendulum_clock.add_updater(
        lambda m: m.become(
        VGroup(
        Line(pivot_point_clock, pivot_point_clock + DOWN * 2, stroke_width=4, color=GRAY),
        Circle(radius=0.3, color=GOLD, fill_opacity=1).move_to(pivot_point_clock + DOWN * 2)
        ).rotate(-angle_tracker_clock.get_value(), about_point=pivot_point_clock, axis=OUT)
        )
        )

        self.play(
        angle_tracker_clock.animate.set_value(-initial_angle_clock),
        rate_func=there_and_back_with_pause,
        run_time=1.5
        )
        self.play(
        angle_tracker_clock.animate.set_value(initial_angle_clock),
        rate_func=there_and_back_with_pause,
        run_time=1.5
        )
        self.play(
        angle_tracker_clock.animate.set_value(-initial_angle_clock),
        rate_func=there_and_back_with_pause,
        run_time=1.5
        )
        self.wait(0.5)
        pendulum_clock.remove_updater(pendulum_clock.updaters[0]) # Remove updater to stop animation
        self.play(FadeOut(pendulum_clock, clock_frame))

        # 3. Metronome
        metronome_base = Triangle(color=RED_B, fill_opacity=0.8).set_height(self.main_region.height * 0.3)
        metronome_base.move_to(self.main_region.get_center() + DOWN * (self.main_region.height * 0.2))

        pivot_point_metronome = metronome_base.get_top() + UP * 0.1
        rod_metronome = Line(pivot_point_metronome, pivot_point_metronome + DOWN * 1.5, stroke_width=3, color=LIGHT_GRAY)
        bob_metronome = Polygon(
        [0, 0.2, 0], [0.2, 0, 0], [0, -0.2, 0], [-0.2, 0, 0],
        color=BLUE_E, fill_opacity=1
        ).scale(0.5).move_to(rod_metronome.get_end())
        pendulum_metronome = VGroup(rod_metronome, bob_metronome)

        initial_angle_metronome = 30 * DEGREES
        pendulum_metronome.rotate(-initial_angle_metronome, about_point=pivot_point_metronome, axis=OUT)

        self.play(FadeIn(metronome_base))
        self.play(Create(pendulum_metronome))

        angle_tracker_metronome = ValueTracker(initial_angle_metronome)
        pendulum_metronome.add_updater(
        lambda m: m.become(
        VGroup(
        Line(pivot_point_metronome, pivot_point_metronome + DOWN * 1.5, stroke_width=3, color=LIGHT_GRAY),
        Polygon(
        [0, 0.2, 0], [0.2, 0, 0], [0, -0.2, 0], [-0.2, 0, 0],
        color=BLUE_E, fill_opacity=1
        ).scale(0.5).move_to(pivot_point_metronome + DOWN * 1.5)
        ).rotate(-angle_tracker_metronome.get_value(), about_point=pivot_point_metronome, axis=OUT)
        )
        )

        self.play(
        angle_tracker_metronome.animate.set_value(-initial_angle_metronome),
        rate_func=there_and_back_with_pause,
        run_time=1
        )
        self.play(
        angle_tracker_metronome.animate.set_value(initial_angle_metronome),
        rate_func=there_and_back_with_pause,
        run_time=1
        )
        self.play(
        angle_tracker_metronome.animate.set_value(-initial_angle_metronome),
        rate_func=there_and_back_with_pause,
        run_time=1
        )
        self.wait(0.5)
        pendulum_metronome.remove_updater(pendulum_metronome.updaters[0])
        self.play(FadeOut(pendulum_metronome, metronome_base))

        # 4. Seismograph
        seismograph_base = Rectangle(
        width=self.main_region.width * 0.7,
        height=self.main_region.height * 0.2,
        color=GRAY_B,
        fill_opacity=0.7
        ).move_to(self.main_region.get_center() + DOWN * (self.main_region.height * 0.3))

        # Pendulum (fixed in space due to inertia)
        seismo_pivot = seismograph_base.get_top() + UP * 1.5
        seismo_rod = Line(seismo_pivot, seismo_pivot + DOWN * 1.5, stroke_width=3, color=WHITE)
        seismo_bob = Circle(radius=0.4, color=RED_E, fill_opacity=1).move_to(seismo_rod.get_end())
        seismo_pendulum = VGroup(seismo_rod, seismo_bob)

        # Pen and its fixed tip
        seismo_pen_end_fixed = seismo_bob.get_right() + RIGHT * 1.5
        seismo_pen = Line(seismo_bob.get_right(), seismo_pen_end_fixed, stroke_width=2, color=BLUE)
        seismo_pen_tip = Dot(seismo_pen_end_fixed, radius=0.01, color=BLACK) # A tiny dot at the pen tip

        # Drum (simplified as a rectangle)
        drum_width = self.main_region.width * 0.4
        drum_height = self.main_region.height * 0.3
        seismo_drum = Rectangle(
        width=drum_width,
        height=drum_height,
        color=WHITE,
        fill_opacity=1
        ).next_to(seismograph_base, RIGHT, buff=0.5)

        # TracedPath to draw the movement of the pen tip relative to the moving drum
        seismo_trace = TracedPath(seismo_pen_tip.get_center, stroke_width=2, color=BLACK)

        # Initial setup
        self.play(FadeIn(seismograph_base, seismo_pendulum, seismo_drum, seismo_pen, seismo_pen_tip))
        self.add(seismo_trace) # Add the trace to the scene

        # Animate base shaking and drum moving under the fixed pen tip
        shake_amplitude = 0.3
        shake_duration = 0.5

        self.play(
        seismograph_base.animate.shift(LEFT * shake_amplitude),
        seismo_drum.animate.shift(LEFT * shake_amplitude),
        run_time=shake_duration,
        rate_func=linear
        )
        self.play(
        seismograph_base.animate.shift(RIGHT * shake_amplitude * 2),
        seismo_drum.animate.shift(RIGHT * shake_amplitude * 2),
        run_time=shake_duration * 2,
        rate_func=linear
        )
        self.play(
        seismograph_base.animate.shift(LEFT * shake_amplitude * 2),
        seismo_drum.animate.shift(LEFT * shake_amplitude * 2),
        run_time=shake_duration * 2,
        rate_func=linear
        )
        self.play(
        seismograph_base.animate.shift(RIGHT * shake_amplitude),
        seismo_drum.animate.shift(RIGHT * shake_amplitude),
        run_time=shake_duration,
        rate_func=linear
        )
        self.wait(0.5)
        self.remove(seismo_trace, seismo_pen_tip) # Remove the trace and the helper dot
        self.play(FadeOut(seismograph_base, seismo_pendulum, seismo_drum, seismo_pen))

        # 5. Foucault Pendulum
        # Long pendulum base (straight down)
        foucault_pivot = self.main_region.get_top() + UP * 0.5 # High pivot point
        foucault_rod_length = self.main_region.height * 0.8
        foucault_pendulum_base = VGroup(
        Line(foucault_pivot, foucault_pivot + DOWN * foucault_rod_length, stroke_width=2, color=WHITE),
        Sphere(radius=0.2, color=BLUE_E, resolution=(10, 10)).move_to(foucault_pivot + DOWN * foucault_rod_length)
        )

        # Pegs on the floor
        peg_radius = self.main_region.width * 0.3
        num_pegs = 12
        pegs = VGroup(*[
        Dot(
        foucault_pivot + DOWN * foucault_rod_length + RIGHT * peg_radius * np.cos(angle) + UP * peg_radius * np.sin(angle),
        radius=0.05,
        color=ORANGE
        )
        for angle in np.linspace(0, 2 * PI, num_pegs, endpoint=False)
        ])
        pegs.move_to(foucault_pivot + DOWN * foucault_rod_length) # Center the pegs at the bob's lowest point

        # ValueTrackers for swing angle and plane rotation
        initial_swing_angle = 15 * DEGREES
        plane_rotation_tracker = ValueTracker(0) # Angle of the swing plane around the vertical axis (Z-axis in 2D)
        swing_angle_tracker = ValueTracker(initial_swing_angle) # Angle of the swing within its plane

        # The actual pendulum mobject, dynamically redrawn
        swing_mobject = always_redraw(
        lambda: foucault_pendulum_base.copy()
        .rotate(plane_rotation_tracker.get_value(), axis=OUT, about_point=foucault_pivot) # Rotate the plane
        .rotate(-swing_angle_tracker.get_value(), axis=OUT, about_point=foucault_pivot) # Swing within the plane
        )

        self.play(Create(swing_mobject))
        self.play(Create(pegs))

        # First swing
        self.play(
        swing_angle_tracker.animate.set_value(-initial_swing_angle),
        rate_func=there_and_back,
        run_time=2
        )

        # Rotate the plane and knock a peg
        self.play(
        plane_rotation_tracker.animate.increment_value(30 * DEGREES), # Rotate the plane by 30 degrees
        FadeOut(pegs[0], shift=DOWN*0.2),
        run_time=1
        )
        self.wait(0.5)

        # Second swing
        self.play(
        swing_angle_tracker.animate.set_value(initial_swing_angle),
        rate_func=there_and_back,
        run_time=2
        )

        # Rotate again and knock another peg
        self.play(
        plane_rotation_tracker.animate.increment_value(30 * DEGREES),
        FadeOut(pegs[1], shift=DOWN*0.2),
        run_time=1
        )
        self.wait(0.5)

        # Third swing
        self.play(
        swing_angle_tracker.animate.set_value(-initial_swing_angle),
        rate_func=there_and_back,
        run_time=2
        )

        self.wait(1)
        self.remove(swing_mobject) # Remove the always_redraw mobject
        self.play(FadeOut(pegs))

        self.play(FadeOut(title_text))
        self.wait(0.5)

# Set narration and duration
Scene5.narration_text = '''Simple pendulums are more than just physics demonstrations; they have practical applications all around us. They are the heart of grandfather clocks, providing a regular oscillation to keep accurate time. Metronomes, used by musicians, rely on a pendulum to set a steady tempo. Even earthquake sensors, known as seismographs, use principles of pendulums to detect ground motion. And for a truly grand example, the Foucault pendulum demonstrates the Earth\'s rotation! From precise timing to scientific discovery, the simple pendulum continues to be a fascinating and useful invention.'''
Scene5.audio_duration = 5.0
