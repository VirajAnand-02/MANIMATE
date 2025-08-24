import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene2(TitleAndMainContent):
    def construct_scene(self):
        title = self.create_textbox("The Simple Pendulum", width=self.title_region.width, height=self.title_region.height)
                title.move_to(self.title_region.get_center())
                self.add(title)

                # Pendulum parameters
                length = 3
                bob_radius = 0.3
                amplitude = PI / 4  # 45 degrees

                # Create the fixed point
                fixed_point = Dot(point=[0, 2, 0], color=RED)
                self.main_region.add(fixed_point)

                # Create the bob
                bob = Dot(point=[length * np.sin(amplitude), 2 - length * np.cos(amplitude), 0], color=BLUE, radius=bob_radius)
                self.main_region.add(bob)

                # Create the string
                string = Line(start=fixed_point.get_center(), end=bob.get_center(), color=WHITE)
                self.main_region.add(string)

                # Create the gravity arrow
                gravity_arrow = Arrow(start=bob.get_center(), end=bob.get_center() + DOWN, color=YELLOW)
                self.main_region.add(gravity_arrow)

                # Add labels
                bob_label = Tex("Bob").next_to(bob, DOWN)
                string_label = Tex("String").next_to(string, LEFT)
                gravity_label = Tex("Gravity").next_to(gravity_arrow, RIGHT)

                self.main_region.add(bob_label, string_label, gravity_label)

                # Initial state
                self.play(Create(fixed_point), Create(bob), Create(string), Create(gravity_arrow), Write(bob_label), Write(string_label), Write(gravity_label))
                self.wait(1)

                # Swing the pendulum
                def update_pendulum(mob, angle):
                    new_x = length * np.sin(angle)
                    new_y = 2 - length * np.cos(angle)
                    mob.move_to([new_x, new_y, 0])
                    string.become(Line(start=fixed_point.get_center(), end=mob.get_center(), color=WHITE))
                    gravity_arrow.move_to(mob.get_center())

                bob.add_updater(lambda mob: update_pendulum(mob, amplitude * np.cos(self.time * 2)))

                self.play(bob.animate.move_to([length * np.sin(amplitude), 2 - length * np.cos(amplitude), 0]), run_time=3)
                self.wait(3)

                bob.remove_updater(bob.updater)

                # Highlight fixed point and string length
                fixed_point_highlight = Circle(radius=0.5, color=GREEN, stroke_width=5).move_to(fixed_point.get_center())
                length_line = Line(start=fixed_point.get_center(), end=[0, 2 - length, 0], color=GREEN, stroke_width=5)
                length_label = Tex("Length").next_to(length_line, LEFT)

                self.play(Create(fixed_point_highlight), Create(length_line), Write(length_label))
                self.wait(2)

# Set narration and duration
Scene2.narration_text = '''A simple pendulum is, well, simple! It consists of a mass, called a bob, suspended from a fixed point by a lightweight string or rod. We assume the string is massless and doesn\'t stretch. When pulled to the side and released, gravity pulls the bob back towards the center, causing it to swing back and forth.'''
Scene2.audio_duration = 5.0
