import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene3(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene 3", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox("What makes a pendulum swing faster or slower? Surprisingly, for small angles, the mass of the bob *doesn't* affect the period! Neither does the amplitude. The two main factors are the length of the st", 
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

Scene3.narration_text = "What makes a pendulum swing faster or slower? Surprisingly, for small angles, the mass of the bob *doesn't* affect the period! Neither does the amplitude. The two main factors are the length of the st"
Scene3.audio_duration = 5.0