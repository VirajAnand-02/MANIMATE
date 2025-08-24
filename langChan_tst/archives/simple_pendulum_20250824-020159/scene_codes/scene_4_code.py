import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Title
                title = self.create_textbox("Calculating the Period", width=self.title_region.width, height=self.title_region.height)
                title.move_to(self.title_region.get_center())
                self.play(Write(title))
                self.wait(1)

                # Formula
                formula = MathTex(r"T = 2\pi\sqrt{\frac{L}{g}}")
                formula.move_to(UP * 2)
                self.play(Write(formula))

                T_label = MathTex("T", "=", r"2\pi\sqrt{\frac{L}{g}}").move_to(LEFT * 5 + UP * 2)
                L_label = MathTex("L").move_to(RIGHT * 0.5 + DOWN * 0.5 + UP * 2)
                g_label = MathTex("g").move_to(RIGHT * 1.5 + DOWN * 1.5 + UP * 2)

                self.play(TransformMatchingTex(formula, T_label))
                self.play(Write(L_label))
                self.play(Write(g_label))

                self.wait(1)

                # Calculation
                calculation = MathTex(r"T = 2\pi\sqrt{\frac{1}{9.8}} \approx 2 \text{ seconds}")
                calculation.move_to(DOWN * 1)
                self.play(Write(calculation))
                self.wait(1)

                # Pendulum and Timer
                pendulum = Line(UP, DOWN * 2)
                bob = Dot(DOWN * 2)
                pendulum_group = VGroup(pendulum, bob).move_to(LEFT * 4 + DOWN * 1)
                self.add(pendulum_group)

                timer = Text("2.0 s").move_to(RIGHT * 4 + DOWN * 1)
                self.play(Write(timer))

                def swing(obj, dt):
                    obj.rotate(0.1 * np.sin(self.time), about_point=pendulum.get_start())

                pendulum_group.add_updater(swing)

                self.wait(2)
                pendulum_group.remove_updater(swing)
                self.wait(1)

# Set narration and duration
Scene4.narration_text = '''We can actually calculate the period using a simple formula: T = 2π√(L/g), where T is the period, L is the length of the pendulum, and g is the acceleration due to gravity (approximately 9.8 m/s² on Earth). Let\'s try an example: if a pendulum is 1 meter long, its period would be about 2 seconds.'''
Scene4.audio_duration = 5.0
