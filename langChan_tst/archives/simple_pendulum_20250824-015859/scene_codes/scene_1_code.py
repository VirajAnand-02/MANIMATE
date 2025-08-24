import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        ```python
                title_text = self.create_textbox("The Simple Pendulum", self.title_region.width, self.title_region.height)
                title_text.move_to(self.title_region.get_center())

                bob_radius = 0.2
                string_length = 2
                pivot_point = np.array([0, 1, 0])
                bob_initial_position = pivot_point + np.array([0, -string_length, 0])

                bob = Circle(radius=bob_radius, color=BLUE, fill_opacity=1)
                bob.move_to(bob_initial_position)

                string = Line(pivot_point, bob_initial_position, color=WHITE)

                pivot_dot = Dot(pivot_point, color=RED)

                bob_label = Tex("Bob", color=BLUE).next_to(bob, DOWN)
                string_label = Tex("String", color=WHITE).next_to(string, LEFT)
                pivot_label = Tex("Pivot Point", color=RED).next_to(pivot_dot, UP)

                angle = Angle(
                    Line(pivot_point, pivot_point + RIGHT),
                    string,
                    radius=0.7,
                    color=YELLOW,
                )
                angle_label = MathTex(r"\theta", color=YELLOW).move_to(
                    angle.point_from_proportion(0.5) + 0.3 * RIGHT
                )

                self.main_region.add(bob, string, pivot_dot)
                self.main_region.add(bob_label, string_label, pivot_label, angle, angle_label)

                self.add(title_text)

                def update_pendulum(obj, alpha):
                    angle_radians = np.sin(alpha * PI) * 0.5  # Reduced amplitude for visual clarity
                    new_bob_position = pivot_point + np.array([string_length * np.sin(angle_radians), -string_length * np.cos(angle_radians), 0])
                    obj[0].move_to(new_bob_position)  # Bob
                    obj[1].become(Line(pivot_point, new_bob_position, color=WHITE))  # String
                    new_angle = Angle(
                        Line(pivot_point, pivot_point + RIGHT),
                        obj[1],
                        radius=0.7,
                        color=YELLOW,
                    )
                    obj[2].become(new_angle)
                    obj[3].move_to(
                        new_angle.point_from_proportion(0.5) + 0.3 * RIGHT
                    )

                animation_group = VGroup(bob, string, angle, angle_label)
                self.play(UpdateFromAlphaFunc(animation_group, update_pendulum), run_time=5, rate_func=smooth)

                self.wait(2)
        ```

# Set narration and duration
Scene1.narration_text = '''Welcome! Today, we\'re diving into the fascinating world of physics with a simple yet powerful tool: the simple pendulum. We\'ll explore its basic components, how it swings, and the factors that influence its motion.'''
Scene1.audio_duration = 5.0
