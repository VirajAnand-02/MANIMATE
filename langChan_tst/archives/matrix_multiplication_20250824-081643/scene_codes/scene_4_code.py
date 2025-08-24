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

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Title
        title_text = self.create_textbox("Key Takeaways", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Main animation
        takeaways = [
        "1. Dimensions must match (m x N) * (N x p)",
        "2. Row by Column rule",
        "3. Not Commutative (AB ≠ BA)"
        ]

        texts = [Text(takeaway) for takeaway in takeaways]
        group = VGroup(*texts).arrange(DOWN, aligned_edge=LEFT).scale(0.7)
        group.move_to(self.main_region.get_center() + LEFT * 2)
        self.play(Write(group))
        self.wait(2)

        # Visual examples
        square = Square(side_length=1).move_to(self.main_region.get_center() + RIGHT * 2 + UP * 1)
        self.play(square.animate.rotate(PI/4), run_time=1)

        dots = VGroup(*[Dot(point=np.random.rand(3)*2-1) for _ in range(50)]).move_to(self.main_region.get_center() + RIGHT * 2 + DOWN * 0.5).scale(0.5)
        self.play(dots.animate.shift(UP*0.5), run_time=1)

        line = Line(start=LEFT, end=RIGHT).move_to(self.main_region.get_center() + RIGHT * 2 + DOWN * 2)
        self.play(line.animate.rotate(PI/2), run_time=1)

        self.wait(2)

        practice_text = Text("Practice makes perfect!").scale(0.8)
        practice_text.move_to(self.main_region.get_center() + DOWN * 3)
        self.play(Write(practice_text))
        self.wait(2)

# Set narration and duration
Scene4.narration_text = '''So, what are the key takeaways? First, always check the dimensions: the inner dimensions must match. Second, remember the \'row by column\' rule – it\'s the foundation for every element in your product matrix. Matrix multiplication is not commutative, meaning A times B is generally not equal to B times A, which is a crucial difference from scalar multiplication. This operation is fundamental in many fields: in computer graphics, it\'s used for transformations like rotations, scaling, and translations. In data science, it helps process large datasets and perform statistical analyses. In physics, it describes quantum states and transformations. Keep practicing with different matrix sizes, and you\'ll master this essential concept. Thanks for watching!'''
Scene4.audio_duration = 5.0
