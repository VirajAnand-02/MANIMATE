import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import SplitScreen
import numpy as np

class Scene4(SplitScreen):
    def construct_scene(self):
        title = self.create_textbox("Mass Independence", width=6, height=1)
                title.move_to(self.left_region.get_center())

                # Pendulum parameters
                length = 3
                amplitude = 2
                damping_factor = 0.99

                # Heavier pendulum
                heavy_bob_radius = 0.3
                heavy_bob = Circle(radius=heavy_bob_radius, color=BLUE, fill_opacity=1)
                heavy_string = Line(start=UP * length, end=DOWN * heavy_bob_radius, color=WHITE)
                heavy_pendulum = VGroup(heavy_string, heavy_bob).move_to(LEFT * 2)
                heavy_pendulum.initial_angle = PI / 4
                heavy_pendulum.angle = heavy_pendulum.initial_angle

                def update_heavy_pendulum(pendulum, dt):
                    pendulum.angle = damping_factor * pendulum.initial_angle * np.cos(np.sqrt(9.8 / length) * self.time)
                    pendulum.become(
                        VGroup(
                            Line(start=UP * length, end=DOWN * heavy_bob_radius, color=WHITE),
                            Circle(radius=heavy_bob_radius, color=BLUE, fill_opacity=1)
                        ).move_to(LEFT * 2).rotate(pendulum.angle, about_point=UP * length + LEFT * 2)
                    )

                heavy_pendulum.add_updater(update_heavy_pendulum)

                # Lighter pendulum
                light_bob_radius = 0.2
                light_bob = Circle(radius=light_bob_radius, color=RED, fill_opacity=1)
                light_string = Line(start=UP * length, end=DOWN * light_bob_radius, color=WHITE)
                light_pendulum = VGroup(light_string, light_bob).move_to(RIGHT * 2)
                light_pendulum.initial_angle = PI / 4
                light_pendulum.angle = light_pendulum.initial_angle

                def update_light_pendulum(pendulum, dt):
                    pendulum.angle = damping_factor * pendulum.initial_angle * np.cos(np.sqrt(9.8 / length) * self.time)
                    pendulum.become(
                        VGroup(
                            Line(start=UP * length, end=DOWN * light_bob_radius, color=WHITE),
                            Circle(radius=light_bob_radius, color=RED, fill_opacity=1)
                        ).move_to(RIGHT * 2).rotate(pendulum.angle, about_point=UP * length + RIGHT * 2)
                    )

                light_pendulum.add_updater(update_light_pendulum)

                # Gravity arrows
                heavy_gravity_arrow = Arrow(
                    start=heavy_bob.get_center() + UP * heavy_bob_radius,
                    end=heavy_bob.get_center() + DOWN * 1,
                    color=YELLOW,
                    buff=0
                )
                light_gravity_arrow = Arrow(
                    start=light_bob.get_center() + UP * light_bob_radius,
                    end=light_bob.get_center() + DOWN * 0.7,
                    color=YELLOW,
                    buff=0
                )

                def update_heavy_gravity(arrow):
                    arrow.become(
                        Arrow(
                            start=heavy_pendulum[1].get_center() + UP * heavy_bob_radius,
                            end=heavy_pendulum[1].get_center() + DOWN * 1,
                            color=YELLOW,
                            buff=0
                        )
                    )

                def update_light_gravity(arrow):
                    arrow.become(
                        Arrow(
                            start=light_pendulum[1].get_center() + UP * light_bob_radius,
                            end=light_pendulum[1].get_center() + DOWN * 0.7,
                            color=YELLOW,
                            buff=0
                        )
                    )

                heavy_gravity_arrow.add_updater(update_heavy_gravity)
                light_gravity_arrow.add_updater(update_light_gravity)

                self.add(heavy_pendulum, light_pendulum, heavy_gravity_arrow, light_gravity_arrow)

                self.time = 0
                def update_time(dt):
                    self.time += dt

                self.add_updater(update_time)

                self.wait(8)

# Set narration and duration
Scene4.narration_text = '''Interestingly, the mass of the bob doesn\'t significantly affect the period! A heavier bob and a lighter bob, with the same length and under the same gravity, will swing with nearly the same period. This is because the increased inertia of the heavier bob is counteracted by the increased gravitational force acting on it.'''
Scene4.audio_duration = 5.0
