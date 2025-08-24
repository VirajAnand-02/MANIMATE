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
        # Helper function to create a single pendulum at a given angle
        def create_single_pendulum(pivot_point, length, bob_radius, bob_color, current_angle_rad):
        # Calculate the end point of the string based on the angle
        string_end = pivot_point + rotate_vector(DOWN * length, current_angle_rad, axis=OUT)
        string = Line(pivot_point, string_end, stroke_width=2)
        bob = Circle(radius=bob_radius, color=bob_color, fill_opacity=1).move_to(string_end)
        return VGroup(string, bob)

        # --- Constants ---
        g = 9.81  # Acceleration due to gravity
        L_long = 2.0  # Length for longer pendulums
        L_short = 1.0  # Length for shorter pendulums
        R_bob_normal = 0.15  # Normal bob radius (visual representation of mass)
        R_bob_large = 0.25   # Larger bob radius (visual representation of larger mass)
        Max_angle_small = 15 * DEGREES  # Small amplitude for most experiments
        Max_angle_large = 30 * DEGREES  # Larger amplitude for visual distinction (not used for period comparison)

        # Calculate periods for reference
        T_long = 2 * PI * np.sqrt(L_long / g)
        T_short = 2 * PI * np.sqrt(L_short / g)

        # --- Define regions for the three side-by-side experiments ---
        exp_width = self.right_region.width / 3
        exp1_center = self.right_region.get_left() + RIGHT * exp_width / 2
        exp2_center = self.right_region.get_center()
        exp3_center = self.right_region.get_right() - RIGHT * exp_width / 0.95 # Adjusted for better spacing

        # Define a consistent Y-level for all pendulum pivots
        pivot_y_level = self.right_region.get_top()[1] - 0.5

        # Pivot points for Experiment 1 (Mass)
        pivot_exp1_left = exp1_center + LEFT * exp_width / 4
        pivot_exp1_right = exp1_center + RIGHT * exp_width / 4
        pivot_exp1_left[1] = pivot_y_level
        pivot_exp1_right[1] = pivot_y_level

        # Pivot points for Experiment 2 (Amplitude)
        pivot_exp2_left = exp2_center + LEFT * exp_width / 4
        pivot_exp2_right = exp2_center + RIGHT * exp_width / 4
        pivot_exp2_left[1] = pivot_y_level
        pivot_exp2_right[1] = pivot_y_level

        # Pivot points for Experiment 3 (Length)
        pivot_exp3_left = exp3_center + LEFT * exp_width / 4
        pivot_exp3_right = exp3_center + RIGHT * exp_width / 4
        pivot_exp3_left[1] = pivot_y_level
        pivot_exp3_right[1] = pivot_y_level

        # --- Title Text ---
        title_text = self.create_textbox(
        "Pendulum Characteristics: Amplitude, Period, Length, and Gravity",
        width=self.left_region.width * 0.9,
        height=self.left_region.height * 0.8
        ).move_to(self.left_region.get_center())
        self.play(FadeIn(title_text))
        self.wait(1)

        # --- Experiment 1: Mass doesn't affect period ---
        # Two pendulums: same length, same amplitude, different masses
        exp1_tracker = ValueTracker(0) # Tracks the phase of the swing
        pendulum1_exp1 = always_redraw(
        lambda: create_single_pendulum(pivot_exp1_left, L_long, R_bob_normal, RED, Max_angle_small * np.sin(exp1_tracker.get_value()))
        )
        pendulum2_exp1 = always_redraw(
        lambda: create_single_pendulum(pivot_exp1_right, L_long, R_bob_large, BLUE, Max_angle_small * np.sin(exp1_tracker.get_value()))
        )
        exp1_label = self.create_textbox(
        "Mass doesn't affect period!",
        width=exp_width * 0.9,
        height=0.5
        ).next_to(exp1_center, DOWN, buff=0.5)

        self.play(
        Create(pendulum1_exp1),
        Create(pendulum2_exp1),
        Write(exp1_label)
        )
        # Animate for 3 periods of the long pendulum
        self.play(exp1_tracker.animate.set_value(2 * PI * 3), run_time=T_long * 3, rate_func=linear)
        self.wait(0.5)
        self.play(
        FadeOut(pendulum1_exp1),
        FadeOut(pendulum2_exp1),
        FadeOut(exp1_label)
        )

        # --- Experiment 2: Amplitude (small angles) doesn't affect period ---
        # Two pendulums: same length, same mass, different small amplitudes
        exp2_tracker = ValueTracker(0)
        pendulum1_exp2 = always_redraw(
        lambda: create_single_pendulum(pivot_exp2_left, L_long, R_bob_normal, RED, Max_angle_small * np.sin(exp2_tracker.get_value()))
        )
        pendulum2_exp2 = always_redraw(
        lambda: create_single_pendulum(pivot_exp2_right, L_long, R_bob_normal, BLUE, (Max_angle_small / 2) * np.sin(exp2_tracker.get_value()))
        )
        exp2_label = self.create_textbox(
        "Amplitude (small angles) doesn't affect period!",
        width=exp_width * 0.9,
        height=0.5
        ).next_to(exp2_center, DOWN, buff=0.5)

        self.play(
        Create(pendulum1_exp2),
        Create(pendulum2_exp2),
        Write(exp2_label)
        )
        # Animate for 3 periods of the long pendulum
        self.play(exp2_tracker.animate.set_value(2 * PI * 3), run_time=T_long * 3, rate_func=linear)
        self.wait(0.5)
        self.play(
        FadeOut(pendulum1_exp2),
        FadeOut(pendulum2_exp2),
        FadeOut(exp2_label)
        )

        # --- Experiment 3: Length *does* affect period ---
        # Two pendulums: same mass, same small amplitude, different lengths
        exp3_tracker = ValueTracker(0)
        # Pendulum 1 (long)
        pendulum1_exp3 = always_redraw(
        lambda: create_single_pendulum(pivot_exp3_left, L_long, R_bob_normal, RED, Max_angle_small * np.sin(exp3_tracker.get_value()))
        )
        # Pendulum 2 (short) - its phase needs to be scaled to reflect its shorter period
        pendulum2_exp3 = always_redraw(
        lambda: create_single_pendulum(pivot_exp3_right, L_short, R_bob_normal, BLUE, Max_angle_small * np.sin(exp3_tracker.get_value() * (T_long / T_short)))
        )
        exp3_label = self.create_textbox(
        "Length *does* affect period!",
        width=exp_width * 0.9,
        height=0.5
        ).next_to(exp3_center, DOWN, buff=0.5)

        self.play(
        Create(pendulum1_exp3),
        Create(pendulum2_exp3),
        Write(exp3_label)
        )
        # Animate for 3 periods of the long pendulum. The short pendulum will complete more cycles.
        self.play(exp3_tracker.animate.set_value(2 * PI * 3), run_time=T_long * 3, rate_func=linear)
        self.wait(0.5)
        self.play(
        FadeOut(pendulum1_exp3),
        FadeOut(pendulum2_exp3),
        FadeOut(exp3_label)
        )

        self.wait(1) # Final wait

# Set narration and duration
Scene3.narration_text = '''Two important characteristics define a pendulum\'s swing: its \'amplitude\' – the maximum displacement from equilibrium – and its \'period\' – the time it takes for one complete back-and-forth swing. Interestingly, for small angles of swing, the period of a simple pendulum depends mainly on two things: the \'length\' of the string and the \'acceleration due to gravity\'. It does *not* depend on the mass of the bob, nor on the amplitude of the swing! A longer string means a longer period, while a shorter string results in a faster swing.'''
Scene3.audio_duration = 5.0
