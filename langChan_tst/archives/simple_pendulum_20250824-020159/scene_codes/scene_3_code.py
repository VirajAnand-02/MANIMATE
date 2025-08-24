import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import SplitScreen

class Scene3(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Pendulum Period", width=6, height=1)
                title.move_to(self.title_region.get_center())

                # Left side: Animated pendulum swinging with timer
                pendulum_length = 3
                bob_radius = 0.2
                pivot_point = self.left_region.get_center() + UP * (self.left_region.height / 2 - bob_radius)
                bob_color = BLUE
                string_color = WHITE

                string = Line(pivot_point, pivot_point + DOWN * pendulum_length, color=string_color)
                bob = Circle(radius=bob_radius, color=bob_color, fill_opacity=1)
                bob.move_to(string.get_end())

                angle = ValueTracker(PI / 4)  # Initial angle
                bob.add_updater(lambda m: m.move_to(pivot_point + pendulum_length * np.array([np.sin(angle.get_value()), -np.cos(angle.get_value()), 0])))
                string.add_updater(lambda m: m.become(Line(pivot_point, bob.get_center(), color=string_color)))

                period = ValueTracker(0)
                timer_text = always_redraw(lambda: Text(f"Period: {period.get_value():.2f} s", font_size=24).move_to(self.left_region.get_center() + DOWN * (self.left_region.height / 2 - 0.5)))

                def pendulum_swing(angle_val, run_time):
                    self.play(angle.animate.set_value(angle_val), run_time=run_time)

                self.add(string, bob, timer_text)

                # Simulate pendulum swing and update timer
                swing_duration = 2  # Approximate swing duration
                self.play(angle.animate.set_value(-PI / 4), run_time=swing_duration)
                self.play(angle.animate.set_value(PI / 4), run_time=swing_duration)
                period.set_value(swing_duration * 2)
                self.wait(1)

                # Right side: Two pendulums with different lengths
                pendulum1_length = 2
                pendulum2_length = 4
                pivot_point_right = self.right_region.get_center() + UP * (self.right_region.height / 2 - bob_radius)
                offset = RIGHT * 2

                string1 = Line(pivot_point_right - offset, pivot_point_right - offset + DOWN * pendulum1_length, color=string_color)
                bob1 = Circle(radius=bob_radius, color=bob_color, fill_opacity=1)
                bob1.move_to(string1.get_end())

                string2 = Line(pivot_point_right + offset, pivot_point_right + offset + DOWN * pendulum2_length, color=string_color)
                bob2 = Circle(radius=bob_radius, color=bob_color, fill_opacity=1)
                bob2.move_to(string2.get_end())

                angle1 = PI / 4
                angle2 = PI / 4

                def swing_pendulum(string, bob, angle, length, run_time):
                    self.play(
                        Rotate(string, angle, about_point=string.get_start()),
                        Rotate(bob, angle, about_point=string.get_start()),
                        run_time=run_time
                    )

                period1_text = Text("Period: {:.2f} s".format(2 * np.pi * np.sqrt(pendulum1_length / 9.8)), font_size=20).next_to(bob1, DOWN)
                period2_text = Text("Period: {:.2f} s".format(2 * np.pi * np.sqrt(pendulum2_length / 9.8)), font_size=20).next_to(bob2, DOWN)

                self.add(string1, bob1, string2, bob2, period1_text, period2_text)

                swing_time1 = np.sqrt(pendulum1_length / 9.8)
                swing_time2 = np.sqrt(pendulum2_length / 9.8)

                self.play(
                    Rotate(string1, angle1, about_point=string1.get_start()),
                    Rotate(bob1, angle1, about_point=string1.get_start()),
                    Rotate(string2, angle2, about_point=string2.get_start()),
                    Rotate(bob2, angle2, about_point=string2.get_start()),
                    run_time=2
                )
                self.play(
                    Rotate(string1, -2 * angle1, about_point=string1.get_start()),
                    Rotate(bob1, -2 * angle1, about_point=string1.get_start()),
                    Rotate(string2, -2 * angle2, about_point=string2.get_start()),
                    Rotate(bob2, -2 * angle2, about_point=string2.get_start()),
                    run_time=2
                )
                self.play(
                    Rotate(string1, angle1, about_point=string1.get_start()),
                    Rotate(bob1, angle1, about_point=string1.get_start()),
                    Rotate(string2, angle2, about_point=string2.get_start()),
                    Rotate(bob2, angle2, about_point=string2.get_start()),
                    run_time=2
                )

                self.wait(1)

                # Two pendulums with different masses, same length
                bob3_radius = 0.2
                bob4_radius = 0.4
                bob3_color = GREEN
                bob4_color = RED

                string3 = Line(pivot_point_right - offset, pivot_point_right - offset + DOWN * pendulum1_length, color=string_color)
                bob3 = Circle(radius=bob3_radius, color=bob3_color, fill_opacity=1)
                bob3.move_to(string3.get_end())

                string4 = Line(pivot_point_right + offset, pivot_point_right + offset + DOWN * pendulum1_length, color=string_color)
                bob4 = Circle(radius=bob4_radius, color=bob4_color, fill_opacity=1)
                bob4.move_to(string4.get_end())

                period3_text = Text("Period: {:.2f} s".format(2 * np.pi * np.sqrt(pendulum1_length / 9.8)), font_size=20).next_to(bob3, DOWN)
                period4_text = Text("Period: {:.2f} s".format(2 * np.pi * np.sqrt(pendulum1_length / 9.8)), font_size=20).next_to(bob4, DOWN)

                self.play(Transform(string1, string3), Transform(bob1, bob3), Transform(period1_text, period3_text),
                          Transform(string2, string4), Transform(bob2, bob4), Transform(period2_text, period4_text))

                self.play(
                    Rotate(string3, angle1, about_point=string3.get_start()),
                    Rotate(bob3, angle1, about_point=string3.get_start()),
                    Rotate(string4, angle2, about_point=string4.get_start()),
                    Rotate(bob4, angle2, about_point=string4.get_start()),
                    run_time=2
                )
                self.play(
                    Rotate(string3, -2 * angle1, about_point=string3.get_start()),
                    Rotate(bob3, -2 * angle1, about_point=string3.get_start()),
                    Rotate(string4, -2 * angle2, about_point=string4.get_start()),
                    Rotate(bob4, -2 * angle2, about_point=string4.get_start()),
                    run_time=2
                )
                self.play(
                    Rotate(string3, angle1, about_point=string3.get_start()),
                    Rotate(bob3, angle1, about_point=string3.get_start()),
                    Rotate(string4, angle2, about_point=string4.get_start()),
                    Rotate(bob4, angle2, about_point=string4.get_start()),
                    run_time=2
                )

                self.wait(2)

# Set narration and duration
Scene3.narration_text = '''The time it takes for one complete swing – that is, from one side to the other and back again – is called the period. Interestingly, the period of a simple pendulum depends primarily on two things: the length of the pendulum and the acceleration due to gravity. The mass of the bob *doesn\'t* affect the period!'''
Scene3.audio_duration = 5.0
