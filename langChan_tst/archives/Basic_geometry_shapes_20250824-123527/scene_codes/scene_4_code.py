```python
from manim import *

class GeneratedScene_4(Scene):
    def construct(self):
        # --- Part 1: Montage of Shapes ---
        self.next_section("Montage", skip_animations=False)
        
        # 2D Shapes (actual mobjects)
        shapes_2d_mobjects = [
            Triangle(color=BLUE, fill_opacity=0.8).scale(0.8),
            Square(color=GREEN, fill_opacity=0.8).scale(0.8),
            Rectangle(color=YELLOW, fill_opacity=0.8, width=2.5, height=1.5),
            Circle(color=RED, fill_opacity=0.8).scale(0.8),
        ]
        
        # 3D Shapes (represented by their names as Text mobjects for clarity and speed in montage)
        shapes_3d_text = [
            Text("Cube", color=PURPLE, font_size=72),
            Text("Sphere", color=ORANGE, font_size=72),
            Text("Cylinder", color=TEAL, font_size=72),
            Text("Cone", color=PINK, font_size=72),
        ]

        all_montage_elements = shapes_2d_mobjects + shapes_3d_text

        # Initial display of the first shape
        current_element = all_montage_elements[0].center()
        self.play(Create(current_element), run_time=0.8)
        self.wait(0.4)

        # Cycle through the rest of the elements
        for i in range(1, len(all_montage_elements)):
            next_element = all_montage_elements[i].center()
            self.play(Transform(current_element, next_element), run_time=0.7)
            self.wait(0.3)
            current_element = next_element
        
        # Fade out the last element
        self.play(FadeOut(current_element), run_time=0.7)
        self.wait(0.5)

        # --- Part 2: House and Garden Scene with Highlights ---
        self.next_section("HouseAndGarden", skip_animations=False)

        # Create the ground
        ground = Rectangle(width=FRAME_WIDTH, height=1, color=GREEN_B, fill_opacity=1).to_edge(DOWN, buff=0)

        # Create the house body (rectangle)
        house_body = Rectangle(width=4, height=3, color=GRAY_B, fill_opacity=0.8).next_to(ground, UP, buff=0)
        
        # Create the roof (triangle)
        roof = Triangle(color=RED_B, fill_opacity=0.9).scale(2.5)
        roof.move_to(house_body.get_top() + UP * roof.get_height() / 2 - UP * 0.1)
        roof.set_width(house_body.get_width() * 1.2, stretch=True)

        # Create windows (squares)
        window1 = Square(side_length=1, color=BLUE_A, fill_opacity=0.7).move_to(house_body.get_center() + UP * 0.5 + LEFT * 0.7)
        window2 = Square(side_length=1, color=BLUE_A, fill_opacity=0.7).move_to(house_body.get_center() + UP * 0.5 + RIGHT * 0.7)
        
        # Create a door (rectangle)
        door = Rectangle(width=1, height=1.5, color=BROWN, fill_opacity=0.8).move_to(house_body.get_bottom() + DOWN * 0.75 + RIGHT * 0.5)
        door.align_to(house_body, DOWN)
        door.shift(RIGHT * 0.5)

        house_elements = VGroup(house_body, roof, window1, window2, door)
        house_elements.shift(LEFT * 2) # Move house to the left

        # Create a tree (trunk as rectangle, canopy as circle)
        tree_trunk = Rectangle(width=0.5, height=2, color=BROWN, fill_opacity=1).next_to(ground, UP, buff=0).shift(RIGHT * 4)
        tree_canopy = Circle(radius=1.5, color=GREEN_E, fill_opacity=0.9).next_to(tree_trunk, UP, buff=0.1)
        tree_elements = VGroup(tree_trunk, tree_canopy)

        # Create a ball (circle representing sphere)
        ball = Circle(radius=0.7, color=ORANGE, fill_opacity=0.8).next_to(ground, UP, buff=0.1).shift(RIGHT * 0.5 + LEFT * 0.5)
        ball.shift(LEFT * 1.5)

        # Add all elements to the scene
        self.play(
            Create(ground),
            Create(house_elements),
            Create(tree_elements),
            Create(ball),
            run_time=3
        )
        self.wait(1)

        # Highlight shapes
        highlight_duration = 1.5
        fade_out_duration = 0.5
        label_color = YELLOW

        # Highlight Roof as Triangle
        roof_highlight = SurroundingRectangle(roof, color=label_color, buff=0.1)
        roof_label = Text("Triangle", color=label_color).next_to(roof, UP)
        self.play(Create(roof_highlight), Write(roof_label), run_time=highlight_duration)
        self.wait(0.5)
        self.play(FadeOut(roof_highlight), FadeOut(roof_label), run_time=fade_out_duration)

        # Highlight Window as Square
        window_highlight = SurroundingRectangle(window1, color=label_color, buff=0.1)
        window_label = Text("Square", color=label_color).next_to(window1, UP)
        self.play(Create(window_highlight), Write(window_label), run_time=highlight_duration)
        self.wait(0.5)
        self.play(FadeOut(window_highlight), FadeOut(window_label), run_time=fade_out_duration)

        # Highlight House body as Rectangle
        house_body_highlight = SurroundingRectangle(house_body, color=label_color, buff=0.1)
        house_body_label = Text("Rectangle", color=label_color).next_to(house_body, DOWN)
        self.play(Create(house_body_highlight), Write(house_body_label), run_time=highlight_duration)
        self.wait(0.5)
        self.play(FadeOut(house_body_highlight), FadeOut(house_body_label), run_time=fade_out_duration)

        # Highlight Tree trunk as Cylinder (represented as Rectangle)
        trunk_highlight = SurroundingRectangle(tree_trunk, color=label_color, buff=0.1)
        trunk_label = Text("Cylinder", color=label_color).next_to(tree_trunk, UP)
        self.play(Create(trunk_highlight), Write(trunk_label), run_time=highlight_duration)
        self.wait(0.5)
        self.play(FadeOut(trunk_highlight), FadeOut(trunk_label), run_time=fade_out_duration)

        # Highlight Tree canopy as Sphere (represented as Circle)
        canopy_highlight = SurroundingRectangle(tree_canopy, color=label_color, buff=0.1)
        canopy_label = Text("Sphere", color=label_color).next_to(tree_canopy, UP)
        self.play(Create(canopy_highlight), Write(canopy_label), run_time=highlight_duration)
        self.wait(0.5)
        self.play(FadeOut(canopy_highlight), FadeOut(canopy_label), run_time=fade_out_duration)

        # Highlight Ball as Sphere
        ball_highlight = SurroundingRectangle(ball, color=label_color, buff=0.1)
        ball_label = Text("Sphere", color=label_color).next_to(ball, UP)
        self.play(Create(ball_highlight), Write(ball_label), run_time=highlight_duration)
        self.wait(0.5)
        self.play(FadeOut(ball_highlight), FadeOut(ball_label), run_time=fade_out_duration)

        self.wait(2) # Pause before final text

        # --- Part 3: Final Text Overlay and Graphic ---
        self.next_section("FinalMessage", skip_animations=False)
        self.play(
            FadeOut(ground),
            FadeOut(house_elements),
            FadeOut(tree_elements),
            FadeOut(ball),
            run_time=2
        )

        final_text = Text("What shapes can YOU find?", font_size=60, color=WHITE).center()
        
        # Friendly closing graphic: a simple star
        star = Star(n=5, outer_radius=1.5, inner_radius=0.7, color=GOLD, fill_opacity=1).next_to(final_text, DOWN, buff=0.8)
        
        self.play(Write(final_text), Create(star), run_time=3)
        self.wait(5) # Long wait for the closing remarks of the text.
```