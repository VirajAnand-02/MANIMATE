import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene5(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene 5", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox("Matrix multiplication is used in computer graphics, data analysis, and much more! Understanding this fundamental concept unlocks powerful applications. Thanks for watching!", 
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

Scene5.narration_text = "Matrix multiplication is used in computer graphics, data analysis, and much more! Understanding this fundamental concept unlocks powerful applications. Thanks for watching!"
Scene5.audio_duration = 5.0