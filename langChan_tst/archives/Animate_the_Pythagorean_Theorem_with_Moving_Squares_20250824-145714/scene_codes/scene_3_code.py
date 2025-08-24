import sys
sys.path.append(r'C:\Users\isanham\Documents\temp\langChan_tst')
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
        main_text = self.create_textbox("Now for the exciting part! The Pythagorean Theorem states that the *sum* of these two areas, a² plus b², will exactly equal the area of a square built on the hypotenuse, c². Let's see it happen. Watch", 
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

Scene3.narration_text = "Now for the exciting part! The Pythagorean Theorem states that the *sum* of these two areas, a² plus b², will exactly equal the area of a square built on the hypotenuse, c². Let's see it happen. Watch"
Scene3.audio_duration = 5.0