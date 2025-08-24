# Scene 1 - Fallback Template Code
# Generated at: 2025-08-23 22:44:57

from layouts import TitleAndMainContent

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene 1", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox(r"""Welcome to our video on Matrix Multiplication! Matrices are powerful tools in mathematics, used in everything from computer graphics to solving complex equations. But how do we multiply them?""", 
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

Scene1.narration_text = r"""Welcome to our video on Matrix Multiplication! Matrices are powerful tools in mathematics, used in everything from computer graphics to solving complex equations. But how do we multiply them?"""
Scene1.audio_duration = 5.0