import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene3(TitleAndMainContent):
    def construct_scene(self):
        ```python
                title_text = self.create_textbox("Pendulum Motion and Gravity", self.title_region.width, self.title_region.height)
                title_text.move_to(self.title_region.get_center())

                pendulum = Circle(radius=0.5).move_to(DOWN * 2)
                string = Line(UP, pendulum.get_center(), stroke_width=2)
                bob = Dot(pendulum.get_center(), radius=0.15, color=RED)
                pendulum_group = VGroup(string, pendulum, bob).move_to(LEFT * 3)

                pivot = Dot(string.get_start(), color=BLUE)

                gravity_arrow = Arrow(pendulum.get_center(), pendulum.get_center() + DOWN, color=YELLOW, buff=0)
                gravity_label = MathTex("mg").next_to(gravity_arrow, RIGHT)

                def update_pendulum(mob, angle):
                    new_pendulum = Circle(radius=0.5)
                    new_bob_pos = new_pendulum.get_center() + np.array([np.sin(angle), -np.cos(angle), 0]) * 2
                    new_string = Line(UP, new_bob_pos, stroke_width=2)
                    new_bob = Dot(new_bob_pos, radius=0.15, color=RED)
                    new_pendulum_group = VGroup(new_string, new_pendulum, new_bob).move_to(LEFT * 3)
                    mob.become(new_pendulum_group)
                    return mob

                def get_restoring_force_arrow(angle):
                    restoring_force_direction = np.array([-np.sin(angle), 0, 0])
                    restoring_force_arrow = Arrow(pendulum_group[2].get_center(), pendulum_group[2].get_center() + restoring_force_direction, color=GREEN, buff=0)
                    restoring_force_label = MathTex("-mg \\sin(\\theta)").next_to(restoring_force_arrow, LEFT)
                    return VGroup(restoring_force_arrow, restoring_force_label)

                angle = ValueTracker(0)
                pendulum_group.add_updater(lambda mob: update_pendulum(mob, angle.get_value()))

                restoring_force_group = always_redraw(lambda: get_restoring_force_arrow(angle.get_value()))

                self.play(Create(pivot), Create(pendulum_group), Write(gravity_label), Create(gravity_arrow))
                self.wait(0.5)

                self.play(angle.animate.set_value(PI / 4), run_time=2)
                self.play(Create(restoring_force_group))
                self.wait(0.5)
                self.play(angle.animate.set_value(-PI / 4), run_time=4)
                self.wait(0.5)
                self.play(angle.animate.set_value(0), run_time=4)
                self.wait(1)
                self.play(FadeOut(restoring_force_group))
                self.play(angle.animate.set_value(0), run_time=1)
                self.wait(1)
                self.play(FadeOut(pendulum_group, gravity_arrow, gravity_label, pivot))
                self.add(title_text)
                self.wait(1)
        ```

# Set narration and duration
Scene3.narration_text = '''The pendulum\'s motion is governed by gravity. When displaced from its resting position, gravity pulls the bob back towards equilibrium. This creates a restoring force that causes the pendulum to oscillate or swing back and forth.'''
Scene3.audio_duration = 5.0
