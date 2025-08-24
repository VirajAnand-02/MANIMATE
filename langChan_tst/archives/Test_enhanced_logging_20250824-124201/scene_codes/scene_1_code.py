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
        # 1. Initial Title: "Debugging Dilemma"
        initial_title_text = self.create_textbox("Debugging Dilemma", width=self.title_region.width, height=self.title_region.height)
        initial_title_text.move_to(self.title_region.get_center())
        self.play(FadeIn(initial_title_text, shift=UP), run_time=1)
        self.wait(0.5) # Short wait before main animation starts

        # 2. Log File Setup
        log_file_rect = Rectangle(
        width=self.main_region.width * 0.6,
        height=self.main_region.height * 0.7,
        color=GREY_B,
        fill_opacity=0.8
        ).move_to(self.main_region.get_center() + LEFT * self.main_region.width * 0.15)

        # Generate some log lines to simulate a dense log file
        log_lines_text = [
        "[2023-10-27 10:01:05] INFO: User 'admin' logged in.",
        "[2023-10-27 10:01:10] DEBUG: Processing request /api/data.",
        "[2023-10-27 10:01:12] ERROR: NullPointerException at com.app.Service.processData(Service.java:123)",
        "[2023-10-27 10:01:15] INFO: Database connection successful.",
        "[2023-10-27 10:01:20] WARN: Low disk space on /var/log.",
        "[2023-10-27 10:01:22] DEBUG: Cache invalidated for user 123.",
        "[2023-10-27 10:01:25] ERROR: Failed to retrieve user profile for ID 456.",
        "[2023-10-27 10:01:30] INFO: Report generated successfully."
        ]
        log_lines = VGroup(*[
        Text(line, font_size=18, color=WHITE, disable_ligatures=True).set_max_width(log_file_rect.width * 0.9)
        for line in log_lines_text
        ]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        log_lines.move_to(log_file_rect.get_center())

        # Identify the error line for later highlighting
        error_line_index = 2 # Index of "NullPointerException" line
        error_line_mobject = log_lines[error_line_index]

        log_file_content = VGroup(log_file_rect, log_lines)

        # 3. Magnifying Glass
        magnifying_lens = Circle(radius=0.7, color=BLUE_A, fill_opacity=0.3, stroke_width=5)
        magnifying_handle = Line(magnifying_lens.get_bottom() + DOWN * 0.1, magnifying_lens.get_bottom() + DOWN * 1.0 + RIGHT * 0.8, stroke_width=5, color=GREY_C)
        magnifying_glass = VGroup(magnifying_lens, magnifying_handle)
        magnifying_glass.move_to(self.main_region.get_center() + RIGHT * self.main_region.width * 0.1)

        # 4. Overlay Text
        log_label = Text("Log File", font_size=36, color=WHITE).next_to(log_file_rect, UP, buff=0.3)
        error_overlay_text = Text("Error: NullPointerException", font_size=28, color=RED).move_to(error_line_mobject.get_center()).shift(UP * 0.2)

        # 5. Confused Face/Thought Bubble
        confused_face = Text("?", font_size=60, color=WHITE)
        thought_bubble = ThoughtBubble(direction=UL, fill_opacity=0.8, stroke_color=WHITE).set_height(2).set_width(2)
        thought_bubble.pin_to(magnifying_glass.get_top() + UP * 0.5)
        confused_face.move_to(thought_bubble.get_center())
        thought_group = VGroup(thought_bubble, confused_face)
        thought_group.next_to(magnifying_glass, UP + RIGHT, buff=0.5).scale(0.8)

        # --- Animation Part 1: The Problem (Generic Log File & Confusion) ---
        # Narration: "Ever stared at a log file, wondering which specific test run or scenario produced that cryptic error?"
        self.play(
        Create(log_file_rect),
        Write(log_lines),
        FadeIn(log_label, shift=UP),
        run_time=4
        )
        self.wait(3)

        # Narration: "Traditional application logs, while vital, often lack the crucial context from the testing environment."
        self.play(
        Create(magnifying_glass),
        magnifying_glass.animate.shift(RIGHT * 0.5 + UP * 0.3), # Hover effect
        run_time=2
        )
        self.play(Indicate(error_line_mobject, scale_factor=1.1, color=YELLOW), run_time=1)
        self.play(Write(error_overlay_text), run_time=1)
        self.wait(4)

        # Narration: "This missing link can turn debugging into a time-consuming, frustrating detective novel without clues."
        self.play(
        FadeIn(thought_group, shift=UP),
        run_time=2
        )
        self.wait(6)

        # --- Animation Part 2: The Solution (Lightbulb & Transition) ---
        # Narration: "Today, we're unveiling 'Test Enhanced Logging' – a powerful technique..."
        self.play(
        FadeOut(log_file_content, shift=DOWN),
        FadeOut(log_label, shift=DOWN),
        FadeOut(error_overlay_text, shift=DOWN),
        FadeOut(magnifying_glass, shift=DOWN),
        FadeOut(thought_group, shift=DOWN),
        FadeOut(initial_title_text, shift=DOWN), # Fade out the initial title
        run_time=2
        )

        # Lightbulb appears
        lightbulb = Lightbulb().scale(0.8).move_to(self.main_region.get_center())
        lightbulb.bulb.set_fill(YELLOW, opacity=0)
        lightbulb.filament.set_stroke(YELLOW, opacity=0)

        self.play(Create(lightbulb), run_time=1.5)
        self.play(
        FadeIn(lightbulb.bulb.set_fill(YELLOW, opacity=1), lightbulb.filament.set_stroke(YELLOW, opacity=1)),
        run_time=0.5
        )
        self.wait(1.5) # For "Today, we're unveiling 'Test Enhanced Logging'"

        # Transition to TEL title card with gears
        self.play(FadeOut(lightbulb), run_time=1)

        tel_title_card = self.create_textbox("Test Enhanced Logging", width=self.title_region.width, height=self.title_region.height)
        tel_title_card.move_to(self.title_region.get_center())

        gear1 = Gear(num_teeth=10, radius=0.8, color=BLUE_D, fill_opacity=0.8)
        gear2 = Gear(num_teeth=10, radius=0.8, color=BLUE_E, fill_opacity=0.8)
        # Position gears to interlock visually
        gear1.next_to(self.main_region.get_center(), LEFT, buff=1.5)
        gear2.next_to(gear1, RIGHT, buff=0.1, aligned_edge=DOWN)
        gear_group = VGroup(gear1, gear2)
        gear_group.scale_to_fit_width(self.main_region.width * 0.5)
        gear_group.move_to(self.main_region.get_center())

        self.play(
        Write(tel_title_card),
        Create(gear_group),
        run_time=2
        )

        # Animate gears turning continuously for the remainder of the narration
        self.play(
        Rotate(gear1, angle=2*PI, about_point=gear1.get_center(), rate_func=linear),
        Rotate(gear2, angle=-2*PI, about_point=gear2.get_center(), rate_func=linear),
        run_time=10 # Long run_time for continuous rotation
        )
        self.wait(4) # For "injects vital, test-specific information directly into your logs..."

        # Final fade out for scene transition
        self.play(
        FadeOut(tel_title_card),
        FadeOut(gear_group),
        run_time=1
        )

# Set narration and duration
Scene1.narration_text = '''Ever stared at a log file, wondering which specific test run or scenario produced that cryptic error? Traditional application logs, while vital, often lack the crucial context from the testing environment. This missing link can turn debugging into a time-consuming, frustrating detective novel without clues. Today, we\'re unveiling \'Test Enhanced Logging\' – a powerful technique that injects vital, test-specific information directly into your logs, transforming vague errors into actionable insights and making your debugging process significantly more efficient.'''
Scene1.audio_duration = 5.0
