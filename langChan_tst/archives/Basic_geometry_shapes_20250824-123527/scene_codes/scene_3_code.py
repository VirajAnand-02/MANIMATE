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

class Scene3(SplitScreen):
    def construct_scene(self):
        # Title for the scene
        title = self.create_textbox("Exploring 3D Shapes", width=self.camera.frame.width * 0.8, height=1)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Cube Introduction ---
        # Narration: "Imagine a box; that's a Cube! It has six flat, square faces."

        # Left side: 3D Cube model
        cube_label = Text("Cube", font_size=48).next_to(self.left_region.get_top(), DOWN)
        cube = Cube(side_length=2, fill_opacity=0.7, fill_color=BLUE, stroke_color=WHITE)
        cube.move_to(self.left_region.get_center())

        # Right side: Real-world object (Dice)
        dice_label = Text("Dice", font_size=48).next_to(self.right_region.get_top(), DOWN)
        dice_text = Text("🎲 Dice", font_size=60) # Using emoji as placeholder for image
        dice_text.move_to(self.right_region.get_center())

        self.play(
        Write(cube_label), Create(cube),
        Write(dice_label), FadeIn(dice_text)
        )
        self.play(cube.animate.rotate(PI/2, axis=UP), run_time=2) # Initial rotation

        # Highlight faces of the cube
        faces = cube.get_faces()
        self.play(
        LaggedStart(*[
        Indicate(face, scale_factor=1.2, color=YELLOW) for face in faces
        ], lag_ratio=0.2),
        run_time=3
        )
        self.wait(1)

        # --- Sphere Introduction ---
        # Narration: "Next, we have the Sphere, which is perfectly round like a ball and has no flat faces, edges, or vertices."

        # Left side: 3D Sphere model
        sphere_label = Text("Sphere", font_size=48).next_to(self.left_region.get_top(), DOWN)
        sphere = Sphere(radius=1.1, resolution=(20, 20), fill_opacity=0.7, fill_color=GREEN, stroke_color=WHITE)
        sphere.move_to(self.left_region.get_center())

        # Right side: Real-world object (Basketball)
        basketball_label = Text("Basketball", font_size=48).next_to(self.right_region.get_top(), DOWN)
        basketball_text = Text("🏀 Basketball", font_size=60) # Using emoji as placeholder for image
        basketball_text.move_to(self.right_region.get_center())

        self.play(
        FadeOut(cube_label, shift=UP), FadeOut(dice_label, shift=UP), FadeOut(dice_text, shift=UP),
        FadeOut(cube, shift=UP),
        Write(sphere_label), Create(sphere),
        Write(basketball_label), FadeIn(basketball_text)
        )
        self.play(sphere.animate.rotate(PI/2, axis=UP), run_time=2) # Initial rotation
        self.wait(2) # No faces/edges/vertices to highlight for a sphere

        # --- Cylinder Introduction ---
        # Narration: "Think of a can of soda, that's a Cylinder! It has two circular bases and one curved side."

        # Left side: 3D Cylinder model
        cylinder_label = Text("Cylinder", font_size=48).next_to(self.left_region.get_top(), DOWN)
        cylinder = Cylinder(radius=0.8, height=2.5, resolution=(20, 1), fill_opacity=0.7, fill_color=ORANGE, stroke_color=WHITE)
        cylinder.move_to(self.left_region.get_center())

        # Right side: Real-world object (Soda Can)
        soda_can_label = Text("Soda Can", font_size=48).next_to(self.right_region.get_top(), DOWN)
        soda_can_text = Text("🥫 Soda Can", font_size=60) # Using emoji as placeholder for image
        soda_can_text.move_to(self.right_region.get_center())

        self.play(
        FadeOut(sphere_label, shift=UP), FadeOut(basketball_label, shift=UP), FadeOut(basketball_text, shift=UP),
        FadeOut(sphere, shift=UP),
        Write(cylinder_label), Create(cylinder),
        Write(soda_can_label), FadeIn(soda_can_text)
        )
        self.play(cylinder.animate.rotate(PI/2, axis=UP), run_time=2) # Initial rotation

        # Highlight bases and curved side of the cylinder
        top_base = cylinder.get_top_circle()
        bottom_base = cylinder.get_bottom_circle()
        self.play(Indicate(top_base, color=YELLOW), Indicate(bottom_base, color=YELLOW))
        self.wait(1)
        self.play(Indicate(cylinder, color=RED)) # Indicate the whole body for "curved side"
        self.wait(1)

        # --- Cone Introduction ---
        # Narration: "And finally, the Cone, which has one circular base and tapers up to a single point, just like an ice cream cone."

        # Left side: 3D Cone model
        cone_label = Text("Cone", font_size=48).next_to(self.left_region.get_top(), DOWN)
        cone = Cone(radius=1.2, height=2.5, resolution=(20, 1), fill_opacity=0.7, fill_color=PURPLE, stroke_color=WHITE)
        cone.move_to(self.left_region.get_center())

        # Right side: Real-world object (Party Hat)
        party_hat_label = Text("Party Hat", font_size=48).next_to(self.right_region.get_top(), DOWN)
        party_hat_text = Text("🎉 Party Hat", font_size=60) # Using emoji as placeholder for image
        party_hat_text.move_to(self.right_region.get_center())

        self.play(
        FadeOut(cylinder_label, shift=UP), FadeOut(soda_can_label, shift=UP), FadeOut(soda_can_text, shift=UP),
        FadeOut(cylinder, shift=UP),
        Write(cone_label), Create(cone),
        Write(party_hat_label), FadeIn(party_hat_text)
        )
        self.play(cone.animate.rotate(PI/2, axis=UP), run_time=2) # Initial rotation

        # Highlight base and apex of the cone
        base = cone.get_base()
        apex = cone.get_apex()
        self.play(Indicate(base, color=YELLOW))
        self.wait(0.5)
        self.play(Flash(apex, color=RED, flash_radius=0.5))
        self.wait(1)

        # --- Conclusion ---
        # Narration: "These 3D shapes are everywhere, from the food we eat to the buildings we live in!"

        final_message = self.create_textbox("3D Shapes Are Everywhere!", width=self.camera.frame.width * 0.8, height=1)
        final_message.move_to(ORIGIN)
        final_message.set_color(YELLOW)

        self.play(
        FadeOut(cone_label, shift=UP), FadeOut(party_hat_label, shift=UP), FadeOut(party_hat_text, shift=UP),
        FadeOut(cone, shift=UP),
        FadeOut(title, shift=UP),
        FadeIn(final_message, scale=1.2)
        )
        self.wait(2)
        self.play(FadeOut(final_message))

# Set narration and duration
Scene3.narration_text = '''Now, let\'s step into the world of 3D shapes! These shapes have length, width, and height, meaning they take up space and you can hold them. Imagine a box; that\'s a Cube! It has six flat, square faces. Next, we have the Sphere, which is perfectly round like a ball and has no flat faces, edges, or vertices. Think of a can of soda, that\'s a Cylinder! It has two circular bases and one curved side. And finally, the Cone, which has one circular base and tapers up to a single point, just like an ice cream cone. These 3D shapes are everywhere, from the food we eat to the buildings we live in!'''
Scene3.audio_duration = 5.0
