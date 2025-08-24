# Scene 1 - Final Combined Code
# Layout: title_and_main_content
# Generated at: 2025-08-23 22:33:10

import sys
sys.path.append('..')
from layouts import TitleAndMainContent

class Scene1(TitleAndMainContent):
    def construct_scene(self):
        title_text = "Understanding Matrix Multiplication"
        title_box = self.create_textbox(title_text, width=self.title_region.width * 0.9, height=self.title_region.height * 0.8)
        title_box.move_to(self.title_region.get_center())
        
        self.play(Write(title_box))
        self.wait(2)
        self.play(FadeOut(title_box))
        self.wait(0.5)
        
        m1 = Matrix([["a", "b"], ["c", "d"]]).scale(0.8)
        m2 = Matrix([["x"], ["y"]]).scale(0.8)
        m3 = Matrix([["1", "0", "2"], ["-1", "3", "1"], ["5", "2", "1"]]).scale(0.8)
        
        matrices = VGroup(m1, m2, m3).arrange(RIGHT, buff=1.5).move_to(self.main_region.get_center())
        self.play(LaggedStart(
            FadeIn(m1, shift=UP),
            FadeIn(m2),
            FadeIn(m3, shift=DOWN),
            lag_ratio=0.5
        ))
        self.wait(1.5)
        self.play(FadeOut(matrices))
        self.wait(0.5)
        
        flash_scale = 0.8
        flash_wait_time = 0.25
        
        # Flash 1: Computer Graphics
        cube = Cube(side_length=2, fill_opacity=0.6, stroke_width=2, fill_color=BLUE)
        cube_label = Text("Computer Graphics").next_to(cube, DOWN)
        graphic_group = VGroup(cube, cube_label).scale(flash_scale).move_to(self.main_region.get_center())
        
        self.play(FadeIn(graphic_group, scale=0.5))
        self.play(Rotate(cube, angle=PI, axis=UP, run_time=1.5))
        self.play(FadeOut(graphic_group, scale=1.5))
        self.wait(flash_wait_time)
        
        # Flash 2: Data Science
        table = Table(
            [["7.1", "5.9", "4.8"],
             ["6.4", "2.1", "5.5"],
             ["3.3", "1.8", "6.2"]],
            include_outer_lines=True).scale(0.8)
        table_label = Text("Data Science").next_to(table, DOWN)
        data_group = VGroup(table, table_label).scale(flash_scale).move_to(self.main_region.get_center())
        row_highlight = SurroundingRectangle(table.get_rows()[1], color=YELLOW, buff=0.1)
        
        self.play(FadeIn(data_group, scale=0.5))
        self.play(Create(row_highlight))
        self.play(row_highlight.animate.move_to(table.get_columns()[1].get_center()), run_time=1.0)
        self.play(FadeOut(data_group, scale=1.5), FadeOut(row_highlight))
        self.wait(flash_wait_time)
        
        # Flash 3: Physics Simulation
        sun = Dot(color=YELLOW, radius=0.25)
        orbit = Circle(radius=2, color=GRAY)
        planet = Dot(color=BLUE, radius=0.1)
        planet.move_to(orbit.point_from_alpha(0))
        physics_label = Text("Physics").next_to(orbit, DOWN)
        physics_group = VGroup(sun, orbit, physics_label, planet).scale(flash_scale).move_to(self.main_region.get_center())
        
        self.play(FadeIn(VGroup(sun, orbit, physics_label), scale=0.5))
        self.add(planet)
        self.play(MoveAlongPath(planet, orbit), run_time=2, rate_func=linear)
        self.play(FadeOut(physics_group, scale=1.5))
        self.wait(1)

Scene1.narration_text = """Welcome to this video on matrix multiplication, a fundamental operation in linear algebra with wide-ranging applications in computer graphics, data science, and physics."""
Scene1.audio_duration = 12.010958
