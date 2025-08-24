# Manim Layout Manager

A comprehensive layout management system for Manim Community Edition that provides collision-free positioning and intelligent scaling of Mobjects within designated regions.

## Features

- **Collision-free placement** with configurable padding between objects
- **Multiple layout strategies**: constraint-based and packing-based algorithms
- **Priority-based conflict resolution** for complex layouts
- **Graceful fallbacks** for impossible layouts (scaling, repositioning, overflow indicators)
- **Detailed reporting** of all layout operations
- **Support for VGroups** - treats groups as single items transparently
- **Deterministic algorithms** - same input always produces same output
- **Performance optimized** for up to 200+ objects

## Core Algorithm

The layout manager uses a three-phase approach:

1. **Collision Detection**: Axis-aligned bounding boxes (AABB) detect overlaps between mobjects
2. **Constraint-based Resolution**: Honors preferred positions, then resolves conflicts by:
   - Small translations along shortest axis to minimize movement
   - Proportional scaling down while respecting minimum scale limits  
   - Priority-based ordering (higher priority items preserved)
3. **Graceful Fallbacks**: Creates overflow indicators for items too large even at minimum scale

The algorithm is deterministic and preserves spatial relationships while ensuring no overlaps.

## Quick Start

```python
from manim import *
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox

class MyScene(Scene):
    def construct(self):
        # Define layout region
        region = BoundingBox(-5, -3, 5, 3)  # x_min, y_min, x_max, y_max
        
        # Create layout manager
        layout_manager = LayoutManager(
            region=region,
            padding=0.1,
            strategy=LayoutStrategy.CONSTRAINT_BASED
        )
        
        # Add objects with preferred positions
        title = Text("My Title", font_size=48)
        formula = MathTex(r"E = mc^2", font_size=36)
        diagram = Circle(radius=1, color=BLUE)
        
        layout_manager.add(title, PreferredPosition.TOP_CENTER, priority=10)
        layout_manager.add(formula, PreferredPosition.CENTER, priority=8)
        layout_manager.add(diagram, PreferredPosition.BOTTOM_CENTER, priority=6)
        
        # Perform layout
        report = layout_manager.layout()
        
        # Display objects
        for item in layout_manager.items:
            self.add(item.mobject)
```

## API Reference

### LayoutManager

Main class for managing object layout within a region.

#### Constructor

```python
LayoutManager(
    region: BoundingBox,           # Layout region boundaries
    padding: float = 0.05,         # Padding around region edges
    strategy: LayoutStrategy = CONSTRAINT_BASED,  # Layout strategy
    min_item_padding: float = 0.02,  # Minimum padding between items
    overflow_indicator_color: str = RED,  # Color for overflow indicators
    max_iterations: int = 100       # Max iterations for conflict resolution
)
```

#### Methods

##### `add(mobject, preferred_position=None, priority=0, min_scale=0.1, max_scale=2.0)`

Add a mobject to be laid out.

**Parameters:**
- `mobject` (Mobject): The Manim object to add
- `preferred_position` (PreferredPosition or np.ndarray, optional): Desired position
- `priority` (int): Higher values get precedence in conflicts (default: 0)  
- `min_scale` (float): Minimum allowed scale factor (default: 0.1)
- `max_scale` (float): Maximum allowed scale factor (default: 2.0)

**Returns:** `LayoutItem` object for further configuration

##### `layout()`

Perform the layout operation.

**Returns:** `LayoutReport` with detailed information about operations performed

##### `get_debug_visuals()`

Get debug visualizations including bounding boxes and region outline.

**Returns:** `VGroup` containing all debug visual elements

##### `clear()`

Clear all items and reset the layout manager.

### PreferredPosition Enum

Predefined position constants:

- `CENTER`, `TOP_LEFT`, `TOP_CENTER`, `TOP_RIGHT`
- `CENTER_LEFT`, `CENTER_RIGHT`  
- `BOTTOM_LEFT`, `BOTTOM_CENTER`, `BOTTOM_RIGHT`
- `ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF` (relative to previous item)

### LayoutStrategy Enum

Available layout strategies:

- `CONSTRAINT_BASED`: Honors preferred positions, resolves conflicts intelligently
- `PACKING_BASED`: Grid/bin-packing approach for many small items

### BoundingBox

Represents a rectangular region for layout.

```python
BoundingBox(x_min: float, y_min: float, x_max: float, y_max: float)
```

**Properties:**
- `width`, `height`: Dimensions
- `center`: Center point as numpy array

**Methods:**
- `overlaps(other)`: Check overlap with another bounding box
- `contains(other)`: Check if fully contains another bounding box
- `expand_by_padding(padding)`: Return expanded bounding box

### LayoutReport

Detailed report of layout operations.

**Attributes:**
- `total_items`: Number of items processed
- `items_placed`: Number successfully placed
- `items_scaled`: Number that were scaled
- `items_moved`: Number that were repositioned
- `items_with_overflow`: Number that exceeded region bounds
- `collisions_resolved`: Number of collision conflicts resolved
- `strategy_used`: Layout strategy that was used
- `region_utilization`: Percentage of region area occupied
- `item_reports`: Per-item details list
- `warnings`: List of warning messages

## Layout Strategies

### Constraint-Based Strategy

Best for: Small to medium number of objects with specific positioning requirements

**Behavior:**
1. Places items at preferred positions
2. Detects and resolves collisions by translation and scaling
3. Respects priority ordering - higher priority items stay in place
4. Minimizes movement and scaling changes

**Use when:** You have specific spatial relationships to maintain (title above content, etc.)

### Packing-Based Strategy  

Best for: Many small objects where efficient space utilization is priority

**Behavior:**
1. Calculates optimal grid dimensions
2. Places items in grid cells
3. Scales items to fit cells if necessary
4. Orders by priority then size

**Use when:** You have many similar-sized items to display efficiently

## Configuration Options

### Padding Settings

- `padding`: Space between region edge and content (default: 0.05)
- `min_item_padding`: Minimum space between items (default: 0.02)

### Scale Limits

Set per-item when adding:
```python
layout_manager.add(
    my_object, 
    min_scale=0.1,  # Don't scale below 10% of original
    max_scale=2.0   # Don't scale above 200% of original
)
```

### Priority System

Higher priority items are preserved during conflict resolution:
```python
layout_manager.add(title, priority=10)    # Highest priority - won't be moved
layout_manager.add(content, priority=5)   # Medium priority  
layout_manager.add(footer, priority=1)    # Lowest priority - moved first
```

## Examples

### Example 1: Academic Presentation Layout

```python
class AcademicSlide(Scene):
    def construct(self):
        # Full screen region
        region = BoundingBox(
            -self.camera.frame_width/2 + 0.5,
            -self.camera.frame_height/2 + 0.5, 
            self.camera.frame_width/2 - 0.5,
            self.camera.frame_height/2 - 0.5
        )
        
        layout_manager = LayoutManager(region, padding=0.1)
        
        # Academic content
        title = Text("Research Findings", font_size=48)
        equation = MathTex(r"\nabla \cdot \vec{E} = \frac{\rho}{\epsilon_0}")
        graph = # ... create graph
        caption = Text("Figure 1: Field distribution")
        
        # Layout with priorities
        layout_manager.add(title, PreferredPosition.TOP_CENTER, priority=10)
        layout_manager.add(equation, PreferredPosition.CENTER, priority=8) 
        layout_manager.add(graph, PreferredPosition.BELOW, priority=6)
        layout_manager.add(caption, PreferredPosition.BELOW, priority=4)
        
        report = layout_manager.layout()
        
        # Animate in order
        for item in layout_manager.items:
            self.play(FadeIn(item.mobject))
```

### Example 2: Dashboard Layout

```python
class Dashboard(Scene):
    def construct(self):
        region = BoundingBox(-6, -4, 6, 4)
        
        # Use packing strategy for uniform grid
        layout_manager = LayoutManager(
            region, 
            strategy=LayoutStrategy.PACKING_BASED,
            min_item_padding=0.1
        )
        
        # Create dashboard widgets
        widgets = []
        for i in range(12):
            widget = VGroup(
                Rectangle(width=1, height=0.8, color=BLUE),
                Text(f"Widget {i+1}", font_size=16)
            )
            widgets.append(widget)
            layout_manager.add(widget, priority=i)
        
        report = layout_manager.layout()
        
        # Show all widgets
        for item in layout_manager.items:
            self.add(item.mobject)
```

## Testing and Validation

The package includes automated validation:

```python
# Run validation tests
validation_results = layout_manager._run_validation_tests()

# Check for issues
if not validation_results['overlap_test']:
    print("Warning: Objects are overlapping!")
    
if not validation_results['boundary_test']:
    print("Warning: Objects exceed region boundaries!")
```

Visual debugging:
```python
# Add debug visuals to scene
debug_group = layout_manager.get_debug_visuals()
self.add(debug_group)  # Shows bounding boxes and region outline
```

## Performance Notes

- **Constraint-based**: O(N²) collision detection, suitable for N < 50
- **Packing-based**: O(N log N) grid placement, suitable for N < 200  
- **Memory usage**: Minimal - only stores item metadata, not mobject copies
- **Deterministic**: Same input always produces same layout

## Error Handling

The layout manager gracefully handles edge cases:

1. **Items too large**: Creates red overflow indicators instead of crashing
2. **No space available**: Scales down items to minimum size
3. **Conflicting constraints**: Uses priority system to resolve
4. **Invalid positions**: Falls back to center placement

## Troubleshooting

### Objects Still Overlapping
- Increase `min_item_padding`
- Reduce `max_scale` for items
- Use higher priority for items that must stay in place

### Items Outside Region
- Increase region size or reduce `padding`
- Set higher `min_scale` values
- Check for overflow indicators

### Poor Space Utilization  
- Switch to `PACKING_BASED` strategy
- Reduce padding values
- Adjust item priorities

### Performance Issues
- Use `PACKING_BASED` for many items
- Reduce `max_iterations` if needed
- Consider splitting into multiple layout regions

## License

This module is designed for use with Manim Community Edition and follows its licensing terms.
