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

class Scene2(SplitScreen):
    def construct_scene(self):
        # Pendulum setup
        pivot = LEFT * 5
        bob_start = pivot + DOWN * 3
        bob = Dot(bob_start, radius=0.2, color=BLUE)
        string = Line(pivot, bob_start, color=WHITE)
        self.add(bob, string)

        def update_bob(mob, alpha):
        angle = np.sin(alpha * TAU) * 0.8  # Reduced amplitude for visual clarity
        new_pos = pivot + DOWN * 3 * np.cos(angle) + RIGHT * 3 * np.sin(angle)
        mob.move_to(new_pos)
        string.become(Line(pivot, new_pos, color=WHITE))

        # Initial swing
        self.play(UpdateFromAlphaFunc(bob, update_bob), run_time=2)

        # Equilibrium Position
        equilibrium_text = self.create_textbox("Equilibrium Position", self.right_region.width * 0.9, 0.5)
        equilibrium_text.move_to(self.right_region.get_top() + DOWN * 0.7)
        equilibrium_point = Dot(pivot + DOWN * 3, color=YELLOW, radius=0.1)
        self.add(equilibrium_point)
        self.play(Write(equilibrium_text))
        self.wait(1)

        # Displacement
        displacement_text = self.create_textbox("Displacement", self.right_region.width * 0.9, 0.5)
        displacement_text.move_to(equilibrium_text.get_bottom() + DOWN * 0.7)
        displacement_arrow = Arrow(pivot + DOWN * 3, bob.get_center(), color=GREEN)
        self.play(Create(displacement_arrow), Write(displacement_text))
        self.wait(1)

        # Oscillation
        oscillation_text = self.create_textbox("Oscillation", self.right_region.width * 0.9, 0.5)
        oscillation_text.move_to(displacement_text.get_bottom() + DOWN * 0.7)
        oscillation_arc = Arc(radius=3, start_angle=-0.8, angle=1.6, color=RED, arc_center=pivot)
        self.play(Create(oscillation_arc), Write(oscillation_text))
        self.wait(1)

        # Amplitude
        amplitude_text = self.create_textbox("Amplitude", self.right_region.width * 0.9, 0.5)
        amplitude_text.move_to(oscillation_text.get_bottom() + DOWN * 0.7)
        amplitude_arrow = Arrow(pivot + DOWN * 3, pivot + DOWN * 3 * np.cos(0.8) + RIGHT * 3 * np.sin(0.8), color=ORANGE)
        self.play(Create(amplitude_arrow), Write(amplitude_text))
        self.wait(1)

        # Period
        period_text = self.create_textbox("Period (seconds)", self.right_region.width * 0.9, 0.5)
        period_text.move_to(amplitude_text.get_bottom() + DOWN * 0.7)
        timer_icon = SVGMobject("assets/timer_icon.svg", fill_color=WHITE, stroke_color=WHITE, height=0.5)
        timer_icon.next_to(period_text, LEFT)

        period_tracker = ValueTracker(0)
        period_number = DecimalNumber(0, num_decimal_places=2).next_to(timer_icon, RIGHT)
        period_group = VGroup(timer_icon, period_number)
        period_group.move_to(period_text.get_center())

        period_number.add_updater(lambda m: m.set_value(period_tracker.get_value()))

        self.play(Write(period_text), Create(timer_icon))
        self.play(Create(period_number))

        self.play(period_tracker.animate.set_value(2), UpdateFromAlphaFunc(bob, update_bob), run_time=2)
        self.wait(1)

        # Frequency
        frequency_text = self.create_textbox("Frequency (Hertz)", self.right_region.width * 0.9, 0.5)
        frequency_text.move_to(period_text.get_bottom() + DOWN * 0.7)
        frequency_counter = Integer(0).next_to(frequency_text, LEFT)
        hertz_label = Text("Hz").next_to(frequency_counter, RIGHT)
        frequency_group = VGroup(frequency_counter, hertz_label)
        frequency_group.move_to(frequency_text.get_center())

        self.play(Write(frequency_text), Create(frequency_counter), Write(hertz_label))

        def update_frequency(mob):
        mob.set_value(int(period_tracker.get_value() / 2))

        frequency_counter.add_updater(update_frequency)

        self.play(period_tracker.animate.set_value(4), UpdateFromAlphaFunc(bob, update_bob), run_time=2)
        self.wait(1)

        self.play(FadeOut(equilibrium_text, displacement_text, oscillation_text, amplitude_text, period_text, timer_icon, period_number, frequency_text, frequency_counter, hertz_label, displacement_arrow, oscillation_arc, amplitude_arrow, equilibrium_point))
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''Let\'s break down the key terms. The lowest point of its swing is the \'equilibrium position.\' When it moves away, that\'s \'displacement.\' One complete back-and-forth swing is an \'oscillation.\' The maximum displacement from equilibrium is the \'amplitude.\' The time it takes for one complete oscillation is the \'period,\' measured in seconds. And the number of oscillations per second is its \'frequency,\' measured in Hertz. These concepts are crucial for understanding any rhythmic motion.'''
Scene2.audio_duration = 5.0
