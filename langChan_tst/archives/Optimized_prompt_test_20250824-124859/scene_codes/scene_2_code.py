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
        from manim import *
        import numpy as np

        def construct_scene(self):
        # 1. Title
        # The narration starts with "So, how do we test prompts effectively?", implying this is the topic.
        # Using a generic title for the scene as no specific title text was provided in the JSON.
        title_text = self.create_textbox("Prompt Optimization Cycle", self.title_region.width * 0.8, self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(FadeIn(title_text), run_time=0.5)
        self.wait(0.5)

        # 2. A/B Test Setup (Left Side - Prompt A)
        prompt_a_str = "Prompt A: Summarize the article."
        output_a_str = "Output A: [Generic Summary]"

        prompt_a_text = self.create_textbox(prompt_a_str, self.left_region.width * 0.8, 1)
        prompt_a_box = SurroundingRectangle(prompt_a_text, buff=0.2, color=BLUE)
        prompt_a_group = VGroup(prompt_a_box, prompt_a_text)

        output_a_text = self.create_textbox(output_a_str, self.left_region.width * 0.8, 1)
        output_a_box = SurroundingRectangle(output_a_text, buff=0.2, color=GREEN)
        output_a_group = VGroup(output_a_box, output_a_text)

        arrow_a = Arrow(prompt_a_box.get_bottom(), output_a_box.get_top(), buff=0.1, color=WHITE)

        left_content = VGroup(prompt_a_group, arrow_a, output_a_group).arrange(DOWN, buff=0.5)
        left_content.move_to(self.left_region.get_center())

        # 3. A/B Test Setup (Right Side - Prompt B)
        prompt_b_str = "Prompt B: Summarize the article for a 10-year-old, highlighting key facts in bullet points."
        output_b_str = "Output B: [Child-friendly, bulleted summary]"

        prompt_b_text = self.create_textbox(prompt_b_str, self.right_region.width * 0.8, 1.5)
        prompt_b_box = SurroundingRectangle(prompt_b_text, buff=0.2, color=BLUE)
        prompt_b_group = VGroup(prompt_b_box, prompt_b_text)

        output_b_text = self.create_textbox(output_b_str, self.right_region.width * 0.8, 1.5)
        output_b_box = SurroundingRectangle(output_b_text, buff=0.2, color=GREEN)
        output_b_group = VGroup(output_b_box, output_b_text)

        arrow_b = Arrow(prompt_b_box.get_bottom(), output_b_box.get_top(), buff=0.1, color=WHITE)

        right_content = VGroup(prompt_b_group, arrow_b, output_b_group).arrange(DOWN, buff=0.5)
        right_content.move_to(self.right_region.get_center())

        # 4. A/B Test Animation (approx. 8 seconds)
        self.play(FadeIn(left_content), run_time=2)
        self.wait(2)
        self.play(FadeIn(right_content), run_time=2)
        self.wait(2)

        # 5. Transition (approx. 1 second)
        self.play(FadeOut(left_content), FadeOut(right_content), FadeOut(title_text), run_time=1)

        # 6. Iterative Cycle Setup
        steps_str = ["Define Goal", "Baseline Prompt", "Create Variations", "Run Tests", "Evaluate", "Refine"]
        steps_mobs = VGroup(*[self.create_textbox(s, 3, 0.7) for s in steps_str])
        steps_boxes = VGroup(*[SurroundingRectangle(m, buff=0.2, color=WHITE) for m in steps_mobs])
        steps_groups = VGroup(*[VGroup(box, text) for box, text in zip(steps_boxes, steps_mobs)])

        # Arrange in a circle
        radius = 3.5
        for i, group in enumerate(steps_groups):
        angle = 2 * PI * i / len(steps_groups) + PI/2 # Start at top, rotate clockwise
        group.move_to(np.array([radius * np.cos(angle), radius * np.sin(angle), 0]))

        steps_groups.move_to(ORIGIN + DOWN * 0.5) # Adjust overall position

        # Arrows for the cycle (forward arrows)
        forward_arrows = VGroup()
        for i in range(len(steps_groups) - 1): # Exclude the last step (Refine) for now
        start_mob = steps_groups[i]
        end_mob = steps_groups[i + 1]

        start_point = start_mob.get_boundary_point(end_mob.get_center() - start_mob.get_center())
        end_point = end_mob.get_boundary_point(start_mob.get_center() - end_mob.get_center())

        # Angle for clockwise curve
        arrow = CurvedArrow(start_point, end_point, angle=-TAU/len(steps_groups)/2, color=GRAY)
        forward_arrows.add(arrow)

        # Special loop-back arrow from 'Refine' (index 5) to 'Create Variations' (index 2)
        refine_mob = steps_groups[5]
        create_variations_mob = steps_groups[2]

        refine_to_variations_arrow = CurvedArrow(
        refine_mob.get_boundary_point(create_variations_mob.get_center() - refine_mob.get_center()),
        create_variations_mob.get_boundary_point(refine_mob.get_center() - create_variations_mob.get_center()),
        angle=PI/2, # Curve outwards then inwards
        color=YELLOW # Distinct color for loop back
        )

        all_cycle_elements = VGroup(steps_groups, forward_arrows, refine_to_variations_arrow)

        # 7. Iterative Cycle Animation (approx. 17 seconds)
        self.play(FadeIn(all_cycle_elements), run_time=1.5)
        self.wait(0.5)

        highlight_color = YELLOW
        loop_count = 2 # Loop through the cycle twice

        for _ in range(loop_count):
        for i in range(len(steps_groups)):
        # Highlight current step
        self.play(Indicate(steps_groups[i], color=highlight_color), run_time=0.8)

        if i < len(steps_groups) - 1: # For forward steps
        self.play(Flash(forward_arrows[i], color=highlight_color, flash_radius=0.5), run_time=0.5)
        else: # This is the 'Refine' step, leading to 'Create Variations'
        self.play(Flash(refine_to_variations_arrow, color=highlight_color, flash_radius=0.5), run_time=0.5)
        self.play(Indicate(steps_groups[2], color=highlight_color), run_time=0.8) # Indicate 'Create Variations'
        self.wait(0.2) # Pause before starting next loop or ending

        if _ < loop_count - 1: # If not the very last loop iteration
        # Reset colors for the next loop iteration
        self.play(
        steps_boxes[i].animate.set_color(WHITE), # Refine box
        refine_to_variations_arrow.animate.set_color(GRAY), # Loop arrow
        steps_boxes[2].animate.set_color(WHITE), # Create Variations box
        run_time=0.3
        )
        break # Exit inner loop after one full cycle and loop back

        self.wait(1) # Final wait

# Set narration and duration
Scene2.narration_text = '''So, how do we test prompts effectively? It begins with defining your objective. What specific task do you want the AI to perform? Once clear, you\'ll establish a baseline prompt – your initial attempt. From there, you create variations, experimenting with different phrasing, constraints, examples, or output formats. Think of it like A/B testing for your AI instructions. Each variation is then run through the model, and its output is carefully evaluated against predetermined criteria. This iterative cycle of prompting, testing, and refining is the heart of optimization, helping you pinpoint exactly what works best for your specific use case.'''
Scene2.audio_duration = 5.0
