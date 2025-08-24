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
        # 1. Create the title text
        title = self.create_textbox("2D Shapes", self.title_region.width * 0.8, self.title_region.height * 0.8)
        title.move_to(self.title_region.get_center())
        self.play(FadeIn(title))
        self.wait(0.5)

        # Initial setup for left and right content
        # These will hold the current shape and example for transformations
        current_left_shape = Mobject()
        current_right_example = Mobject()

        # Define common animation durations for better pacing
        draw_time = 1.5
        highlight_time = 1.0
        transform_time = 1.5

        # --- Triangle ---
        # Left side: Animated drawing of Triangle
        triangle_shape = Triangle(color=BLUE, fill_opacity=0.8).set_height(self.left_region.height * 0.6)
        triangle_shape.move_to(self.left_region)

        # Right side: Real-world example (Pizza Slice)
        pizza_slice_shape = Triangle(color=ORANGE, fill_opacity=0.7).set_height(self.right_region.height * 0.4)
        pizza_slice_text = Text("Pizza Slice", font_size=30, color=WHITE).next_to(pizza_slice_shape, DOWN)
        pizza_slice_example = VGroup(pizza_slice_shape, pizza_slice_text).move_to(self.right_region)

        self.play(Create(triangle_shape, run_time=draw_time), FadeIn(pizza_slice_example, run_time=draw_time))
        current_left_shape = triangle_shape
        current_right_example = pizza_slice_example

        # Highlight sides
        sides = triangle_shape.get_lines()
        self.play(LaggedStart(*[Indicate(side, scale_factor=1.2, color=YELLOW) for side in sides], lag_ratio=0.3, run_time=highlight_time))

        # Highlight vertices
        vertices = VGroup(*[Dot(v, radius=0.08, color=YELLOW) for v in triangle_shape.get_vertices()])
        self.play(LaggedStart(*[Flash(v, flash_radius=0.3, line_length=0.2, color=YELLOW) for v in vertices], lag_ratio=0.3, run_time=highlight_time))
        self.wait(0.5)

        # --- Square ---
        # Left side: Animated drawing of Square
        square_shape = Square(color=GREEN, fill_opacity=0.8).set_height(self.left_region.height * 0.6)
        square_shape.move_to(self.left_region)

        # Right side: Real-world example (Window)
        window_shape = Square(color=LIGHT_GRAY, fill_opacity=0.7).set_height(self.right_region.height * 0.4)
        window_text = Text("Window", font_size=30, color=WHITE).next_to(window_shape, DOWN)
        window_example = VGroup(window_shape, window_text).move_to(self.right_region)

        self.play(
        Transform(current_left_shape, square_shape, run_time=transform_time),
        Transform(current_right_example, window_example, run_time=transform_time)
        )
        current_left_shape = square_shape
        current_right_example = window_example

        # Highlight sides
        sides = square_shape.get_lines()
        self.play(LaggedStart(*[Indicate(side, scale_factor=1.2, color=YELLOW) for side in sides], lag_ratio=0.3, run_time=highlight_time))

        # Highlight vertices
        vertices = VGroup(*[Dot(v, radius=0.08, color=YELLOW) for v in square_shape.get_vertices()])
        self.play(LaggedStart(*[Flash(v, flash_radius=0.3, line_length=0.2, color=YELLOW) for v in vertices], lag_ratio=0.3, run_time=highlight_time))
        self.wait(0.5)

        # --- Rectangle ---
        # Left side: Animated drawing of Rectangle
        rectangle_shape = Rectangle(color=RED, fill_opacity=0.8, width=self.left_region.width * 0.5, height=self.left_region.height * 0.4)
        rectangle_shape.move_to(self.left_region)

        # Right side: Real-world example (Door)
        door_shape = Rectangle(color=BROWN, fill_opacity=0.7, width=self.right_region.width * 0.3, height=self.right_region.height * 0.5)
        door_text = Text("Door", font_size=30, color=WHITE).next_to(door_shape, DOWN)
        door_example = VGroup(door_shape, door_text).move_to(self.right_region)

        self.play(
        Transform(current_left_shape, rectangle_shape, run_time=transform_time),
        Transform(current_right_example, door_example, run_time=transform_time)
        )
        current_left_shape = rectangle_shape
        current_right_example = door_example

        # Highlight sides
        sides = rectangle_shape.get_lines()
        self.play(LaggedStart(*[Indicate(side, scale_factor=1.2, color=YELLOW) for side in sides], lag_ratio=0.3, run_time=highlight_time))

        # Highlight vertices
        vertices = VGroup(*[Dot(v, radius=0.08, color=YELLOW) for v in rectangle_shape.get_vertices()])
        self.play(LaggedStart(*[Flash(v, flash_radius=0.3, line_length=0.2, color=YELLOW) for v in vertices], lag_ratio=0.3, run_time=highlight_time))
        self.wait(0.5)

        # --- Circle ---
        # Left side: Animated drawing of Circle
        circle_shape = Circle(color=PURPLE, fill_opacity=0.8).set_height(self.left_region.height * 0.6)
        circle_shape.move_to(self.left_region)

        # Right side: Real-world example (Coin)
        coin_shape = Circle(color=GOLD, fill_opacity=0.7).set_height(self.right_region.height * 0.4)
        coin_text = Text("Coin", font_size=30, color=WHITE).next_to(coin_shape, DOWN)
        coin_example = VGroup(coin_shape, coin_text).move_to(self.right_region)

        self.play(
        Transform(current_left_shape, circle_shape, run_time=transform_time),
        Transform(current_right_example, coin_example, run_time=transform_time)
        )
        current_left_shape = circle_shape
        current_right_example = coin_example

        self.wait(1)

        # Fade out all content at the end of the scene
        self.play(FadeOut(title), FadeOut(current_left_shape), FadeOut(current_right_example))
        self.wait(0.5)

# Set narration and duration
Scene2.narration_text = '''First, let\'s dive into 2D shapes. These are flat shapes that only have length and width. Think of them as drawings on a piece of paper. Our first shape is the Triangle, which has three straight sides and three corners, or vertices. Next up is the Square, easily recognizable with its four equal straight sides and four vertices. Similar to a square, but with two long sides and two short sides, is the Rectangle, also having four straight sides and four vertices. And finally, the Circle! A perfectly round shape with no straight sides and no vertices, just a continuous curved line.'''
Scene2.audio_duration = 5.0
