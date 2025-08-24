```python
from manim import *
import numpy as np

class Scene4(Scene):
    def construct(self):
        # --- Introduction Text ---
        intro_text = Text(
            "The predictable motion of pendulums makes them incredibly useful.",
            font_size=36,
            line_spacing=1.5,
            color=BLUE_A
        ).to_edge(UP)
        self.play(Write(intro_text))
        self.wait(1)

        # --- Grandfather Clock ---
        self.play(FadeOut(intro_text))
        self.show_grandfather_clock()

        # --- Metronome ---
        self.show_metronome()

        # --- Seismograph ---
        self.show_seismograph()

        # --- Recap ---
        self.show_recap()

    def create_pendulum_mobjects(self, pivot_point, rod_length=2, bob_radius=0.2, color=WHITE):
        """Helper to create the rod and bob mobjects for a pendulum."""
        rod = Line(pivot_point, pivot_point + DOWN * rod_length, color=color, stroke_width=3)
        bob = Circle(radius=bob_radius, color=color, fill_opacity=1).move_to(rod.get_end())
        return VGroup(rod, bob)

    def show_grandfather_clock(self):
        title = Text("Grandfather Clock", font_size=48, color=GOLD).to_edge(UP)
        self.play(FadeIn(title))

        # Clock body
        clock_body = Rectangle(width=2, height=5, color=BROWN, fill_opacity=0.8).shift(DOWN * 0.5)
        clock_top = Polygon(
            clock_body.get_corner(UL) + UP * 0.5,
            clock_body.get_center() + UP * 2.5,
            clock_body.get_corner(UR) + UP * 0.5,
            color=BROWN, fill_opacity=0.8
        ).align_to(clock_body, DOWN)
        clock_face = Circle(radius=0.7, color=LIGHT_GRAY, fill_opacity=1).move_to(clock_body.get_center() + UP * 1.5)
        hour_hand = Line(clock_face.get_center(), clock_face.get_center() + RIGHT * 0.3, stroke_width=4, color=BLACK)
        minute_hand = Line(clock_face.get_center(), clock_face.get_center() + UP * 0.5, stroke_width=4, color=BLACK)
        clock_hands = VGroup(hour_hand, minute_hand)
        clock_frame = VGroup(clock_body, clock_top, clock_face, clock_hands)

        # Pendulum for clock
        pivot_point = clock_body.get_center() + DOWN * 0.5
        
        # Create initial pendulum mobjects
        initial_pendulum = self.create_pendulum_mobjects(pivot_point, rod_length=1.5, bob_radius=0.15, color=GOLD)
        
        angle_tracker = ValueTracker(0)

        # Updater to rotate the pendulum group around its pivot
        def update_clock_pendulum(mobj):
            mobj.become(
                self.create_pendulum_mobjects(pivot_point, rod_length=1.5, bob_radius=0.15, color=GOLD)
            ).rotate(angle_tracker.get_value(), about_point=pivot_point)
        
        clock_pendulum = always_redraw(update_clock_pendulum)

        self.play(Create(clock_frame))
        self.add(clock_pendulum) # Add the always_redraw mobject

        # Animate the pendulum swinging
        self.play(
            angle_tracker.animate.set_value(20 * DEGREES),
            rate_func=linear,
            run_time=0.5
        )
        self.play(
            angle_tracker.animate.set_value(-20 * DEGREES),
            rate_func=there_and_back,
            run_time=4,
            rate_func_config={"num_cycles": 2} # 2 full cycles
        )
        self.play(
            angle_tracker.animate.set_value(0),
            rate_func=linear,
            run_time=0.5
        )

        self.wait(0.5)
        self.remove(clock_pendulum) # Remove the always_redraw mobject
        self.play(FadeOut(VGroup(title, clock_frame)))

    def show_metronome(self):
        title = Text("Metronome", font_size=48, color=GREEN_SCREEN).to_edge(UP)
        self.play(FadeIn(title))

        # Metronome body
        metronome_body = Rectangle(width=1.5, height=3, color=GRAY_BROWN, fill_opacity=0.8)
        metronome_screen = Rectangle(width=1.2, height=0.8, color=BLACK, fill_opacity=1).move_to(metronome_body.get_center() + UP * 0.8)
        
        bpm_value = ValueTracker(120)
        bpm_display = always_redraw(
            lambda: Text(f"{int(bpm_value.get_value())} BPM", font_size=30, color=GREEN_SCREEN).move_to(metronome_screen.get_center())
        )
        
        metronome_frame = VGroup(metronome_body, metronome_screen)

        # Metronome pendulum
        pivot_point = metronome_body.get_center() + UP * 1.2
        
        initial_pendulum = self.create_pendulum_mobjects(pivot_point, rod_length=1.5, bob_radius=0.1, color=SILVER)
        
        angle_tracker = ValueTracker(0)
        
        def update_metronome_pendulum(mobj):
            mobj.become(
                self.create_pendulum_mobjects(pivot_point, rod_length=1.5, bob_radius=0.1, color=SILVER)
            ).rotate(angle_tracker.get_value(), about_point=pivot_point)
        
        metronome_pendulum = always_redraw(update_metronome_pendulum)

        self.play(Create(metronome_frame))
        self.add(bpm_display, metronome_pendulum) # Add redrawable mobjects

        # Animate the pendulum swinging
        self.play(
            angle_tracker.animate.set_value(30 * DEGREES),
            rate_func=linear,
            run_time=0.5
        )
        self.play(
            angle_tracker.animate.set_value(-30 * DEGREES),
            rate_func=there_and_back,
            run_time=4,
            rate_func_config={"num_cycles": 2}
        )
        self.play(
            angle_tracker.animate.set_value(0),
            rate_func=linear,
            run_time=0.5
        )

        self.wait(0.5)
        self.remove(bpm_display, metronome_pendulum)
        self.play(FadeOut(VGroup(title, metronome_frame)))

    def show_seismograph(self):
        title = Text("Seismograph", font_size=48, color=ORANGE).to_edge(UP)
        self.play(FadeIn(title))

        # Seismograph components
        ground_base = Rectangle(width=6, height=1, color=GRAY_D, fill_opacity=1).shift(DOWN * 2)
        seismo_frame = Rectangle(width=1, height=2, color=GRAY_A, fill_opacity=0.8).next_to(ground_base, UP, buff=0).align_to(ground_base, LEFT)
        paper_roll = Rectangle(width=3, height=1.5, color=WHITE, fill_opacity=1).next_to(seismo_frame, RIGHT, buff=0.5)
        
        # Pendulum (rod and bob)
        pivot_point_initial = seismo_frame.get_center() + UP * 0.8
        rod_length = 1.5
        bob_radius = 0.15
        
        pendulum_rod = Line(pivot_point_initial, pivot_point_initial + DOWN * rod_length, color=GOLD, stroke_width=3)
        pendulum_bob = Circle(radius=bob_radius, color=GOLD, fill_opacity=1).move_to(pendulum_rod.get_end())
        
        # Pen arm
        pen_arm = Line(pendulum_bob.get_center(), paper_roll.get_left() + UP * 0.5, color=BLACK, stroke_width=2)
        pen_tip = Dot(pen_arm.get_end(), radius=0.05, color=RED)

        # Group all static parts that move with the ground
        movable_group = VGroup(ground_base, seismo_frame, paper_roll)
        
        # The seismic path will be drawn
        seismic_path = VMobject(stroke_width=2, color=RED)
        
        # Add initial mobjects to scene
        self.add(movable_group, pendulum_rod, pendulum_bob, pen_arm, pen_tip, seismic_path)

        # ValueTracker for ground movement
        ground_offset_tracker = ValueTracker(0)

        # Updater for the seismograph components
        # This function will be called every frame to update positions
        def update_seismograph_components(dt):
            current_offset = ground_offset_tracker.get_value()
            
            # Move the entire ground/frame/paper system
            movable_group.move_to(ORIGIN + DOWN * 0.5 + RIGHT * current_offset)
            
            # Recalculate current pivot point based on moved frame
            current_pivot_abs = movable_group[1].get_center() + UP * 0.8
            
            # The bob's absolute X position should be less affected by ground motion (inertia)
            # Let's say the bob moves only 20% of the ground's movement
            initial_bob_x_on_screen = pivot_point_initial[0] # The initial x-coord of the bob if it were perfectly vertical
            initial_bob_y_on_screen = pivot_point_initial[1] - rod_length
            
            new_bob_abs_x = initial_bob_x_on_screen + current_offset * 0.2
            new_bob_abs_y = initial_bob_y_on_screen # Keep y constant for simplicity
            
            # Update pendulum rod and bob
            pendulum_rod.put_start_and_end_on(current_pivot_abs, np.array([new_bob_abs_x, new_bob_abs_y, 0]))
            pendulum_bob.move_to(pendulum_rod.get_end())
            
            # Update pen arm and tip
            pen_arm.put_start_and_end_on(pendulum_bob.get_center(), movable_group[2].get_left() + UP * 0.5)
            pen_tip.move_to(pen_arm.get_end())

            # Update seismic path
            seismic_path.add_points_as_corners([pen_tip.get_center()])

        # Add the updater to the scene
        self.add_updater(update_seismograph_components)

        # Animate ground shaking
        self.play(
            ground_offset_tracker.animate.set_value(1),
            rate_func=there_and_back,
            run_time=1,
            rate_func_config={"num_cycles": 2}
        )
        self.play(
            ground_offset_tracker.animate.set_value(-1),
            rate_func=there_and_back,
            run_time=1,
            rate_func_config={"num_cycles": 2}
        )
        self.play(
            ground_offset_tracker.animate.set_value(0),
            rate_func=linear,
            run_time=0.5
        )
        
        self.remove_updater(update_seismograph_components) # Remove the updater after animation
        self.play(FadeOut(VGroup(title, movable_group, pendulum_rod, pendulum_bob, pen_arm, pen_tip, seismic_path)))

    def show_recap(self):
        # Final gently swinging pendulum
        final_pendulum_pivot = ORIGIN + UP * 2
        
        initial_final_pendulum = self.create_pendulum_mobjects(final_pendulum_pivot, rod_length=2, bob_radius=0.2, color=BLUE)
        
        angle_tracker = ValueTracker(0)
        
        def update_final_pendulum(mobj):
            mobj.become(
                self.create_pendulum_mobjects(final_pendulum_pivot, rod_length=2, bob_radius=0.2, color=BLUE)
            ).rotate(angle_tracker.get_value(), about_point=final_pendulum_pivot)
        
        final_pendulum = always_redraw(update_final_pendulum)
        self.add(final_pendulum)

        # Start swinging
        self.play(
            angle_tracker.animate.set_value(15 * DEGREES),
            rate_func=linear,
            run_time=0.5
        )
        self.play(
            angle_tracker.animate.set_value(-15 * DEGREES),
            rate_func=there_and_back,
            run_time=3, # Longer swing for background
            rate_func_config={"num_cycles": 1.5} # 1.5 cycles
        )
        
        # Key terms
        terms = VGroup(
            Text("Period", font_size=48, color=YELLOW),
            Text("Amplitude", font_size=48, color=ORANGE),
            Text("Length", font_size=48, color=GREEN),
            Text("Gravity", font_size=48, color=RED)
        ).arrange(DOWN, buff=0.8).next_to(final_pendulum, LEFT, buff=2)

        self.play(Write(terms[0]))
        self.wait(0.5)
        self.play(Write(terms[1]))
        self.wait(0.5)
        self.play(Write(terms[2]))
        self.wait(0.5)
        self.play(Write(terms[3]))
        self.wait(1)

        # Final text
        final_text = Text(
            "Understanding the simple pendulum gives us insight into oscillatory motion, a fundamental concept in physics that's all around us. So next time you see something swinging, remember the fascinating science at play!",
            font_size=30,
            line_spacing=1.5,
            color=BLUE_A
        ).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(3)

        self.remove(final_pendulum) # Remove the always_redraw mobject
        self.play(FadeOut(VGroup(terms, final_text)))

```