import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from src.templates.layouts import TitleAndMainContent

class Scene4(TitleAndMainContent):
    def construct_scene(self):
        # Create title text
        title_text = self.create_textbox("Scene 4", 
                                       self.title_region.width, 
                                       self.title_region.height, 
                                       font_size=36)
        title_text.move_to(self.title_region.get_center())
        
        # Create main content text  
        main_text = self.create_textbox("For example: (1,2) * (3,4) becomes (1*3) + (2*4) = 11. This '11' populates the corresponding cell in the resultant matrix. Repeat this for every row-column combination.", 
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

Scene4.narration_text = "For example: (1,2) * (3,4) becomes (1*3) + (2*4) = 11. This '11' populates the corresponding cell in the resultant matrix. Repeat this for every row-column combination."
Scene4.audio_duration = 5.0