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
        main_text = self.create_textbox("From ancient timekeeping to modern science, simple pendulums have played a vital role. They are the heart of many grandfather clocks and metronomes, providing a steady beat. Seismographs use pendulums", 
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

Scene4.narration_text = "From ancient timekeeping to modern science, simple pendulums have played a vital role. They are the heart of many grandfather clocks and metronomes, providing a steady beat. Seismographs use pendulums"
Scene4.audio_duration = 5.0