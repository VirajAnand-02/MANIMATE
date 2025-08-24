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
        # 1. Create and position the title
        title_text = self.create_textbox("Optimized Prompt Testing", width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())

        # 2. Define prompt and response texts
        vague_prompt_text = "Write something about dogs."
        poor_response_text = "Dogs are animals. They have fur. They bark. Some are big, some are small. They live with people."
        detailed_prompt_text = "Write a 5-sentence persuasive paragraph about why dogs make great emotional support animals, using an encouraging tone."
        better_response_text = "Dogs offer unparalleled emotional support, their unwavering loyalty and comforting presence providing immense relief during stressful times. Their intuitive nature allows them to sense human emotions, offering a gentle nudge or a warm cuddle exactly when needed. Engaging with an emotional support dog can significantly reduce feelings of anxiety and loneliness, fostering a sense of purpose and companionship. These incredible animals encourage routine and physical activity, contributing to overall mental well-being. Truly, the bond with an emotional support dog is a powerful, healing force that enriches lives profoundly."

        # 3. Create initial mobjects (vague prompt, poor response) and their labels
        prompt_label = Text("Prompt:", font_size=36, color=YELLOW)
        response_label = Text("AI Response:", font_size=36, color=BLUE)

        vague_prompt = self.create_textbox(vague_prompt_text, width=self.main_region.width * 0.8, height=self.main_region.height * 0.2)
        poor_response = self.create_textbox(poor_response_text, width=self.main_region.width * 0.8, height=self.main_region.height * 0.4)

        # Arrange initial content to calculate positions
        temp_prompt_group_initial = VGroup(prompt_label.copy(), vague_prompt.copy()).arrange(DOWN, buff=0.2)
        temp_response_group_initial = VGroup(response_label.copy(), poor_response.copy()).arrange(DOWN, buff=0.2)
        temp_initial_content_group = VGroup(temp_prompt_group_initial, temp_response_group_initial).arrange(DOWN, buff=0.5).move_to(self.main_region.get_center())

        # Apply calculated positions to the actual mobjects
        prompt_label.move_to(temp_prompt_group_initial[0].get_center())
        vague_prompt.move_to(temp_prompt_group_initial[1].get_center())
        response_label.move_to(temp_response_group_initial[0].get_center())
        poor_response.move_to(temp_response_group_initial[1].get_center())

        # 4. Create final mobjects (detailed prompt, better response) and position them at their final locations
        detailed_prompt = self.create_textbox(detailed_prompt_text, width=self.main_region.width * 0.8, height=self.main_region.height * 0.3)
        better_response = self.create_textbox(better_response_text, width=self.main_region.width * 0.8, height=self.main_region.height * 0.5)

        # Arrange final content to calculate positions
        temp_prompt_group_final = VGroup(prompt_label.copy(), detailed_prompt.copy()).arrange(DOWN, buff=0.2)
        temp_response_group_final = VGroup(response_label.copy(), better_response.copy()).arrange(DOWN, buff=0.2)
        temp_final_content_group = VGroup(temp_prompt_group_final, temp_response_group_final).arrange(DOWN, buff=0.5).move_to(self.main_region.get_center())

        # Apply calculated positions to the final mobjects
        detailed_prompt.move_to(temp_prompt_group_final[1].get_center())
        better_response.move_to(temp_response_group_final[1].get_center())

        # 5. Animations
        self.play(Write(title_text), run_time=2)
        self.wait(3) # Narration: "Welcome to our guide... your prompt."

        self.play(
        Write(prompt_label),
        Write(vague_prompt),
        run_time=4
        )
        self.wait(4) # Narration: "But how do you know... testing comes in."

        self.play(
        Write(response_label),
        Write(poor_response),
        run_time=4
        )
        self.wait(4) # Narration: "It's not just about crafting... language models."

        self.play(
        Transform(vague_prompt, detailed_prompt),
        run_time=7
        )
        self.wait(4) # Narration: "This process is crucial... AI-driven tasks."

        self.play(
        Transform(poor_response, better_response),
        run_time=7
        )
        self.wait(2) # End of narration

# Set narration and duration
Scene1.narration_text = '''Welcome to our guide on Optimized Prompt Testing! In the world of AI, the quality of your output is directly tied to the quality of your input – your prompt. But how do you know if your prompt is truly effective? That\'s where optimized prompt testing comes in. It\'s not just about crafting a good prompt; it\'s about systematically evaluating and refining your prompts to achieve the best possible results from large language models. This process is crucial for anyone looking to harness the full potential of AI, ensuring consistency, accuracy, and efficiency in their AI-driven tasks.'''
Scene1.audio_duration = 5.0
