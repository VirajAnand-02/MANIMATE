import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
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
        from manim import *
        import numpy as np

        # Narration text
        narration_text_content = (
        "Now, what happens when we multiply complex numbers? It's not just simple "
        "component-wise multiplication. Geometrically, complex multiplication is a "
        "powerful transformation. Think of it as a combination of scaling and rotation! "
        "When you multiply a complex number 'z1' by another complex number 'z2', the "
        "vector representing 'z1' undergoes a change in both its length and its direction. "
        "This visual insight is key to understanding complex multiplication intuitively."
        )

        # Create the initial narration text, placed at the top of the screen.
        # Assuming 'self.create_textbox' handles fitting the text within the given dimensions.
        narration_text = self.create_textbox(narration_text_content, config.frame_width * 0.9, config.frame_height * 0.2)
        narration_text.to_edge(UP)
        self.play(FadeIn(narration_text), run_time=1)
        self.wait(5) # Give time to read the initial overview

        # --- Setup Axes for both sides ---
        # Adjust axes dimensions to fit within the provided regions
        left_axes = Axes(
        x_range=[-3, 3, 1], y_range=[-3, 3, 1],
        x_length=self.left_region.width * 0.8, y_length=self.left_region.height * 0.8,
        axis_config={"color": GRAY, "stroke_width": 2},
        tips=False
        ).move_to(self.left_region.get_center())
        left_axes.add(left_axes.get_axis_labels(x_label="Re", y_label="Im"))

        right_axes = Axes(
        x_range=[-3, 3, 1], y_range=[-3, 3, 1],
        x_length=self.right_region.width * 0.8, y_length=self.right_region.height * 0.8,
        axis_config={"color": GRAY, "stroke_width": 2},
        tips=False
        ).move_to(self.right_region.get_center())
        right_axes.add(right_axes.get_axis_labels(x_label="Re", y_label="Im"))

        self.play(
        Create(left_axes),
        Create(right_axes),
        run_time=3
        )
        self.wait(2)

        # --- Initial Vector 'z' ---
        initial_z_complex = complex(1, 1.5) # Example complex number z = 1 + 1.5i

        # Left side vector
        z_left = Arrow(start=left_axes.c2p(0), end=left_axes.c2p(initial_z_complex), buff=0, color=BLUE, tip_length=0.2)
        label_z_left = MathTex("z", color=BLUE).next_to(z_left.get_end(), UP + RIGHT * 0.5)

        # Right side vector (initially identical to left)
        z_right_initial = Arrow(start=right_axes.c2p(0), end=right_axes.c2p(initial_z_complex), buff=0, color=BLUE, tip_length=0.2)
        label_z_right_initial = MathTex("z", color=BLUE).next_to(z_right_initial.get_end(), UP + RIGHT * 0.5)

        self.play(
        GrowArrow(z_left),
        Write(label_z_left),
        GrowArrow(z_right_initial),
        Write(label_z_right_initial),
        run_time=2
        )
        self.wait(1)

        # --- Left Animation: Real Scaling ---
        # Fade out the general narration and bring in specific narration for the left side.
        left_narration_content = "On the left, we see simple scaling by a real number. The direction remains the same, only the length changes."
        left_narration = self.create_textbox(left_narration_content, self.left_region.width * 0.9, config.frame_height * 0.1)
        left_narration.next_to(left_axes, UP)

        self.play(
        FadeOut(narration_text),
        FadeIn(left_narration),
        run_time=1
        )

        k_scalar = 2
        scaled_z_complex_left = initial_z_complex * k_scalar
        scaled_z_point_left = left_axes.c2p(scaled_z_complex_left)

        # Path for scaling (subtle dashed line)
        scaling_path_left = Line(z_left.get_end(), scaled_z_point_left, stroke_opacity=0.5, stroke_width=2, color=YELLOW)
        scaling_path_left.set_stroke(dash_array=[0.05, 0.1])

        # Scaled vector
        scaled_z_left = Arrow(start=left_axes.c2p(0), end=scaled_z_point_left, buff=0, color=GREEN, tip_length=0.2)
        label_scaled_z_left = MathTex(f"{k_scalar}z", color=GREEN).next_to(scaled_z_left.get_end(), UP + RIGHT * 0.5)

        self.play(
        Create(scaling_path_left),
        Transform(z_left, scaled_z_left), # z_left transforms into scaled_z_left
        FadeOut(label_z_left),
        FadeIn(label_scaled_z_left),
        run_time=5
        )
        self.wait(3)

        # --- Right Animation: Complex Multiplication (Scaling + Rotation) ---
        # Fade out left narration and bring in specific narration for the right side.
        right_narration_content = "Complex multiplication involves both scaling and rotation. The vector changes both its length and direction. This visual insight is key to understanding complex multiplication intuitively."
        right_narration = self.create_textbox(right_narration_content, self.right_region.width * 0.9, config.frame_height * 0.1)
        right_narration.next_to(right_axes, UP)

        self.play(
        FadeOut(left_narration),
        FadeIn(right_narration),
        run_time=1
        )

        # Complex multiplier w = magnitude * e^(i * angle)
        magnitude_w = 1.8
        angle_w = PI / 3 # 60 degrees
        w_complex = magnitude_w * np.exp(1j * angle_w)
        transformed_z_complex_right = initial_z_complex * w_complex

        # Create a ValueTracker for the complex number representing the current state of z_right
        current_z_tracker = ValueTracker(initial_z_complex)

        # The actual vector for the right side, which will be updated
        z_right_animated = Arrow(start=right_axes.c2p(0), end=right_axes.c2p(initial_z_complex), buff=0, color=ORANGE, tip_length=0.2)

        # Updater function for the animated vector
        def update_z_right_vector(mobj):
        current_complex = current_z_tracker.get_value()
        mobj.become(Arrow(start=right_axes.c2p(0), end=right_axes.c2p(current_complex), buff=0, color=ORANGE, tip_length=0.2))

        z_right_animated.add_updater(update_z_right_vector)
        self.add(z_right_animated) # Add the animated vector to the scene
        self.remove(z_right_initial) # Remove the initial static vector
        self.remove(label_z_right_initial) # Remove its label

        # Path for the transformation: first scale, then rotate
        # Intermediate point after scaling only
        scaled_only_complex_right = initial_z_complex * magnitude_w
        scaled_only_point_right = right_axes.c2p(scaled_only_complex_right)

        # Path for scaling part (subtle dashed line)
        path_scale = Line(right_axes.c2p(initial_z_complex), scaled_only_point_right, color=YELLOW, stroke_width=2, stroke_opacity=0.5)
        path_scale.set_stroke(dash_array=[0.05, 0.1])

        # Path for rotation part (subtle dashed arc)
        path_rotate = Arc(
        start_angle=np.angle(scaled_only_complex_right),
        angle=angle_w,
        radius=np.abs(scaled_only_complex_right),
        arc_center=right_axes.c2p(0),
        color=YELLOW, stroke_width=2, stroke_opacity=0.5
        )
        path_rotate.set_stroke(dash_array=[0.05, 0.1])

        # Animate scaling
        self.play(
        Create(path_scale),
        current_z_tracker.animate.set_value(scaled_only_complex_right),
        run_time=4
        )
        self.wait(1)

        # Animate rotation
        self.play(
        Create(path_rotate),
        current_z_tracker.animate.set_value(transformed_z_complex_right),
        run_time=4
        )

        # Final label for the transformed vector
        label_transformed_z_right = MathTex("wz", color=ORANGE).next_to(z_right_animated.get_end(), UP + RIGHT * 0.5)
        self.play(FadeIn(label_transformed_z_right), run_time=1)

        self.wait(5) # Give time to read the final narration and observe the result

        # Clean up updaters before ending the scene
        z_right_animated.remove_updater(update_z_right_vector)

        # Final fade out of all mobjects
        self.play(
        FadeOut(left_axes),
        FadeOut(right_axes),
        FadeOut(scaled_z_left), # This is the final state of the left vector
        FadeOut(label_scaled_z_left),
        FadeOut(scaling_path_left),
        FadeOut(z_right_animated), # This is the final state of the right vector
        FadeOut(label_transformed_z_right),
        FadeOut(path_scale),
        FadeOut(path_rotate),
        FadeOut(right_narration),
        run_time=2
        )
        self.wait(1)

# Set narration and duration
Scene2.narration_text = '''Now, what happens when we multiply complex numbers? It\'s not just simple component-wise multiplication. Geometrically, complex multiplication is a powerful transformation. Think of it as a combination of scaling and rotation! When you multiply a complex number \'z1\' by another complex number \'z2\', the vector representing \'z1\' undergoes a change in both its length and its direction. This visual insight is key to understanding complex multiplication intuitively.'''
Scene2.audio_duration = 5.0