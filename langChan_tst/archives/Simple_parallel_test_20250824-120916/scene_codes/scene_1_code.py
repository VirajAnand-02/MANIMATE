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
        # 1. Create the title text and place it in the title region
        title_text = self.create_textbox("Simple Parallel Testing", self.title_region.width, self.title_region.height)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text), run_time=2)
        self.wait(2)

        # --- Sequential Testing Setup ---
        # Define dimensions relative to the main_region
        main_width = self.main_region.width
        main_height = self.main_region.height

        conveyor_width_seq = main_width * 0.7
        conveyor_height_seq = main_height * 0.1
        product_side_seq = conveyor_height_seq * 0.8
        station_width_seq = conveyor_height_seq * 1.5
        station_height_seq = conveyor_height_seq * 1.2

        # Conveyor belt
        conveyor_seq = Rectangle(width=conveyor_width_seq, height=conveyor_height_seq, color=GRAY_D, fill_opacity=0.6, stroke_width=2)
        conveyor_seq.move_to(self.main_region.get_center() + DOWN * main_height * 0.15)

        # Product
        product_seq = Square(side_length=product_side_seq, color=BLUE, fill_opacity=1, stroke_width=0)
        product_seq.move_to(conveyor_seq.get_left() + RIGHT * product_seq.width / 2)

        # Test Station
        test_station_seq = Rectangle(width=station_width_seq, height=station_height_seq, color=RED_E, fill_opacity=0.7, stroke_width=2)
        test_station_seq.next_to(conveyor_seq.get_right(), RIGHT, buff=0.5)
        test_station_seq.align_to(conveyor_seq, DOWN)
        test_station_label_seq = Text("Test Station", font_size=24, color=WHITE).next_to(test_station_seq, UP, buff=0.1)

        # Clock (simple face and hand)
        clock_face = Circle(radius=0.3, color=WHITE, stroke_width=2)
        clock_hand = Line(clock_face.get_center(), clock_face.get_center() + UP * 0.2, color=WHITE, stroke_width=3)
        clock_group = VGroup(clock_face, clock_hand)
        clock_group.next_to(test_station_seq, UP, buff=0.5)

        # --- Sequential Animation ---
        self.play(
        Create(conveyor_seq),
        Create(test_station_seq),
        Write(test_station_label_seq),
        run_time=2
        )
        self.play(FadeIn(product_seq, shift=RIGHT), run_time=1)

        # Product moves towards the test station
        self.play(
        product_seq.animate.move_to(test_station_seq.get_center() + LEFT * (test_station_seq.width / 2 - product_seq.width / 2)),
        run_time=3,
        rate_func=linear
        ) 
        # Product moves into the station and clock appears
        self.play(
        product_seq.animate.move_to(test_station_seq.get_center()),
        Create(clock_group),
        run_time=2
        ) 

        # Clock ticks slowly to represent testing time
        self.play(
        Rotate(clock_hand, -PI, about_point=clock_face.get_center()), # Half turn
        run_time=5,
        rate_func=linear
        )
        self.wait(3) # Wait for narration about inefficiency

        # --- Parallel Testing Transition ---
        self.play(
        FadeOut(product_seq),
        FadeOut(conveyor_seq),
        FadeOut(test_station_seq),
        FadeOut(test_station_label_seq),
        FadeOut(clock_group),
        run_time=1.5
        )

        # --- Parallel Testing Setup ---
        num_paths = 3
        path_spacing = main_height * 0.25
        conveyor_length_parallel = main_width * 0.6
        conveyor_height_parallel = main_height * 0.08
        product_side_parallel = conveyor_height_parallel * 0.8
        station_width_parallel = conveyor_height_parallel * 1.5
        station_height_parallel = conveyor_height_parallel * 1.2

        parallel_elements = VGroup()
        products_to_animate = VGroup()
        test_stations_to_animate = VGroup()

        for i in range(num_paths):
        y_offset = (i - (num_paths - 1) / 2) * path_spacing

        current_conveyor = Rectangle(width=conveyor_length_parallel, height=conveyor_height_parallel, color=GRAY_D, fill_opacity=0.6, stroke_width=2)
        current_conveyor.move_to(self.main_region.get_center() + UP * y_offset)

        current_product = Square(side_length=product_side_parallel, color=BLUE, fill_opacity=1, stroke_width=0)
        current_product.move_to(current_conveyor.get_left() + RIGHT * current_product.width / 2)

        current_test_station = Rectangle(width=station_width_parallel, height=station_height_parallel, color=RED_E, fill_opacity=0.7, stroke_width=2)
        current_test_station.next_to(current_conveyor.get_right(), RIGHT, buff=0.5)
        current_test_station.align_to(current_conveyor, DOWN)
        current_station_label = Text("Test Station", font_size=20, color=WHITE).next_to(current_test_station, UP, buff=0.1)

        parallel_elements.add(current_conveyor, current_product, current_test_station, current_station_label)
        products_to_animate.add(current_product)
        test_stations_to_animate.add(current_test_station)

        # Re-create clock for parallel section, place it centrally above the parallel paths
        parallel_clock_face = Circle(radius=0.3, color=WHITE, stroke_width=2)
        parallel_clock_hand = Line(parallel_clock_face.get_center(), parallel_clock_face.get_center() + UP * 0.2, color=WHITE, stroke_width=3)
        parallel_clock_group = VGroup(parallel_clock_face, parallel_clock_hand)
        parallel_clock_group.move_to(self.main_region.get_top() + DOWN * 0.5)


        self.play(
        FadeIn(parallel_elements),
        Create(parallel_clock_group),
        run_time=2.5
        )
        self.wait(1)

        # --- Parallel Animation ---
        # Animate all products moving towards their respective test stations simultaneously
        animations_move_to_pre_station = []
        for i in range(num_paths):
        animations_move_to_pre_station.append(
        products_to_animate[i].animate.move_to(test_stations_to_animate[i].get_center() + LEFT * (test_stations_to_animate[i].width / 2 - products_to_animate[i].width / 2))
        )
        self.play(*animations_move_to_pre_station, run_time=2.5, rate_func=linear)

        # Animate all products moving into their stations, and the clock ticks faster
        animations_move_into_station = []
        for i in range(num_paths):
        animations_move_into_station.append(
        products_to_animate[i].animate.move_to(test_stations_to_animate[i].get_center())
        )
        self.play(
        *animations_move_into_station,
        Rotate(parallel_clock_hand, -PI * 2, about_point=parallel_clock_face.get_center()), # Full rotation, faster
        run_time=2.5,
        rate_func=linear
        )
        self.wait(8) # Wait for narration about increased efficiency and speed

        # Final fade out of all elements
        self.play(
        FadeOut(title_text),
        FadeOut(parallel_elements),
        FadeOut(parallel_clock_group),
        run_time=1
        )

# Set narration and duration
Scene1.narration_text = '''Welcome to our quick guide on Simple Parallel Testing! In today\'s fast-paced manufacturing and development world, testing can often be a bottleneck. Traditional sequential testing, where you test one item after another, can be slow and inefficient, especially when dealing with high volumes. But what if you could test multiple products simultaneously, drastically cutting down your overall test time? That\'s exactly what simple parallel testing allows you to do – increasing your efficiency and speeding up your entire production or validation process. Let\'s dive in!'''
Scene1.audio_duration = 5.0
