# Manim Community Edition: A Detailed Reference Guide

## 1. Manim Versions: A Critical Distinction

This reference focuses on **Manim Community Edition**. Different, incompatible versions exist. Ensure your code and environment match.

*   **Manim Community Edition (`manim`)**:
    *   **Identifier**: `from manim import Scene`
    *   **Package**: `manim` on PyPI.
    *   **Recommendation**: Use this version for stability, documentation, and community support.

*   **ManimGL (`manimgl`)**: The original 3Blue1Brown version.
    *   **Identifier**: `from manimlib import Scene`
    *   **Package**: `manimgl` on PyPI.

*   **ManimCairo (`manimlib`)**: Obsolete predecessor to ManimGL.
    *   **Identifier**: `from manimlib.imports import ...`
    *   **Package**: `manimlib` on PyPI.

## 2. Core Concepts

Manim animations are built from **Scenes**, **Mobjects**, and **Animations**.

### 2.1. Scenes
A `Scene` is the canvas for an animation. Your animation logic is defined within the `construct` method of a class that inherits from `Scene`.

*   **Default Canvas**: 16:9 aspect ratio, 8 Manim Units (MUs) high, ~14.22 MUs wide. Origin `(0,0,0)` is at the center.
*   **Entry Point**: The `construct` method. If misspelled, Manim renders a blank video.

**Example `Scene` Structure:**
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Animation code goes here
        circle = Circle()
        self.play(Create(circle))
        self.wait(1)
```

### 2.2. Mobjects (Mathematical Objects)
Mobjects are the visual elements on screen.

#### Common Mobject Types
*   **Shapes**: `Circle`, `Square`, `Triangle`, `Ellipse`, `Line`, `Arrow`, `Dot`, `Polygon`, `Rectangle`.
*   **Text & Formulas**:
    *   `Text`: Plain text (Pango). Supports international scripts.
    *   `MarkupText`: Rich text with PangoMarkup tags (e.g., `<b>`, `<span color='red'>`).
    *   `Tex`: General-purpose LaTeX.
    *   `MathTex`: LaTeX math expressions (auto-wrapped in a math environment).
*   **Grouping**: `VGroup` (for vector mobjects) and `Group` (general) bundle mobjects to be treated as a single unit.

#### Creating, Positioning, and Styling Mobjects

Mobjects are instantiated as Python objects. Position with methods like `.shift()`, `.move_to()`, `.next_to()`. Style with keyword arguments or setter methods.

**Common Style Properties**:
*   `color` / `stroke_color`: Stroke color.
*   `fill_color`: Fill color.
*   `fill_opacity`: Fill transparency (0.0 to 1.0).
*   `stroke_width`: Stroke thickness.
*   `stroke_opacity`: Stroke transparency.

```python
# Create a blue, semi-transparent square
square = Square(color=BLUE, fill_opacity=0.5)

# Position it 2 units to the left
square.shift(LEFT * 2)

# Create text above the square
text = Text("A Square").next_to(square, UP)

# Style an existing mobject
circle = Circle()
circle.set_fill(color=ORANGE, opacity=1.0)
circle.set_stroke(color=GREEN, width=10)
```

### 2.3. Animations
Animations are actions executed via `self.play()`.

#### The `.animate` Syntax
A simple way to animate a property change. It creates a `Transform` animation implicitly.

```python
class AnimateSyntaxExample(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=1)
        self.add(square) # Mobject must be on screen to be animated

        # Animate property changes
        self.play(square.animate.shift(LEFT))
        self.play(square.animate.set_fill(ORANGE))
        self.play(square.animate.scale(0.3))
        self.play(square.animate.rotate(PI / 4))
```

#### Animation Classes
For explicit control, use animation classes.

| Animation Type       | Description                                                 | Examples                               |
| -------------------- | ----------------------------------------------------------- | ------------------------------------------ |
| **Creation**         | Animate the drawing or appearance of a mobject.             | `Create(mobj)`, `Write(text)`, `DrawBorderThenFill(mobj)` |
| **Transformation**   | Morph one mobject into another.                             | `Transform(m1, m2)`, `ReplacementTransform(m1, m2)` |
| **Fading**           | Fade mobjects in or out.                                    | `FadeIn(mobj)`, `FadeOut(mobj)`      |
| **Movement**         | Animate movement along a specified path.                    | `MoveAlongPath(dot, path)`          |
| **Emphasis**         | Draw attention to a mobject.                                | `Indicate(mobj)`, `Circumscribe(mobj)`, `Flash(mobj)` |

**Example:**
```python
class TransformExample(Scene):
    def construct(self):
        formula = MathTex("f(x)=", "g(x)", "+", "h(x)")
        self.play(Write(formula))

        box1 = SurroundingRectangle(formula[1])
        box2 = SurroundingRectangle(formula[3])
        self.play(Create(box1))
        self.wait()
        # Transforms the first box into the second.
        self.play(ReplacementTransform(box1, box2))
        self.wait()
```

### 2.4. Updaters and `ValueTracker`
Updaters make mobjects change continuously on every frame.

*   `ValueTracker`: A container for a number that can be animated. Access its value with `.get_value()`.
*   `.add_updater(func)`: Attaches a function `func` to a mobject. The function is called every frame and must accept the mobject as its first argument (e.g., `lambda m: ...`).
*   `always_redraw(func)`: A function that wraps a mobject-generating function, causing it to be re-drawn on every frame.

**Example: A dynamically updating angle.**
```python
class UpdaterExample(Scene):
    def construct(self):
        theta_tracker = ValueTracker(110) # Initial angle in degrees
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)

        # Updater makes the line follow the ValueTracker's value
        line_moving.add_updater(
            lambda m: m.become(line1.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=LEFT
            )
        )

        # always_redraw is for mobjects whose shape depends on others
        angle_arc = always_redraw(
            lambda: Angle(line1, line_moving, radius=0.5)
        )
        angle_label = always_redraw(
            lambda: MathTex(f"{theta_tracker.get_value():.0f}^\\circ").next_to(angle_arc, RIGHT)
        )

        self.add(line1, line_moving, angle_arc, angle_label)
        self.wait()

        # Animate the ValueTracker itself
        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140), run_time=2)
        self.wait()
```

## 3. Graphing and Data Visualization

Manim provides `Axes` and `NumberPlane` for plotting.

*   **`Axes`**: A Cartesian coordinate system.
*   **`NumberPlane`**: A grid that spans the screen.
*   **`.plot(function)`**: An `Axes` method to plot a function.
*   **`.get_graph_label(graph, label)`**: Adds a label to a plot.
*   **`.get_area(graph, x_range)`**: Creates a shaded area under a curve.
*   **`.get_riemann_rectangles(graph, ...)`**: Creates Riemann rectangles.

**Example: Plotting Functions**
```python
class PlottingExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-10, 10.3, 1],  # [start, end, step]
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            axis_config={"color": GREEN},
        )
        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)
        sin_label = axes.get_graph_label(sin_graph, "\\sin(x)")
        cos_label = axes.get_graph_label(cos_graph, label="\\cos(x)")

        self.play(Create(axes), Create(sin_graph), Create(cos_graph))
        self.play(Write(sin_label), Write(cos_label))
        self.wait()
```

## 4. Camera and 3D Scenes

### 4.1. Moving Camera
Inherit from `MovingCameraScene` for camera control.

*   `self.camera.frame`: A mobject representing the camera's view. Animate it to zoom and pan.
*   `save_state()` / `restore()`: Use `self.camera.frame.save_state()` and `self.play(Restore(self.camera.frame))` to save and return to a camera position.

**Example: Camera Following a Dot**
```python
class FollowingCameraScene(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        ax = Axes(x_range=(0, 10), y_range=(0, 10))
        graph = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=(0, 3 * PI))
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE)

        self.add(ax, graph, moving_dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        # Attach camera to dot's position
        self.camera.frame.add_updater(lambda m: m.move_to(moving_dot))
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))
        self.camera.frame.remove_updater()

        self.play(Restore(self.camera.frame))
```

### 4.2. 3D Scenes
Inherit from `ThreeDScene` to work in 3D.

*   **3D Mobjects**: `Sphere`, `Cube`, `Cone`, `Surface`.
*   **Camera Orientation**: `self.set_camera_orientation(phi, theta, gamma)`
    *   `phi`: Polar angle from z-axis (e.g., `75 * DEGREES` for isometric-like view).
    *   `theta`: Azimuthal angle (rotation in xy-plane).
*   **Camera Animation**: `self.move_camera(...)` or `self.begin_ambient_camera_rotation(...)`.

**Example: 3D Surface Plot**
```python
class ThreeDPlot(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        axes = ThreeDAxes()
        surface = Surface(
            lambda u, v: np.array([u, v, np.sin(u) * np.cos(v)]),
            u_range=[-3, 3], v_range=[-3, 3],
            resolution=16
        )
        surface.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        self.add(axes, surface)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
```

## 5. Usage and Installation

### 5.1. Installation
Requires Python 3.8+, FFmpeg, and a LaTeX distribution (e.g., MiKTeX, TeX Live).

```bash
pip install manim
```

### 5.2. Rendering Scenes
Use the `manim` command in your terminal.

```bash
manim -pql my_scene_file.py MyScene
```

*   `my_scene_file.py`: Your Python script.
*   `MyScene`: The class name of the scene to render.

#### Common CLI Flags
*   `-p`, `--preview`: Play the video after rendering.
*   `-q`, `--quality`: `l` (low), `m` (medium), `h` (high), `k` (4K).
*   `-s`, `--save_last_frame`: Save the last frame as an image.
*   `-t`, `--transparent`: Render with a transparent background (`.mov`).
*   `--format <fmt>`: Render to a different format (e.g., `gif`).
*   `--renderer=opengl`: Use the experimental OpenGL renderer for real-time interaction.

## 6. Extending Manim: Plugins

Plugins are installable Python packages that add functionality.

*   **Finding Plugins**: https://plugins.manim.community/
*   **Installation**: `pip install <plugin-name>` (e.g., `pip install manim-voiceover`).
*   **Usage**: Enable in `manim.cfg` or with the `--plugins` flag.
    *   **In `manim.cfg`:**
        ```ini
        [CLI]
        plugins = manim_voiceover
        ```
    *   **Via command line:**
        ```bash
        manim --plugins "manim_voiceover" my_scene.py MyScene
        ```

## 7. Troubleshooting

*   **"no scenes inside that module"**:
    1.  Save your file.
    2.  Check for typos in the file and scene name in your command.
    3.  Ensure you're using the `manim` executable for ManimCE code.

*   **Black frame output**:
    *   You likely misspelled the `construct` method in your `Scene` class.

*   **Missing letters in `Tex`/`MathTex`**:
    *   LaTeX font cache issue. Rebuild your LaTeX distribution's font map (e.g., `fmtutil-sys --all` for TeX Live).

*   **How to find mobject arguments?**
    *   Check the documentation for the class and its parents (`Circle` inherits from `Arc`, `VMobject`, `Mobject`). `**kwargs` are passed up, so `VMobject` arguments like `fill_color` work for `Circle`.

*   **Getting Help**:
    *   **Discord**: Most active community.
    *   **StackOverflow**: Use the `manim` tag.
    *   **GitHub**: For bug reports (with a minimal reproducible example) and feature requests.

---

## Add-on: Manim Voiceover Plugin

A plugin to synchronize voiceovers with animations directly in Python.

**Usage:** Inherit from `VoiceoverScene` and use `self.set_speech_service()`.

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class VoiceoverExample(VoiceoverScene):
    def construct(self):
        # Prompts you to record audio with your mic during rendering
        self.set_speech_service(RecorderService())

        circle = Circle()

        # The animation's run_time is synced to the audio clip's duration
        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left.") as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)
```

---

## Add-on: Manim Configuration

Settings are managed via CLI flags, `manim.cfg` files, or the global `config` object.

### Configuration Files (`manim.cfg`)
Place a `manim.cfg` file in your project directory for persistent settings.

```ini
[CLI]
# Default render settings for this project
quality = h
background_color = #222222
preview = True
```

### Precedence Order (Lowest to Highest)
1.  Library-wide default config.
2.  User-wide config (`~/.config/manim/manim.cfg`).
3.  Folder-wide config (in the same directory as your script).
4.  Custom config file (`--config_file` flag).
5.  CLI flags (`-pqh`, `-c RED`).
6.  Programmatic changes in your script (`from manim import config; config.background_color = ...`).

### Accessing Config in Code
```python
from manim import config, Scene, Text

class ShowConfig(Scene):
    def construct(self):
        res = f"{config.pixel_width}x{config.pixel_height}"
        text = Text(f"Resolution: {res}")
        self.add(text)
```

---

## Add-on: Rendering Text and Formulas

### Pango (`Text`, `MarkupText`)
For fast, general-purpose text. No LaTeX required.

```python
class PangoTextExample(Scene):
    def construct(self):
        # Plain text with font styling
        text1 = Text("Hello", font="Noto Sans", slant=ITALIC)

        # Color parts of text using t2c (text-to-color)
        text2 = Text("Hello World", t2c={"[1:-1]": BLUE, "World": RED})

        # Use PangoMarkup for inline styling
        markup_text = MarkupText(
            f'This is <span fgcolor="{YELLOW}">yellow</span> and <b>bold</b>.'
        )

        # Disable ligatures for accurate character indexing
        text3 = Text("flow", disable_ligatures=True) # "f" and "l" are separate

        group = VGroup(text1, text2, markup_text, text3).arrange(DOWN, buff=0.8)
        self.add(group)
```

### LaTeX (`Tex`, `MathTex`)
For high-quality mathematical typesetting. Requires a LaTeX installation. Use raw strings (`r"..."`).

*   **`Tex`**: General LaTeX. Math must be in `$...$` or `$$...$$`.
*   **`MathTex`**: Automatically in a math environment.

```python
class LatexExample(Scene):
    def construct(self):
        # MathTex is for math-mode content
        euler_identity = MathTex(r"e^{i\pi} + 1 = 0", font_size=96)

        # Isolate parts for coloring/animation with {{...}}
        pythagorean = MathTex(r"{{a^2}} + {{b^2}} = {{c^2}}")
        pythagorean.get_part_by_tex("a^2").set_color(RED)
        pythagorean.get_part_by_tex("b^2").set_color(BLUE)
        pythagorean.get_part_by_tex("c^2").set_color(GREEN)

        self.add(VGroup(euler_identity, pythagorean).arrange(DOWN, buff=1))
```

#### Custom LaTeX Templates
Use `TexTemplate` to add packages or define custom preambles.

```python
class CustomLatexTemplate(Scene):
    def construct(self):
        my_template = TexTemplate()
        my_template.add_to_preamble(r"\usepackage{mathrsfs}") # For \mathscr
        fancy_h = Tex(
            r"$\mathscr{H} \rightarrow \mathbb{H}$",
            tex_template=my_template,
            font_size=144,
        )
        self.add(fancy_h)
```
