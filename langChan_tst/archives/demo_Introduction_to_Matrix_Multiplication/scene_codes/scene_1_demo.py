import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene 1: Title And Main Content", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox("Welcome to our educational video about linear algebra. Today we'll explore matrix multiplication and its applications.", 
                                      self.main_region.width, 
                                      self.main_region.height, 
                                      font_size=24)
        main_text.move_to(self.main_region.get_center())
        
        # Animate
        self.play(Write(title_text))
        self.wait(1)
        self.play(Write(main_text))
        self.wait(3)
        self.play(FadeOut(title_text), FadeOut(main_text))

Scene1.narration_text = "Welcome to our educational video about linear algebra. Today we'll explore matrix multiplication and its applications."
Scene1.audio_duration = 5.0
