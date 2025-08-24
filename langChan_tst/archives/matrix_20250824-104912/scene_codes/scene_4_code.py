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

class Scene4(SplitScreen):
    def construct_scene(self):
        # Left side animations
        cube = Cube().scale(0.7).rotate(PI / 4, axis=RIGHT)
        padlock = SVGMobject("padlock.svg").scale(0.7)  # Replace with actual padlock SVG
        binary = VGroup(*[Text(str(i), font_size=24) for i in [0, 1] * 20]).arrange(RIGHT)
        binary.add_updater(lambda m: m.shift(LEFT * 0.1))
        bridge = VGroup(Line(LEFT * 2, RIGHT * 2), Line(UP * 1, DOWN * 1)).scale(0.7)  # Simple bridge
        force_vectors = VGroup(*[Arrow(ORIGIN, UP * 0.5, color=RED), Arrow(ORIGIN, DOWN * 0.5, color=BLUE)]).arrange(RIGHT, buff=0.5).scale(0.5).move_to(bridge)
        neural_network = VGroup(*[Circle(radius=0.1) for _ in range(5)]).arrange(RIGHT)
        for i in range(4):
        neural_network.add(Line(neural_network[i].get_right(), neural_network[i+1].get_left()))
        neural_network.scale(0.7)

        # Right side text
        title_text = self.create_textbox("Matrices: Organize, Transform, Solve", self.right_region.width * 0.8, self.right_region.height * 0.2)
        thank_you_text = self.create_textbox("Thank You for Watching!", self.right_region.width * 0.8, self.right_region.height * 0.2)

        # Positioning
        cube.move_to(self.left_region.get_center())
        padlock.move_to(self.left_region.get_center())
        bridge.move_to(self.left_region.get_center())
        neural_network.move_to(self.left_region.get_center())
        title_text.move_to(self.right_region.get_center())
        thank_you_text.move_to(self.right_region.get_center())

        # Animations
        self.play(Create(cube))
        self.wait(2)
        self.play(Transform(cube, padlock), Create(binary))
        self.wait(2)
        self.play(Transform(padlock, bridge), FadeOut(binary), Create(force_vectors))
        self.wait(2)
        self.play(Transform(bridge, neural_network), FadeOut(force_vectors))
        self.wait(2)
        self.play(FadeOut(neural_network))

        self.play(Write(title_text))
        self.wait(3)
        self.play(Transform(title_text, thank_you_text))
        self.wait(1)

# Set narration and duration
Scene4.narration_text = '''Matrices aren\'t just for textbooks; they\'re shaping our world! In computer graphics, matrices transform 3D objects – rotating, scaling, and moving them on your screen. Cryptography relies on them to encrypt and decrypt sensitive information, keeping our data secure. Engineers use matrices for structural analysis, from designing bridges to optimizing aircraft performance. In data science, matrices organize and process vast datasets, powering machine learning and AI algorithms. From simulating complex systems to solving intricate equations, matrices provide the essential framework for understanding and manipulating the world around us. They are a powerful, versatile tool for organizing, transforming, and solving complex problems. So, next time you see organized data, remember the incredible power of matrices!'''
Scene4.audio_duration = 5.0
