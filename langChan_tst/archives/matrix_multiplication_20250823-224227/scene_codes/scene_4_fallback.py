# Scene 4 - Fallback Template Code
# Generated at: 2025-08-23 22:48:01

from layouts import TitleAndMainContent

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene 4", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox(r"""Let's work through a quick example. Multiply a 2x2 matrix by another 2x2 matrix. The result will also be a 2x2 matrix. Take your time, practice, and soon you'll be multiplying matrices like a pro! Tha""", 
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

Scene4.narration_text = r"""Let's work through a quick example. Multiply a 2x2 matrix by another 2x2 matrix. The result will also be a 2x2 matrix. Take your time, practice, and soon you'll be multiplying matrices like a pro! Tha"""
Scene4.audio_duration = 5.0