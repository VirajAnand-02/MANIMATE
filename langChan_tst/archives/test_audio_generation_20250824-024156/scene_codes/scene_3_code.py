import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from manim import *
from src.templates.layouts import TitleAndMainContent
import numpy as np

class Scene3(TitleAndMainContent):
    def construct_scene(self):
        title_text = self.create_textbox("How Neural Networks Work", width=self.title_region.width * 0.8, height=self.title_region.height * 0.8)
        title_text.move_to(self.title_region.get_center())
        self.play(Write(title_text))
        self.wait(1)

        # Neural Network Diagram
        input_layer = VGroup(*[Circle(radius=0.2) for _ in range(5)]).arrange(DOWN).shift(LEFT * 3)
        hidden_layer1 = VGroup(*[Circle(radius=0.2) for _ in range(7)]).arrange(DOWN)
        hidden_layer2 = VGroup(*[Circle(radius=0.2) for _ in range(5)]).arrange(DOWN).shift(RIGHT * 3)
        output_layer = VGroup(*[Circle(radius=0.2) for _ in range(3)]).arrange(DOWN).shift(RIGHT * 6)

        layers = [input_layer, hidden_layer1, hidden_layer2, output_layer]

        input_text = Text("Text Input", font_size=24).next_to(input_layer, UP)
        output_text = Text("Audio Output", font_size=24).next_to(output_layer, UP)

        self.play(Create(input_layer), Write(input_text))
        self.play(Create(hidden_layer1))
        self.play(Create(hidden_layer2))
        self.play(Create(output_layer), Write(output_text))

        # Connections
        connections = VGroup()
        for i, layer in enumerate(layers[:-1]):
        next_layer = layers[i+1]
        for node1 in layer:
        for node2 in next_layer:
        line = Line(node1.get_center(), node2.get_center(), stroke_width=1, color=GREY)
        connections.add(line)

        self.play(Create(connections, run_time=2))

        # Data Flow Highlight
        for i in range(len(layers) - 1):
        for node1 in layers[i]:
        for node2 in layers[i+1]:
        line = Line(node1.get_center(), node2.get_center(), stroke_width=3, color=YELLOW)
        self.play(Create(line), run_time=0.2)
        self.play(FadeOut(line), run_time=0.1)
        self.wait(1)

        # Phoneme and Acoustic Feature Examples
        phoneme_example = Text("Phonemes: /k/, /æ/, /t/", font_size=20).to_corner(DL)
        acoustic_example = Text("Acoustic Features: Pitch, Tone", font_size=20).to_corner(DR)

        self.play(Write(phoneme_example), Write(acoustic_example))
        self.wait(2)

        everything = VGroup(title_text, input_layer, hidden_layer1, hidden_layer2, output_layer, input_text, output_text, connections, phoneme_example, acoustic_example)
        everything.scale(0.6)
        everything.move_to(self.main_region.get_center())

        self.wait(1)

# Set narration and duration
Scene3.narration_text = '''How does it work? Neural networks, specifically deep learning models, are trained on massive datasets of text and audio. These models learn the complex relationships between words, phonemes (the sounds of language), and acoustic features like pitch, tone, and rhythm.'''
Scene3.audio_duration = 5.0
