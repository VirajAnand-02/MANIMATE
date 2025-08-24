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
        # Constants for pendulum
        string_length = self.left_region.height * 0.4
        bob_radius = 0.3
        max_angle = 45 * DEGREES  # Initial displacement angle

        # --- Left Side: Pendulum Animation ---
        # 1. Create Pendulum Components
        pivot = Dot(self.left_region.get_center() + UP * self.left_region.height / 2.5, radius=0.08, color=WHITE)

        # Initial position for the bob (displaced)
        initial_bob_center = pivot.get_center() + rotate_vector(DOWN * string_length, max_angle)
        bob = Circle(radius=bob_radius, color=BLUE_E, fill_opacity=1).move_to(initial_bob_center)

        string = Line(pivot.get_center(), bob.get_center(), color=GREY_B)

        pendulum = VGroup(string, bob)

        # 2. Equilibrium Position Line
        equilibrium_line = DashedLine(
        pivot.get_center(),
        pivot.get_center() + DOWN * string_length * 1.2,
        color=GREY_A,
        stroke_width=2
        )
        equilibrium_label = Text("Equilibrium Position", font_size=24, color=GREY_A).next_to(equilibrium_line, RIGHT, buff=0.2)

        # 3. Pendulum Swing Logic
        angle_tracker = ValueTracker(max_angle) # Start at max_angle (displaced)

        def update_pendulum(mobj):
        current_angle = angle_tracker.get_value()
        new_bob_center = pivot.get_center() + rotate_vector(DOWN * string_length, current_angle)
        mobj[0].put_start_and_end_on(pivot.get_center(), new_bob_center) # String
        mobj[1].move_to(new_bob_center) # Bob

        pendulum.add_updater(update_pendulum)

        # 4. Gravity Arrow
        gravity_arrow = Arrow(
        start=bob.get_center() + UP * bob_radius * 1.5,
        end=bob.get_center() + DOWN * bob_radius * 1.5,
        color=RED,
        buff=0,
        stroke_width=5,
        max_tip_length_to_length_ratio=0.25
        ).set_opacity(0) # Start invisible
        gravity_label = Text("Gravity", font_size=24, color=RED).next_to(gravity_arrow, DOWN, buff=0.1)
        gravity_group = VGroup(gravity_arrow, gravity_label)

        def update_gravity_arrow(mobj):
        # Update arrow position to follow the bob
        mobj[0].set_points_by_ends(
        bob.get_center() + UP * bob_radius * 1.5,
        bob.get_center() + DOWN * bob_radius * 1.5
        )
        mobj[1].next_to(mobj[0], DOWN, buff=0.1)

        gravity_group.add_updater(update_gravity_arrow)


        # --- Right Side: Text Definitions ---
        # Ensure text fits within the right region
        eq_pos_text = self.create_textbox(
        "Equilibrium Position: The resting position where the bob hangs vertically.",
        width=self.right_region.width * 0.9,
        height=self.right_region.height * 0.3
        ).to_edge(UP).shift(RIGHT * self.right_region.width / 2) # Position in right region, top

        oscillation_text = self.create_textbox(
        "Oscillation: The back-and-forth motion of the pendulum around its equilibrium.",
        width=self.right_region.width * 0.9,
        height=self.right_region.height * 0.3
        ).next_to(eq_pos_text, DOWN, buff=0.8) # Position below first text

        # --- Animation Sequence ---
        self.play(
        Create(pivot),
        Create(string),
        Create(bob),
        run_time=1
        )
        self.add(pendulum) # Add pendulum with updater

        # Show equilibrium line
        self.play(Create(equilibrium_line), Write(equilibrium_label))
        self.wait(0.5)

        # Start swinging the pendulum
        # The swing will be continuous, so we use a longer run_time
        # The narration is about 25 seconds. Let's make the swing last for a good portion of it.
        swing_duration = 15 # Total duration of the continuous swing

        # Animate the angle tracker to simulate swinging
        # We need to swing from max_angle to -max_angle and back
        # A simple way is to use a custom rate_func that goes back and forth
        def swing_rate_func(t):
        # t goes from 0 to 1. We want angle to go from max_angle to -max_angle and back.
        # Use a sine wave for smooth oscillation.
        # np.cos(t * PI) goes from 1 to -1 as t goes from 0 to 1.
        # So, max_angle * np.cos(t * PI) will swing from max_angle to -max_angle.
        # To make it swing back, we can use a longer cycle or chain animations.
        # For continuous swing, let's just animate the tracker value.
        # We'll use a loop or a longer animation with a custom rate_func.
        # For simplicity, let's animate the tracker to go back and forth multiple times.
        return np.cos(t * 2 * PI) # Goes from 1 to 1, completing a full cycle.

        # Initial swing to equilibrium and past
        self.play(
        angle_tracker.animate.set_value(-max_angle),
        run_time=2.5,
        rate_func=lambda t: smooth(t) # Smooth start
        )

        # Show Equilibrium Position text
        self.play(Write(eq_pos_text), run_time=2)
        self.wait(0.5)

        # Continuous swing while showing gravity arrow
        # The angle tracker will oscillate between max_angle and -max_angle
        # We need to make it swing for the rest of the narration.
        # Let's create a sequence of animations for the swing.

        # First swing back to positive max_angle
        self.play(
        angle_tracker.animate.set_value(max_angle),
        run_time=2.5,
        rate_func=smooth
        )

        # Show gravity arrow at max displacement (right side)
        self.play(FadeIn(gravity_group, shift=DOWN), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(gravity_group, shift=DOWN), run_time=1)

        # Swing to negative max_angle
        self.play(
        angle_tracker.animate.set_value(-max_angle),
        run_time=2.5,
        rate_func=smooth
        )

        # Show gravity arrow at max displacement (left side)
        self.play(FadeIn(gravity_group, shift=DOWN), run_time=1)
        self.wait(0.5)
        self.play(FadeOut(gravity_group, shift=DOWN), run_time=1)

        # Swing back to positive max_angle
        self.play(
        angle_tracker.animate.set_value(max_angle),
        run_time=2.5,
        rate_func=smooth
        )

        # Show Oscillation text
        self.play(Write(oscillation_text), run_time=2)
        self.wait(0.5)

        # Swing back to equilibrium and stop
        self.play(
        angle_tracker.animate.set_value(0),
        run_time=2,
        rate_func=smooth
        )
        self.wait(1)

        # Clean up updater
        pendulum.remove_updater(update_pendulum)
        gravity_group.remove_updater(update_gravity_arrow)

# Set narration and duration
Scene2.narration_text = '''Let\'s observe how it moves. The pendulum\'s journey begins from its \'equilibrium position\' – that\'s when the bob hangs straight down, perfectly still. When we pull the bob to one side and release it, gravity pulls it back towards equilibrium. But due to inertia, it swings past, reaching the opposite side before gravity pulls it back again. This continuous back-and-forth motion is called \'oscillation\'. The point where it momentarily stops before changing direction is its maximum displacement.'''
Scene2.audio_duration = 5.0
