```python
from manim import *
import numpy as np

class Scene3(Scene):
    def construct(self):
        # --- Constants and Initial Setup ---
        pivot_point = UP * 3
        string_length = 3
        max_swing_angle = 45 * DEGREES # Max displacement from vertical
        # Period duration chosen for animation clarity, not physical accuracy for a simple pendulum
        period_duration = 4.0 

        # Pendulum Mobjects
        pivot = Dot(pivot_point, color=WHITE)
        
        # ValueTracker for the angle of the pendulum from the vertical
        # 0 means vertical, positive is right, negative is left
        # This will be updated either directly or via an oscillation phase tracker
        pendulum_angle_tracker = ValueTracker(max_swing_angle)

        # Mobjects that depend on the pendulum_angle_tracker
        def get_bob_position():
            angle = pendulum_angle_tracker.get_value()
            x = pivot_point[0] + string_length * np.sin(angle)
            y = pivot_point[1] - string_length * np.cos(angle)
            return np.array([x, y, 0])

        def get_string():
            return Line(pivot_point, get_bob_position(), color=WHITE)

        def get_bob():
            return Circle(radius=0.2, color=RED, fill_opacity=1).move_to(get_bob_position())

        string = always_redraw(get_string)
        bob = always_redraw(get_bob)

        # Equilibrium line for reference
        equilibrium_line = Line(pivot_point, pivot_point + DOWN * string_length, color=GRAY, stroke_opacity=0.5)

        self.add(pivot, equilibrium_line, string, bob)

        # --- Introduction Text ---
        intro_text = Text("To understand pendulums better, we use three key terms:", font_size=36)
        terms_text = Text("Amplitude, Period, and Frequency.", font_size=40, color=YELLOW)
        VGroup(intro_text, terms_text).arrange(DOWN, buff=0.5).to_edge(UP)
        
        self.play(Write(intro_text))
        self.play(Write(terms_text))
        self.wait(1)
        self.play(FadeOut(intro_text), FadeOut(terms_text))

        # --- Amplitude ---
        amplitude_title = Text("'Amplitude'", font_size=48, color=BLUE).to_edge(UP)
        amplitude_def = Text("Maximum displacement or angle from equilibrium.", font_size=32).next_to(amplitude_title, DOWN)
        
        self.play(Write(amplitude_title))
        self.play(Write(amplitude_def))
        self.wait(0.5)

        # Ensure pendulum is at max_swing_angle for amplitude illustration
        self.play(pendulum_angle_tracker.animate.set_value(max_swing_angle), run_time=1)
        self.wait(0.5)

        # Arc and Angle for Amplitude
        arc_amplitude = always_redraw(
            lambda: Arc(
                start_angle= -90 * DEGREES, # Vertical down
                angle=pendulum_angle_tracker.get_value(),
                radius=0.8,
                arc_center=pivot_point,
                color=BLUE
            )
        )
        angle_label = always_redraw(
            lambda: MathTex(r"\theta_{max}", font_size=30)
            .next_to(arc_amplitude, RIGHT, buff=0.1)
            .shift(0.2 * UP)
        )

        self.play(Create(arc_amplitude), Write(angle_label))
        self.wait(2)
        
        self.play(FadeOut(amplitude_title, amplitude_def, arc_amplitude, angle_label))

        # --- Period ---
        period_title = Text("'Period'", font_size=48, color=GREEN).to_edge(UP)
        period_symbol = MathTex("T", font_size=60, color=GREEN).next_to(period_title, RIGHT, buff=0.2)
        period_def = Text("Time for one complete back-and-forth swing.", font_size=32).next_to(period_title, DOWN)

        self.play(Write(period_title), Write(period_symbol))
        self.play(Write(period_def))
        self.wait(0.5)

        # Timer for Period
        period_timer_tracker = ValueTracker(0)
        period_timer_label = Text("T = ", font_size=36).to_corner(DR).shift(LEFT*2)
        period_timer_display = always_redraw(
            lambda: DecimalNumber(
                period_timer_tracker.get_value(),
                num_decimal_places=2,
                font_size=36
            ).next_to(period_timer_label, RIGHT, buff=0.1)
        )
        period_timer_unit = Text(" s", font_size=36).next_to(period_timer_display, RIGHT, buff=0.1)
        period_timer_group = VGroup(period_timer_label, period_timer_display, period_timer_unit)
        
        self.play(FadeIn(period_timer_group))

        # ValueTracker for the oscillation phase (0 to 2*PI for one full cycle)
        oscillation_phase_tracker = ValueTracker(0) 

        # Updater for the pendulum_angle_tracker based on oscillation_phase_tracker
        # This makes the pendulum swing according to a cosine wave
        pendulum_angle_tracker.add_updater(
            lambda m: m.set_value(max_swing_angle * np.cos(oscillation_phase_tracker.get_value()))
        )

        # Animate one full swing (phase from 0 to 2*PI) and update the timer
        self.play(
            oscillation_phase_tracker.animate.set_value(2 * PI), # One full cycle
            period_timer_tracker.animate.set_value(period_duration),
            run_time=period_duration,
            rate_func=linear # Linear rate for the phase and timer
        )
        self.wait(1)
        
        # Remove updater to stop continuous motion of the pendulum
        pendulum_angle_tracker.remove_updater()
        self.play(FadeOut(period_title, period_symbol, period_def, period_timer_group))

        # --- Frequency ---
        frequency_title = Text("'Frequency'", font_size=48, color=ORANGE).to_edge(UP)
        frequency_symbol = MathTex("f", font_size=60, color=ORANGE).next_to(frequency_title, RIGHT, buff=0.2)
        frequency_def = Text("Number of complete oscillations per unit of time.", font_size=32).next_to(frequency_title, DOWN)
        
        self.play(Write(frequency_title), Write(frequency_symbol))
        self.play(Write(frequency_def))
        self.wait(0.5)

        # Frequency counter and timer
        oscillation_counter_tracker = ValueTracker(0)
        oscillation_counter_label = Text("Oscillations: ", font_size=36).to_corner(DL).shift(RIGHT*2)
        oscillation_counter_display = always_redraw(
            lambda: DecimalNumber(
                oscillation_counter_tracker.get_value(),
                num_decimal_places=0,
                font_size=36
            ).next_to(oscillation_counter_label, RIGHT, buff=0.1)
        )
        
        frequency_time_tracker = ValueTracker(0)
        frequency_time_label = Text("Time: ", font_size=36).next_to(oscillation_counter_label, UP, buff=0.5)
        frequency_time_display = always_redraw(
            lambda: DecimalNumber(
                frequency_time_tracker.get_value(),
                num_decimal_places=1,
                font_size=36
            ).next_to(frequency_time_label, RIGHT, buff=0.1)
        )
        frequency_time_unit = Text(" s", font_size=36).next_to(frequency_time_display, RIGHT, buff=0.1)
        frequency_time_group = VGroup(frequency_time_label, frequency_time_display, frequency_time_unit)
        
        frequency_formula = MathTex(r"f = \frac{1}{T}", font_size=60, color=ORANGE).next_to(frequency_time_group, UP, buff=1)

        self.play(FadeIn(oscillation_counter_label, oscillation_counter_display, frequency_time_group))
        self.play(Write(frequency_formula))

        # Animate multiple swings for frequency
        num_swings = 3
        total_frequency_time = num_swings * period_duration

        # Re-add the updater for pendulum angle to make it swing again
        pendulum_angle_tracker.add_updater(
            lambda m: m.set_value(max_swing_angle * np.cos(oscillation_phase_tracker.get_value()))
        )

        # Reset phase tracker for new animation
        oscillation_phase_tracker.set_value(0) 
        
        # Animate the phase tracker and time tracker, and update oscillation counter at the end
        self.play(
            oscillation_phase_tracker.animate.set_value(num_swings * 2 * PI), # Multiple full cycles
            frequency_time_tracker.animate.set_value(total_frequency_time),
            run_time=total_frequency_time,
            rate_func=linear
        )
        
        # Update oscillation counter to its final value
        self.play(
            oscillation_counter_tracker.animate.set_value(num_swings),
            run_time=0.5 # Quick update
        )
        self.wait(1)

        # Clean up
        self.play(
            FadeOut(frequency_title, frequency_symbol, frequency_def,
                    oscillation_counter_label, oscillation_counter_display,
                    frequency_time_group, frequency_formula)
        )
        self.wait(1)
        
        # Final fade out of pendulum
        self.play(FadeOut(pivot, equilibrium_line, string, bob))
        self.wait(0.5)
```