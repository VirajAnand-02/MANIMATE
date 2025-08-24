import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
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
        "Exploring Basic Geometry Shapes",
        self.title_region.width * 0.9,
        self.title_region.height * 0.8
        )
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(10) # Narration: "Welcome, curious minds... Look around you – shapes are everywhere!"

        # Transition: Fade out title
        self.play(FadeOut(title_text))
        self.wait(1)

        # 2. Animate lines forming into simple 2D shapes (square, circle, triangle)
        square = Square(side_length=1.5, color=BLUE)
        circle = Circle(radius=0.75, color=GREEN)
        triangle = Triangle(color=RED).scale(0.8) # Scale to be visually comparable

        # Arrange shapes in the main region
        shapes_2d_group = VGroup(square, circle, triangle).arrange(RIGHT, buff=1.5)
        shapes_2d_group.move_to(self.main_region.get_center())

        self.play(Create(square), run_time=1.5)
        self.play(Create(circle), run_time=1.5)
        self.play(Create(triangle), run_time=1.5)
        self.wait(3) # Narration: "From the screen you're watching this on... building blocks of our visual world."

        # 3. Morphing into outlines of real-world objects
        # Window outline (from Square)
        window_frame = Rectangle(width=2, height=2, color=BLUE)
        h_line = Line(window_frame.get_left(), window_frame.get_right())
        v_line = Line(window_frame.get_top(), window_frame.get_bottom())
        window_outline = VGroup(window_frame, h_line, v_line).move_to(square.get_center())

        # Coin outline (from Circle)
        coin_outline_main = Circle(radius=0.75, color=GREEN, stroke_width=5)
        coin_outline_detail = Circle(radius=0.6, color=GREEN, stroke_width=2)
        coin_mobject = VGroup(coin_outline_main, coin_outline_detail).move_to(circle.get_center())

        # Pizza Slice outline (from Triangle)
        pizza_slice_center_point = triangle.get_center() + DOWN * 0.2
        pizza_slice_radius = 0.8
        pizza_slice_start_angle = PI/2 - PI/4
        pizza_slice_angle = PI/2
        pizza_arc = Arc(
        radius=pizza_slice_radius,
        start_angle=pizza_slice_start_angle,
        angle=pizza_slice_angle,
        arc_center=pizza_slice_center_point,
        color=RED
        )
        pizza_line1 = Line(pizza_slice_center_point, pizza_arc.get_start(), color=RED)
        pizza_line2 = Line(pizza_slice_center_point, pizza_arc.get_end(), color=RED)
        pizza_slice_outline = VGroup(pizza_arc, pizza_line1, pizza_line2)
        pizza_slice_outline.move_to(triangle.get_center())

        # Perform transformations
        self.play(Transform(square, window_outline), run_time=1.5)
        self.wait(1)
        self.play(Transform(circle, coin_mobject), run_time=1.5)
        self.wait(1)
        self.play(Transform(triangle, pizza_slice_outline), run_time=1.5)
        self.wait(5) # Narration: "Today, we're going to uncover some of the most basic... understand the space around us."

        # 4. Text '2D Shapes: Flat' and '3D Shapes: Solid' appear
        # Fade out the morphed objects
        self.play(FadeOut(window_outline, coin_mobject, pizza_slice_outline))

        text_2d_label = Text("2D Shapes: Flat", font_size=48, color=YELLOW)
        text_3d_label = Text("3D Shapes: Solid", font_size=48, color=ORANGE)
        text_group = VGroup(text_2d_label, text_3d_label).arrange(DOWN, buff=1.0)
        text_group.move_to(self.main_region.get_center())

        self.play(Write(text_2d_label))
        self.wait(2)
        self.play(Write(text_3d_label))
        self.wait(7) # Narration: "Let's start by understanding the difference... Get ready to spot shapes like never before!"

# Set narration and duration
Scene1.narration_text = '''Welcome, curious minds, to the fascinating world of geometry! Geometry is all about shapes, sizes, positions, and properties of objects. Look around you – shapes are everywhere! From the screen you\'re watching this on to the ball you play with, shapes form the building blocks of our visual world. Today, we\'re going to uncover some of the most basic and fundamental shapes that help us understand the space around us. Let\'s start by understanding the difference between flat shapes, called 2D shapes, and solid shapes, which are 3D shapes. Get ready to spot shapes like never before!'''
Scene1.audio_duration = 5.0
