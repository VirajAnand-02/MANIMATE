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
        # 1. Create the title text
        title = self.create_textbox("Pendulum Oscillation", width=self.left_region.width * 0.9, height=self.left_region.height * 0.15)
        title.move_to(self.left_region.get_center() + UP * self.left_region.height * 0.35)
        self.play(Write(title), run_time=1)

        # Pendulum parameters
        pivot_point = self.right_region.get_center() + UP * self.right_region.height * 0.3
        string_length = self.right_region.height * 0.4
        bob_radius = 0.3
        initial_angle = 45 * DEGREES # Max displacement angle

        # Mobjects: Pivot, String, Bob
        pivot = Dot(pivot_point, color=WHITE)
        string = Line(pivot_point, pivot_point + DOWN * string_length, color=WHITE)
        bob = Circle(radius=bob_radius, color=BLUE, fill_opacity=1).move_to(string.get_end())
        pendulum_group = VGroup(string, bob)

        # ValueTrackers for animation state
        angle_tracker = ValueTracker(0) # Current angle from vertical (radians)
        pe_tracker = ValueTracker(0)    # Potential Energy (normalized 0 to 1)
        ke_tracker = ValueTracker(0)    # Kinetic Energy (normalized 0 to 1)

        # Updater for the pendulum's position based on angle_tracker
        def update_pendulum(mobj):
        string_m, bob_m = mobj
        current_angle = angle_tracker.get_value()
        new_bob_pos = pivot_point + rotate_vector(DOWN * string_length, current_angle)
        string_m.put_start_and_end_on(pivot_point, new_bob_pos)
        bob_m.move_to(new_bob_pos)
        pendulum_group.add_updater(update_pendulum)

        # Energy Bars (Potential Energy and Kinetic Energy)
        bar_width = 0.5
        bar_max_height = self.right_region.height * 0.25

        pe_bar = Rectangle(width=bar_width, height=0.01, color=RED, fill_opacity=0.8)
        ke_bar = Rectangle(width=bar_width, height=0.01, color=GREEN, fill_opacity=0.8)

        pe_label = Text("PE", font_size=24, color=RED)
        ke_label = Text("KE", font_size=24, color=GREEN)

        # Position bars and labels
        VGroup(pe_bar, ke_bar).arrange(RIGHT, buff=1.5).move_to(self.right_region.get_center() + DOWN * self.right_region.height * 0.35)
        pe_label.next_to(pe_bar, DOWN, buff=0.1)
        ke_label.next_to(ke_bar, DOWN, buff=0.1)

        # Updaters for energy bar heights
        def update_pe_bar(mobj):
        mobj.set(height=pe_tracker.get_value() * bar_max_height)
        mobj.move_to(pe_bar.get_bottom(), aligned_edge=DOWN) # Keep bottom fixed
        pe_bar.add_updater(update_pe_bar)

        def update_ke_bar(mobj):
        mobj.set(height=ke_tracker.get_value() * bar_max_height)
        mobj.move_to(ke_bar.get_bottom(), aligned_edge=DOWN) # Keep bottom fixed
        ke_bar.add_updater(update_ke_bar)

        # Updater for PE/KE trackers based on pendulum angle
        max_height_diff = string_length * (1 - np.cos(initial_angle))
        def update_energy_trackers(dt):
        current_angle = angle_tracker.get_value()
        current_height_diff = string_length * (1 - np.cos(current_angle))
        pe_ratio = current_height_diff / max_height_diff
        ke_ratio = 1 - pe_ratio
        pe_tracker.set_value(pe_ratio)
        ke_tracker.set_value(ke_ratio)
        self.add_updater(update_energy_trackers)

        # Force Vectors (Gravity, Tension, Restoring Force)
        # Gravity (constant, downwards)
        gravity_arrow = always_redraw(
        lambda: Arrow(
        bob.get_center(),
        bob.get_center() + DOWN * 0.8,
        buff=0, color=YELLOW,
        max_stroke_width_to_length_ratio=0.1,
        max_tip_length_to_length_ratio=0.2
        ).set_opacity(1 if abs(angle_tracker.get_value()) > 0.01 else 0) # Hide when at equilibrium
        )

        # Tension (along the string, towards pivot)
        tension_arrow = always_redraw(
        lambda: Arrow(
        bob.get_center(),
        pivot_point,
        buff=0, color=PURPLE,
        max_stroke_width_to_length_ratio=0.1,
        max_tip_length_to_length_ratio=0.2
        ).set_opacity(1 if abs(angle_tracker.get_value()) > 0.01 else 0) # Hide when at equilibrium
        )

        # Net Restoring Force (tangential component of gravity)
        def get_restoring_force_arrow():
        current_angle = angle_tracker.get_value()
        if abs(current_angle) < 0.01: # Hide near equilibrium
        return Mobject()

        string_vec = bob.get_center() - pivot_point
        # Tangential direction: perpendicular to string, towards equilibrium
        tangent_direction = rotate_vector(string_vec, -PI/2 if current_angle > 0 else PI/2)
        # Magnitude proportional to sin(angle)
        force_magnitude = 0.8 * np.sin(abs(current_angle))

        return Arrow(
        bob.get_center(),
        bob.get_center() + normalize(tangent_direction) * force_magnitude,
        buff=0, color=ORANGE,
        max_stroke_width_to_length_ratio=0.1,
        max_tip_length_to_length_ratio=0.2
        )
        restoring_force_arrow = always_redraw(get_restoring_force_arrow)

        # Velocity Arrow (indicates direction of motion and speed)
        def get_velocity_arrow():
        current_angle = angle_tracker.get_value()
        if ke_tracker.get_value() < 0.01: # Hide when speed is zero
        return Mobject()

        string_vec = bob.get_center() - pivot_point
        # Direction is tangential to the arc
        # If angle > 0, moving left (counter-clockwise) -> rotate string_vec by PI/2
        # If angle < 0, moving right (clockwise) -> rotate string_vec by -PI/2
        tangent_direction = rotate_vector(string_vec, PI/2 if current_angle > 0 else -PI/2)

        # Scale magnitude by KE (speed)
        velocity_magnitude = 0.8 * ke_tracker.get_value()

        return Arrow(
        bob.get_center(),
        bob.get_center() + normalize(tangent_direction) * velocity_magnitude,
        buff=0, color=WHITE,
        max_stroke_width_to_length_ratio=0.1,
        max_tip_length_to_length_ratio=0.2
        )
        velocity_arrow = always_redraw(get_velocity_arrow)

        # Add initial mobjects to the scene
        self.add(pivot, pendulum_group, pe_bar, ke_bar, pe_label, ke_label)
        self.wait(0.5)

        # Animation Sequence
        # 2. Displace the pendulum to one side
        # Narration: "Once displaced from its equilibrium, the pendulum begins to swing."
        self.play(
        angle_tracker.animate.set_value(initial_angle),
        run_time=2
        )
        self.wait(2) # Wait for narration

        # 3. Overlay force vectors and velocity arrow
        self.play(
        FadeIn(gravity_arrow),
        FadeIn(tension_arrow),
        FadeIn(restoring_force_arrow),
        FadeIn(velocity_arrow),
        run_time=1.5
        )

        # 4. Pendulum swings down (Potential Energy converts to Kinetic Energy)
        # Narration: "Gravity pulls the bob downwards, but the string's tension keeps it moving along an arc. As it swings down, potential energy converts to kinetic energy, reaching maximum speed at the bottom."
        self.play(
        angle_tracker.animate.set_value(0),
        run_time=3,
        rate_func=ease_in_sine # Accelerate towards bottom
        )
        self.wait(1) # Wait at bottom for narration

        # 5. Pendulum swings upwards (Kinetic Energy converts back to Potential Energy)
        # Narration: "Then, it swings upwards, kinetic energy converting back to potential energy, slowing down until it momentarily stops at its highest point,"
        self.play(
        angle_tracker.animate.set_value(-initial_angle),
        run_time=3,
        rate_func=ease_out_sine # Decelerate towards peak
        )
        self.wait(1) # Wait at peak for narration

        # 6. Continuous back-and-forth motion (Oscillation)
        # Narration: "before gravity pulls it back down again. This continuous back-and-forth motion is called 'oscillation'."
        self.play(
        angle_tracker.animate.set_value(initial_angle),
        run_time=6,
        rate_func=there_and_back # Completes one full cycle: -initial -> 0 -> initial
        )

        # Remove updaters to stop the dynamic changes
        pendulum_group.remove_updater(update_pendulum)
        pe_bar.remove_updater(update_pe_bar)
        ke_bar.remove_updater(update_ke_bar)
        self.remove_updater(update_energy_trackers)

        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''Once displaced from its equilibrium, the pendulum begins to swing. Gravity pulls the bob downwards, but the string\'s tension keeps it moving along an arc. As it swings down, potential energy converts to kinetic energy, reaching maximum speed at the bottom. Then, it swings upwards, kinetic energy converting back to potential energy, slowing down until it momentarily stops at its highest point, before gravity pulls it back down again. This continuous back-and-forth motion is called \'oscillation\'.'''
Scene2.audio_duration = 5.0
