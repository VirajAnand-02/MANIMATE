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
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox("Optimized Prompt Testing", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text), run_time=2)
        self.wait(1)

        # 2. Initial simple, vague prompt box ('Write a story.')
        vague_prompt_str = "Write a story."
        vague_text = Text(vague_prompt_str, font_size=40, color=BLUE_C)
        vague_box = Rectangle(
        width=vague_text.width + 1.0,
        height=vague_text.height + 1.0,
        color=BLUE_C,
        fill_opacity=0.2
        ).surround(vague_text, buff=0.5)
        vague_group = VGroup(vague_box, vague_text)
        vague_group.move_to(self.main_region.get_center())

        self.play(Create(vague_box), Write(vague_text), run_time=3)
        self.wait(2)

        # 3. Expand and fill with more detail, evolving into an optimized prompt
        detailed_prompt_str = "Write a 3-paragraph sci-fi story about a lone astronaut discovering an alien artifact, focusing on themes of isolation and wonder, in a formal tone."
        detailed_text = Text(detailed_prompt_str, font_size=28, line_spacing=1.2, color=GREEN_C)
        detailed_text.set(width=self.main_region.width * 0.45) # Adjust width to fit
        detailed_box = Rectangle(
        width=detailed_text.width + 1.0,
        height=detailed_text.height + 1.0,
        color=GREEN_C,
        fill_opacity=0.2
        ).surround(detailed_text, buff=0.5)

        # Position the detailed prompt group to the left side of the main region
        detailed_prompt_group = VGroup(detailed_box, detailed_text)
        detailed_prompt_group.move_to(self.main_region.get_center() + LEFT * (self.main_region.width * 0.25))

        self.play(FadeOut(vague_text, shift=UP), run_time=1)
        # Transform the vague box into the detailed box's shape and position
        self.play(Transform(vague_box, detailed_box), run_time=4)
        self.play(FadeIn(detailed_text), run_time=2)
        self.wait(5)

        # 4. Show the vastly improved output next to it
        output_text_str = "Output: A compelling 3-paragraph sci-fi story, rich in descriptive language and thematic depth, delivered in a formal tone."
        output_text = Text(output_text_str, font_size=28, line_spacing=1.2, color=YELLOW_C)
        output_text.set(width=self.main_region.width * 0.45)
        output_box = Rectangle(
        width=output_text.width + 1.0,
        height=output_text.height + 1.0,
        color=YELLOW_C,
        fill_opacity=0.2
        ).surround(output_text, buff=0.5)
        output_group = VGroup(output_box, output_text)
        output_group.next_to(detailed_prompt_group, RIGHT, buff=0.8) # Position next to the detailed prompt

        self.play(FadeIn(output_group, shift=RIGHT), run_time=3)
        self.wait(5)

        # 5. A checklist of 'Best Practices' appears with checkmarks
        best_practices_title = Text("Best Practices:", font_size=36, color=WHITE)
        best_practices_items_str = ["Be Specific", "Provide Examples", "Define Format", "Set Constraints"]
        best_practices_items = VGroup(*[Text(item, font_size=30, color=WHITE) for item in best_practices_items_str])
        best_practices_items.arrange(DOWN, buff=0.6, aligned_edge=LEFT)

        # Position the checklist below the prompt/output boxes
        best_practices_group = VGroup(best_practices_title, best_practices_items).arrange(DOWN, buff=0.5)
        best_practices_group.next_to(self.main_region.get_bottom(), UP, buff=0.5)
        best_practices_group.align_to(self.main_region, LEFT)
        best_practices_group.shift(RIGHT * (self.main_region.width / 2 - best_practices_group.width / 2)) # Center horizontally

        self.play(FadeIn(best_practices_title, shift=UP), run_time=1.5)
        self.wait(0.5)

        checkmarks = VGroup()
        for i, item in enumerate(best_practices_items):
        self.play(FadeIn(item, shift=UP), run_time=1)
        checkmark = Checkmark().next_to(item, LEFT, buff=0.5).scale(0.7).set_color(GREEN)
        checkmarks.add(checkmark)
        self.play(Create(checkmark), run_time=0.5)
        if i < len(best_practices_items) - 1:
        self.wait(0.5) # Short pause between items

        self.wait(7) # Final wait for narration

# Set narration and duration
Scene4.narration_text = '''Optimized prompt testing is an ongoing process, not a one-time event. As models evolve or your needs change, your prompts may need re-evaluation. Best practices include being specific and concise, providing examples, defining output format, and setting clear constraints. For instance, instead of \'write a story,\' try \'write a 3-paragraph sci-fi story about a lone astronaut discovering an alien artifact, focusing on themes of isolation and wonder, in a formal tone.\' By systematically testing and refining, you move from vague instructions to powerful, precise commands, unlocking superior performance from your AI models. Start testing your prompts today and elevate your AI interactions!'''
Scene4.audio_duration = 5.0
