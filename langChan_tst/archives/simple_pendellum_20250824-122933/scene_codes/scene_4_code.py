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
        # Helper function to create a pendulum mobject
        def create_pendulum_mobject(length, angle_tracker, pivot_point, mass_radius=0.3, mass_color=BLUE):
        pivot = Dot(pivot_point, radius=0.05, color=WHITE)
        string = Line(pivot.get_center(), pivot.get_center() + DOWN * length, color=WHITE)
        bob = Circle(radius=mass_radius, color=mass_color, fill_opacity=1)

        # Initial position based on angle_tracker
        angle = angle_tracker.get_value()
        bob_x = pivot_point[0] + length * np.sin(angle)
        bob_y = pivot_point[1] - length * np.cos(angle)
        initial_bob_pos = np.array([bob_x, bob_y, 0])
        bob.move_to(initial_bob_pos)
        string.put_start_and_end_on(pivot.get_center(), initial_bob_pos)

        pendulum_group = VGroup(pivot, string, bob)

        # Updater for string and bob position based on angle_tracker
        def update_pendulum_position(mobj):
        current_angle = angle_tracker.get_value()
        bob_x_updated = pivot_point[0] + length * np.sin(current_angle)
        bob_y_updated = pivot_point[1] - length * np.cos(current_angle)
        new_bob_pos = np.array([bob_x_updated, bob_y_updated, 0])
        mobj[2].move_to(new_bob_pos)  # Bob is the 3rd element
        mobj[1].put_start_and_end_on(pivot.get_center(), new_bob_pos)  # String is the 2nd element

        pendulum_group.add_updater(update_pendulum_position)
        return pendulum_group

        # Helper function to create a sequence of pendulum swings
        def create_swing_sequence(tracker, length, g, initial_angle, num_cycles=1):
        period = 2 * PI * np.sqrt(length / g)
        half_period = period / 2
        animations = []
        for _ in range(num_cycles):
        # Swing from initial_angle to -initial_angle
        animations.append(tracker.animate.set_value(-initial_angle).set_run_time(half_period))
        # Swing from -initial_angle back to initial_angle
        animations.append(tracker.animate.set_value(initial_angle).set_run_time(half_period))
        return Succession(*animations)

        # --- Title ---
        title = self.create_textbox("Factors Affecting Pendulum Period", width=self.left_region.width * 0.9)
        title.move_to(self.left_region.get_center() + UP * self.left_region.height * 0.4)
        self.play(Write(title))
        self.wait(0.5)

        # --- Split screen setup ---
        # Vertical line to split the right_region into two panels
        split_line = Line(self.right_region.get_top() + LEFT * self.right_region.width / 2,
        self.right_region.get_bottom() + LEFT * self.right_region.width / 2,
        color=GRAY)
        self.play(Create(split_line))

        # --- Left Panel: Length Effect ---
        left_panel_center = self.right_region.get_center() + LEFT * self.right_region.width / 4
        g_earth = 9.8
        initial_angle = PI / 6  # 30 degrees

        # Short pendulum
        length_short = 2.0
        angle_tracker_short = ValueTracker(initial_angle)
        pivot_short_pos = left_panel_center + UP * self.right_region.height * 0.3
        pendulum_short = create_pendulum_mobject(length_short, angle_tracker_short, pivot_short_pos, mass_color=RED)

        # Long pendulum
        length_long = 4.0
        angle_tracker_long = ValueTracker(initial_angle)
        pivot_long_pos = left_panel_center + UP * self.right_region.height * 0.3
        pendulum_long = create_pendulum_mobject(length_long, angle_tracker_long, pivot_long_pos, mass_color=BLUE)

        # Adjust positions slightly so they don't overlap
        pendulum_short.shift(LEFT * 1.5)
        pendulum_long.shift(RIGHT * 1.5)

        # Labels for length comparison
        label_short = Text("Short String", font_size=24).next_to(pendulum_short, DOWN)
        label_long = Text("Long String", font_size=24).next_to(pendulum_long, DOWN)

        self.play(
        FadeIn(pendulum_short, pendulum_long),
        Write(label_short),
        Write(label_long)
        )
        self.wait(0.5)

        # Swing them concurrently. The longer period will naturally make the long one swing slower.
        num_swings_length = 1  # One full cycle
        swing_short = create_swing_sequence(angle_tracker_short, length_short, g_earth, initial_angle, num_swings_length)
        swing_long = create_swing_sequence(angle_tracker_long, length_long, g_earth, initial_angle, num_swings_length)
        self.play(swing_short, swing_long)
        self.wait(0.5)

        # --- Right Panel: Mass Effect ---
        right_panel_center = self.right_region.get_center() + RIGHT * self.right_region.width / 4

        # Light pendulum (same length as heavy)
        length_mass = 3.0
        angle_tracker_light = ValueTracker(initial_angle)
        pivot_light_pos = right_panel_center + UP * self.right_region.height * 0.3
        pendulum_light = create_pendulum_mobject(length_mass, angle_tracker_light, pivot_light_pos, mass_radius=0.2, mass_color=WHITE)

        # Heavy pendulum (same length as light)
        angle_tracker_heavy = ValueTracker(initial_angle)
        pivot_heavy_pos = right_panel_center + UP * self.right_region.height * 0.3
        pendulum_heavy = create_pendulum_mobject(length_mass, angle_tracker_heavy, pivot_heavy_pos, mass_radius=0.4, mass_color=GRAY)

        # Adjust positions slightly
        pendulum_light.shift(LEFT * 1.5)
        pendulum_heavy.shift(RIGHT * 1.5)

        # Labels for mass comparison
        label_light = Text("Light Bob", font_size=24).next_to(pendulum_light, DOWN)
        label_heavy = Text("Heavy Bob", font_size=24).next_to(pendulum_heavy, DOWN)

        self.play(
        FadeIn(pendulum_light, pendulum_heavy),
        Write(label_light),
        Write(label_heavy)
        )
        self.wait(0.5)

        # Swing them. They should swing at the exact same rate.
        num_swings_mass = 1
        swing_light = create_swing_sequence(angle_tracker_light, length_mass, g_earth, initial_angle, num_swings_mass)
        swing_heavy = create_swing_sequence(angle_tracker_heavy, length_mass, g_earth, initial_angle, num_swings_mass)
        self.play(swing_light, swing_heavy)
        self.wait(0.5)

        # --- Transition to Gravity Effect ---
        self.play(
        FadeOut(pendulum_short, pendulum_long, label_short, label_long,
        pendulum_light, pendulum_heavy, label_light, label_heavy,
        split_line),
        FadeOut(title)  # Fade out title to make space for new text
        )
        self.wait(0.5)

        # Single pendulum for gravity comparison
        gravity_pendulum_length = 3.5
        gravity_initial_angle = PI / 6
        gravity_angle_tracker = ValueTracker(gravity_initial_angle)
        gravity_pivot_pos = self.right_region.get_center() + UP * self.right_region.height * 0.3
        gravity_pendulum = create_pendulum_mobject(gravity_pendulum_length, gravity_angle_tracker, gravity_pivot_pos, mass_color=GREEN)

        # Earth background
        earth_bg = Circle(radius=3, color=BLUE_E, fill_opacity=0.8)
        earth_land = Polygon(
        [-3.5, -0.5, 0], [-2.5, -1, 0], [-1.5, -0.2, 0],
        [-2.0, 0.8, 0], [-3.0, 0.5, 0],
        color=GREEN_E, fill_opacity=1
        )
        earth_group = VGroup(earth_bg, earth_land).scale(0.8).move_to(self.right_region.get_center() + LEFT * self.right_region.width / 4)
        earth_label = Text("Earth (g = 9.8 m/s²)", font_size=28).next_to(earth_group, DOWN)

        # Moon background
        moon_bg = Circle(radius=3, color=GRAY_B, fill_opacity=0.8)
        crater1 = Circle(radius=0.5, color=GRAY_D, fill_opacity=1).move_to(moon_bg.get_center() + UP * 0.8 + LEFT * 0.5)
        crater2 = Circle(radius=0.3, color=GRAY_D, fill_opacity=1).move_to(moon_bg.get_center() + DOWN * 0.7 + RIGHT * 0.8)
        moon_group = VGroup(moon_bg, crater1, crater2).scale(0.8).move_to(self.right_region.get_center() + RIGHT * self.right_region.width / 4)
        moon_label = Text("Moon (g = 1.62 m/s²)", font_size=28).next_to(moon_group, DOWN)

        # Position pendulum between Earth and Moon backgrounds
        gravity_pendulum.move_to(self.right_region.get_center() + UP * self.right_region.height * 0.3)

        self.play(
        FadeIn(earth_group, moon_group),
        Write(earth_label),
        Write(moon_label),
        FadeIn(gravity_pendulum)
        )
        self.wait(0.5)

        # Swing on Earth
        g_earth = 9.8
        earth_swing_anim = create_swing_sequence(gravity_angle_tracker, gravity_pendulum_length, g_earth, gravity_initial_angle, num_cycles=1)
        self.play(earth_swing_anim)
        self.wait(0.5)

        # Swing on Moon (slower due to lower gravity)
        g_moon = 1.62
        moon_swing_anim = create_swing_sequence(gravity_angle_tracker, gravity_pendulum_length, g_moon, gravity_initial_angle, num_cycles=1)
        self.play(moon_swing_anim)
        self.wait(0.5)

        # Final fade out
        self.play(
        FadeOut(gravity_pendulum, earth_group, moon_group, earth_label, moon_label)
        )
        self.wait(0.5)

# Set narration and duration
Scene4.narration_text = '''What factors affect a pendulum\'s period? Surprisingly, for small angles, the mass of the bob does not affect the period! A heavy bob and a light bob, with the same string length, will swing with the same period. The two main factors are the length of the string and the acceleration due to gravity. A longer string results in a longer period, meaning it swings slower. On the other hand, if gravity were stronger, the pendulum would swing faster, resulting in a shorter period. This is why a pendulum clock would run differently on the Moon than on Earth!'''
Scene4.audio_duration = 5.0
