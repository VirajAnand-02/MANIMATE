import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
from manim import *
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
    LAYOUT_MANAGER_AVAILABLE = True
except ImportError:
    LAYOUT_MANAGER_AVAILABLE = False
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox(
        "Complex Number Multiplication: The Argand Plane",
        self.title_region.width,
        self.title_region.height
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(0.5)

        # 2. Animate the Argand Plane appearing
        # Define axes for the Argand Plane
        axes = Axes(
        x_range=[-5, 5, 1],
        y_range=[-5, 5, 1],
        x_length=self.main_region.width * 0.8,
        y_length=self.main_region.height * 0.8,
        axis_config={"color": GRAY, "stroke_width": 2},
        x_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
        y_axis_config={"numbers_to_include": np.arange(-4, 5, 1)},
        )
        axes.add_coordinates()

        # Label the axes
        x_label = axes.get_x_axis_label(Text("Real", font_size=24, color=WHITE)).next_to(axes.x_axis, RIGHT, buff=0.2)
        y_label = axes.get_y_axis_label(Text("Imaginary", font_size=24, color=WHITE)).next_to(axes.y_axis, UP, buff=0.2)
        axes_labels = VGroup(x_label, y_label)

        # Group axes and labels and position them in the main region
        argand_plane = VGroup(axes, axes_labels)
        argand_plane.move_to(self.main_region.get_center())

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # 3. Plot a sample complex number 'z1 = 3 + 4i'
        z1_coords = (3, 4)
        z1_point = Dot(point=axes.c2p(*z1_coords), color=YELLOW)
        z1_vector = Arrow(
        start=axes.c2p(0, 0),
        end=axes.c2p(*z1_coords),
        buff=0,
        color=BLUE,
        stroke_width=5,
        tip_length=0.2
        )
        z1_label = MathTex("z_1 = 3 + 4i", font_size=36, color=BLUE).next_to(z1_point, UP + RIGHT, buff=0.2)

        self.play(Create(z1_point))
        self.play(GrowArrow(z1_vector))
        self.play(Write(z1_label))
        self.wait(1)

        # 4. Highlight its magnitude (length of vector)
        magnitude_label = Text("Magnitude", font_size=28, color=BLUE).next_to(z1_vector.get_center(), RIGHT, buff=0.3)
        self.play(
        z1_vector.animate.set_stroke(width=8, color=YELLOW),
        FadeIn(magnitude_label, shift=UP)
        )
        self.wait(1.5)
        self.play(
        z1_vector.animate.set_stroke(width=5, color=BLUE),
        FadeOut(magnitude_label, shift=DOWN)
        )
        self.wait(0.5)

        # 5. Highlight its argument (angle from positive real axis)
        # Create a line along the positive real axis for the angle reference
        # Use a line from origin to a point on the positive x-axis
        positive_real_axis_ref = Line(axes.c2p(0, 0), axes.c2p(axes.x_range[1], 0), color=GRAY, stroke_width=2)

        # Create the angle arc
        angle_arc = Angle(
        positive_real_axis_ref,
        z1_vector,
        radius=0.7,
        color=GREEN,
        stroke_width=4,
        other_angle=False # Ensure it's the smaller angle
        )
        argument_label_math = MathTex("\\theta", font_size=36, color=GREEN).next_to(angle_arc, UP + LEFT, buff=0.1)
        argument_label_text = Text("Argument", font_size=28, color=GREEN).next_to(angle_arc, DOWN + RIGHT, buff=0.3)


        self.play(
        Create(angle_arc),
        Write(argument_label_math),
        FadeIn(argument_label_text, shift=DOWN)
        )
        self.wait(2)

        self.play(FadeOut(angle_arc, argument_label_math, argument_label_text))
        self.wait(1)

# Set narration and duration
Scene1.narration_text = '''Welcome to a visual exploration of complex number multiplication! Imagine a special plane, called the Argand Plane, where the horizontal axis is for real numbers and the vertical axis is for imaginary numbers. Any complex number, like \'z = a + bi\', can be represented as a point or a vector starting from the origin. This vector has two key properties: its length, called the magnitude, and its angle with the positive real axis, called the argument.'''
Scene1.audio_duration = 5.0