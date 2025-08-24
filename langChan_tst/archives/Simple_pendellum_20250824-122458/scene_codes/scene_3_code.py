```python
from manim import *

class Pendulum(VGroup):
    def __init__(self, length, initial_angle=PI/6, g_tracker=None, pivot_point=ORIGIN, bob_color=BLUE, **kwargs):
        super().__init__(**kwargs)
        self.length = length
        self.pivot_point = pivot_point
        self.initial_angle = initial_angle  # Max displacement from vertical
        self.g_tracker = g_tracker if g_tracker is not None else ValueTracker(9.81)
        self.bob_color = bob_color

        # Create components in their initial (vertical) state
        # The string starts at ORIGIN and goes DOWN
        self.string = Line(ORIGIN, DOWN * self.length, stroke_width=2, color=WHITE)
        # The bob is at the end of the string
        self.bob = Circle(radius=0.2, fill_opacity=1, color=self.bob_color).move_to(DOWN * self.length)
        
        # Group string and bob. Position their top (which is ORIGIN for the VGroup) at the desired pivot_point.
        self.pendulum_arm = VGroup(self.string, self.bob).move_to(self.pivot_point, aligned_edge=UP)
        self.pivot_dot = Dot(self.pivot_point, radius=0.05, color=WHITE)

        self.add(self.pendulum_arm, self.pivot_dot)

        # Apply initial rotation to the arm around the pivot point
        self.pendulum_arm.rotate(initial_angle, about_point=self.pivot_point)

        self.time_tracker = ValueTracker(0)
        self.add_updater(self._update_pendulum)

    def _update_pendulum(self, mobject, dt):
        self.time_tracker.increment_value(dt)
        
        g = self.g_tracker.get_value()
        if g <= 0: g = 0.001 # Prevent division by zero or negative g
        
        # Calculate period and angular frequency based on current g
        period = 2 * PI * np.sqrt(self.length / g)
        angular_frequency = 2 * PI / period

        # Calculate current angular displacement from vertical using simple harmonic motion
        current_displacement_angle = self.initial_angle * np.cos(angular_frequency * self.time_tracker.get_value())

        # The pendulum arm is initially vertical (angle -PI/2).
        # We want its angle to be (-PI/2 + current_displacement_angle).
        target_absolute_angle = -PI/2 + current_displacement_angle

        # Calculate the difference in angle needed from its current orientation
        angle_diff = target_absolute_angle - mobject.pendulum_arm.get_angle()
        
        # Rotate the pendulum arm by this difference around its pivot point
        mobject.pendulum_arm.rotate(angle_diff, about_point=self.pivot_point)

    def stop_swinging(self):
        self.remove_updater(self._update_pendulum)

    def start_swinging(self):
        self.add_updater(self._update_pendulum)

    def reset_time(self):
        """Resets the internal time tracker, effectively resetting the phase of the swing."""
        self.time_tracker.set_value(0)


class GeneratedScene_3(Scene):
    def construct(self):
        # --- Constants ---
        G_EARTH = 9.81
        G_MOON = 1.62
        L_SHORT = 2.5
        L_LONG = 4.5
        INITIAL_ANGLE = PI / 6 # 30 degrees for small angle approximation

        # --- Shared Gravity Tracker ---
        # Both pendulums will use this tracker, allowing us to animate 'g'
        g_tracker = ValueTracker(G_EARTH)

        # --- Pendulums for Length Comparison ---
        pivot_left = LEFT * 4 + UP * 2
        pivot_right = RIGHT * 4 + UP * 2

        pendulum_short = Pendulum(L_SHORT, initial_angle=INITIAL_ANGLE, g_tracker=g_tracker, pivot_point=pivot_left, bob_color=YELLOW)
        pendulum_long = Pendulum(L_LONG, initial_angle=INITIAL_ANGLE, g_tracker=g_tracker, pivot_point=pivot_right, bob_color=RED)

        short_label = Text("Short String (L)", font_size=36).next_to(pendulum_short, DOWN, buff=0.5)
        long_label = Text("Long String (L)", font_size=36).next_to(pendulum_long, DOWN, buff=0.5)

        # Initial setup and start swinging
        self.play(
            Create(pendulum_short),
            Create(pendulum_long),
            Write(short_label),
            Write(long_label),
            run_time=3
        )
        self.wait(1) # Allow pendulums to start their first swing cycle

        # Observe length difference
        # Narration: "What makes a pendulum swing faster or slower? The period of a simple pendulum is primarily determined by two factors: the length of the string..."
        self.wait(10) 
        
        # Narration: "...The longer the string, the longer the period, meaning it swings slower."
        self.play(Indicate(long_label, scale_factor=1.2), run_time=2)
        self.wait(5)

        # --- Transition to Gravity Comparison ---
        earth_label = Text("Earth (g)", font_size=36).next_to(pendulum_long, DOWN, buff=0.5)
        
        self.play(
            FadeOut(pendulum_short),
            FadeOut(short_label),
            pendulum_long.animate.move_to(ORIGIN + UP * 2), # Move the long pendulum to center
            ReplacementTransform(long_label, earth_label), # Change label to Earth
            run_time=3
        )
        self.wait(1) # Let it settle and swing on Earth

        # Observe gravity difference
        # Narration: "...and the acceleration due to gravity."
        self.wait(3)

        moon_label = Text("Moon (g)", font_size=36).next_to(pendulum_long, DOWN, buff=0.5)
        
        # Narration: "On the other hand, if gravity were stronger, the pendulum would swing faster."
        # Animate g_tracker changing value, which will affect the pendulum's swing speed via its updater
        self.play(
            g_tracker.animate.set_value(G_MOON),
            pendulum_long.bob.animate.set_color(GREY), # Change bob color for Moon
            ReplacementTransform(earth_label, moon_label),
            run_time=5 # Slower transition to clearly show the change in 'g' and its effect
        )
        pendulum_long.reset_time() # Reset phase to ensure a smooth start with the new 'g'
        self.wait(5) # Observe slower swing on Moon

        # Narration: "Surprisingly, for small angles of swing, the mass of the bob does not affect its period! Also, the amplitude only significantly affects the period if the swing is very wide."
        self.wait(10) # Placeholder for this part of the narration, no explicit animation for mass/amplitude

        # --- Formula Display ---
        # Stop the pendulum for clarity before showing the formula
        pendulum_long.stop_swinging()
        self.play(
            FadeOut(pendulum_long),
            FadeOut(moon_label),
            run_time=2
        )

        formula = MathTex(r"T = 2\pi\sqrt{\frac{L}{g}}", font_size=96)
        
        # Narration: "This relationship is captured by the formula: T equals two pi times the square root of L over g."
        self.play(Write(formula), run_time=3)
        self.wait(1)
        
        # Highlight L as the narration mentions it
        self.play(Indicate(formula.get_part_by_tex("L"), scale_factor=1.2, color=YELLOW), run_time=2)
        self.wait(1)
        
        # Highlight g as the narration mentions it
        self.play(Indicate(formula.get_part_by_tex("g"), scale_factor=1.2, color=GREEN), run_time=2)
        self.wait(3) # Final wait
```