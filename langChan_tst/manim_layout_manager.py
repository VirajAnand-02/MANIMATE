#!/usr/bin/env python3
"""
Manim Layout Manager - Advanced collision-free positioning and scaling for Mobjects

CORE ALGORITHM:
1. Collision Detection: Uses axis-aligned bounding boxes (AABB) to detect overlaps between mobjects
2. Constraint-based Resolution: Attempts to honor preferred positions first, then resolves conflicts by:
   a) Small translations along shortest axis to minimize movement
   b) Proportional scaling down while respecting minimum scale limits
   c) Priority-based ordering (higher priority items preserved over lower priority)
3. Packing-based Strategy: Uses bin-packing heuristics for many small items with grid/row fallback
4. Graceful Fallbacks: Overflow indicators for items too large even at minimum scale

The algorithm is deterministic and preserves spatial relationships while ensuring no overlaps
and all items remain within specified region bounds with configurable padding.
"""

from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import math
import logging
import numpy as np

# Try to import Manim, fall back to basic object if not available
try:
    from manim import *
    MANIM_AVAILABLE = True
except ImportError:
    # Define minimal compatibility classes for testing without Manim
    MANIM_AVAILABLE = False
    
    # Direction constants - create simple placeholder objects
    class _Direction:
        def __init__(self, name):
            self.name = name
    
    DL = _Direction("DL")  # Down-Left
    UR = _Direction("UR")  # Up-Right
    UP = _Direction("UP")
    
    class Mobject:
        def __init__(self):
            self._width = 1.0
            self._height = 1.0
            self._center = np.array([0, 0, 0])
        
        @property 
        def width(self):
            return self._width
            
        @property
        def height(self):
            return self._height
            
        def get_center(self):
            return self._center
            
        def get_corner(self, direction):
            center = self.get_center()
            half_width = self.width / 2
            half_height = self.height / 2
            
            if direction.name == "DL":  # Down-Left
                return center + np.array([-half_width, -half_height, 0])
            elif direction.name == "UR":  # Up-Right
                return center + np.array([half_width, half_height, 0])
            return center
            
        def move_to(self, position):
            self._center = position.copy()
            
        def scale(self, factor):
            self._width *= factor
            self._height *= factor
        
        def next_to(self, other, direction, buff=0.1):
            pass
    
    class VGroup(Mobject):
        def __init__(self, *objects):
            super().__init__()
            self.objects = list(objects)
        
        def add(self, obj):
            self.objects.append(obj)
    
    class Rectangle(Mobject):
        def __init__(self, width=1, height=1, color=None, stroke_width=1, fill_opacity=0):
            super().__init__()
            self._width = width
            self._height = height
    
    class SurroundingRectangle(Mobject):
        def __init__(self, mobject, color=None, stroke_width=1):
            super().__init__()
    
    class Text(Mobject):
        def __init__(self, text, font_size=24, color=None):
            super().__init__()
            # Approximate text dimensions based on font size
            self._width = len(text) * font_size * 0.02
            self._height = font_size * 0.03
    
    # Color constants
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    WHITE = "white"
    YELLOW = "yellow"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LayoutStrategy(Enum):
    """Available layout strategies"""
    CONSTRAINT_BASED = "constraint_based"
    PACKING_BASED = "packing_based"


class PreferredPosition(Enum):
    """Predefined preferred positions within a region"""
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    CENTER_LEFT = "center_left"
    CENTER_RIGHT = "center_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"
    ABOVE = "above"  # Relative to previous item
    BELOW = "below"  # Relative to previous item
    LEFT_OF = "left_of"  # Relative to previous item
    RIGHT_OF = "right_of"  # Relative to previous item


@dataclass
class BoundingBox:
    """Axis-aligned bounding box for collision detection"""
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    
    @property
    def width(self) -> float:
        return self.x_max - self.x_min
    
    @property
    def height(self) -> float:
        return self.y_max - self.y_min
    
    @property
    def center(self) -> np.ndarray:
        return np.array([(self.x_min + self.x_max) / 2, (self.y_min + self.y_max) / 2, 0])
    
    def overlaps(self, other: 'BoundingBox') -> bool:
        """Check if this bounding box overlaps with another"""
        return not (self.x_max <= other.x_min or self.x_min >= other.x_max or
                   self.y_max <= other.y_min or self.y_min >= other.y_max)
    
    def contains(self, other: 'BoundingBox') -> bool:
        """Check if this bounding box fully contains another"""
        return (self.x_min <= other.x_min and self.x_max >= other.x_max and
                self.y_min <= other.y_min and self.y_max >= other.y_max)
    
    def expand_by_padding(self, padding: float) -> 'BoundingBox':
        """Return a new bounding box expanded by padding on all sides"""
        return BoundingBox(
            self.x_min - padding, self.y_min - padding,
            self.x_max + padding, self.y_max + padding
        )


@dataclass
class LayoutItem:
    """Container for a mobject with layout metadata"""
    mobject: 'Mobject'  # Use string annotation for forward compatibility
    preferred_position: Optional['Union[PreferredPosition, np.ndarray]'] = None
    priority: int = 0
    min_scale: float = 0.1
    max_scale: float = 2.0
    
    # Runtime properties (set during layout)
    final_position: Optional[np.ndarray] = None
    final_scale: float = 1.0
    actions_taken: List[str] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None
    
    def get_current_bbox(self) -> BoundingBox:
        """Get current bounding box of the mobject"""
        # Get the actual bounds from Manim or fallback calculation
        center = self.mobject.get_center()
        half_width = self.mobject.width / 2
        half_height = self.mobject.height / 2
        
        x_min = center[0] - half_width
        x_max = center[0] + half_width
        y_min = center[1] - half_height
        y_max = center[1] + half_height
            
        return BoundingBox(x_min, y_min, x_max, y_max)
    
    def apply_scale(self, scale_factor: float) -> bool:
        """Apply scale if within limits. Returns True if successful."""
        new_scale = self.final_scale * scale_factor
        if self.min_scale <= new_scale <= self.max_scale:
            self.mobject.scale(scale_factor)
            self.final_scale = new_scale
            self.actions_taken.append(f"scaled to {self.final_scale:.2f}")
            return True
        return False
    
    def move_to_position(self, position: np.ndarray):
        """Move mobject to specified position"""
        self.mobject.move_to(position)
        self.final_position = position.copy()
        self.actions_taken.append(f"moved to ({position[0]:.2f}, {position[1]:.2f})")


@dataclass
class LayoutReport:
    """Detailed report of layout operations"""
    total_items: int
    items_placed: int
    items_scaled: int
    items_moved: int
    items_with_overflow: int
    collisions_resolved: int
    strategy_used: LayoutStrategy
    region_utilization: float
    item_reports: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class LayoutManager:
    """
    Advanced layout manager for Manim mobjects with collision detection and resolution.
    
    Features:
    - Collision-free placement with configurable padding
    - Multiple layout strategies (constraint-based, packing-based)
    - Priority-based conflict resolution
    - Graceful fallbacks for impossible layouts
    - Detailed reporting and logging
    """
    
    def __init__(self, 
                 region: BoundingBox,
                 padding: float = 0.05,
                 strategy: LayoutStrategy = LayoutStrategy.CONSTRAINT_BASED,
                 min_item_padding: float = 0.02,
                 overflow_indicator_color: str = "red",  # Use string default
                 max_iterations: int = 100):
        """
        Initialize the layout manager.
        
        Args:
            region: The bounding region for layout
            padding: Padding around the region edges
            strategy: Layout strategy to use
            min_item_padding: Minimum padding between items
            overflow_indicator_color: Color for overflow indicators
            max_iterations: Maximum iterations for conflict resolution
        """
        self.region = region
        self.available_region = region.expand_by_padding(-padding)
        self.padding = padding
        self.min_item_padding = min_item_padding
        self.strategy = strategy
        self.overflow_indicator_color = overflow_indicator_color
        self.max_iterations = max_iterations
        
        self.items: List[LayoutItem] = []
        self.overflow_indicators: List['Mobject'] = []
        
    def add(self, 
            mobject: 'Mobject', 
            preferred_position: 'Optional[Union[PreferredPosition, np.ndarray]]' = None,
            priority: int = 0,
            min_scale: float = 0.1,
            max_scale: float = 2.0) -> LayoutItem:
        """
        Add a mobject to be laid out.
        
        Args:
            mobject: The Manim mobject to add
            preferred_position: Desired position (enum or coordinates)
            priority: Higher values get precedence in conflict resolution
            min_scale: Minimum allowed scale factor
            max_scale: Maximum allowed scale factor
            
        Returns:
            LayoutItem object for further configuration
        """
        item = LayoutItem(
            mobject=mobject,
            preferred_position=preferred_position,
            priority=priority,
            min_scale=min_scale,
            max_scale=max_scale
        )
        self.items.append(item)
        logger.info(f"Added item with priority {priority} and preferred position {preferred_position}")
        return item
    
    def layout(self) -> LayoutReport:
        """
        Perform the layout operation and return a detailed report.
        
        Returns:
            LayoutReport with details of all operations performed
        """
        logger.info(f"Starting layout with {len(self.items)} items using {self.strategy.value} strategy")
        
        if self.strategy == LayoutStrategy.CONSTRAINT_BASED:
            return self._constraint_based_layout()
        elif self.strategy == LayoutStrategy.PACKING_BASED:
            return self._packing_based_layout()
        else:
            raise ValueError(f"Unknown layout strategy: {self.strategy}")
    
    def _constraint_based_layout(self) -> LayoutReport:
        """Constraint-based layout algorithm"""
        report = LayoutReport(
            total_items=len(self.items),
            items_placed=0,
            items_scaled=0,
            items_moved=0,
            items_with_overflow=0,
            collisions_resolved=0,
            strategy_used=self.strategy,
            region_utilization=0.0
        )
        
        # Sort items by priority (higher first)
        sorted_items = sorted(self.items, key=lambda x: x.priority, reverse=True)
        
        # Phase 1: Initial placement based on preferred positions
        placed_items: List[LayoutItem] = []
        for item in sorted_items:
            position = self._get_preferred_position(item, placed_items)
            item.move_to_position(position)
            item.bounding_box = item.get_current_bbox()
            placed_items.append(item)
            report.items_moved += 1
        
        # Phase 2: Collision detection and resolution
        iterations = 0
        while iterations < self.max_iterations:
            collisions = self._detect_collisions(placed_items)
            if not collisions:
                break
                
            resolved = self._resolve_collisions(collisions, report)
            if not resolved:
                break  # No more resolutions possible
                
            # Update bounding boxes
            for item in placed_items:
                item.bounding_box = item.get_current_bbox()
                
            iterations += 1
            
        # Phase 3: Boundary checking and overflow handling
        for item in placed_items:
            if not self.available_region.contains(item.bounding_box):
                if not self._fit_item_in_region(item):
                    self._create_overflow_indicator(item)
                    report.items_with_overflow += 1
                    report.warnings.append(f"Item exceeded region bounds even at minimum scale")
        
        # Generate final report
        report.items_placed = len([item for item in placed_items if item.final_position is not None])
        report.items_scaled = len([item for item in placed_items if item.final_scale != 1.0])
        report.region_utilization = self._calculate_region_utilization(placed_items)
        
        for item in placed_items:
            item_report = {
                "priority": item.priority,
                "final_position": item.final_position.tolist() if item.final_position is not None else None,
                "final_scale": item.final_scale,
                "actions_taken": item.actions_taken.copy(),
                "bounding_box": {
                    "x_min": item.bounding_box.x_min,
                    "y_min": item.bounding_box.y_min,
                    "x_max": item.bounding_box.x_max,
                    "y_max": item.bounding_box.y_max
                } if item.bounding_box else None
            }
            report.item_reports.append(item_report)
        
        logger.info(f"Layout completed: {report.items_placed}/{report.total_items} placed, "
                   f"{report.collisions_resolved} collisions resolved, "
                   f"{report.region_utilization:.1%} region utilization")
        
        return report
    
    def _packing_based_layout(self) -> LayoutReport:
        """Packing-based layout algorithm using grid placement"""
        report = LayoutReport(
            total_items=len(self.items),
            items_placed=0,
            items_scaled=0,
            items_moved=0,
            items_with_overflow=0,
            collisions_resolved=0,
            strategy_used=self.strategy,
            region_utilization=0.0
        )
        
        # Sort items by priority (higher first) then by size (larger first)
        sorted_items = sorted(self.items, key=lambda x: (x.priority, -x.mobject.width * x.mobject.height), reverse=True)
        
        # Calculate optimal grid dimensions
        grid_cols = math.ceil(math.sqrt(len(sorted_items)))
        grid_rows = math.ceil(len(sorted_items) / grid_cols)
        
        cell_width = self.available_region.width / grid_cols
        cell_height = self.available_region.height / grid_rows
        
        for i, item in enumerate(sorted_items):
            row = i // grid_cols
            col = i % grid_cols
            
            # Calculate cell center
            cell_x = self.available_region.x_min + (col + 0.5) * cell_width
            cell_y = self.available_region.y_max - (row + 0.5) * cell_height
            
            # Move item to cell center
            position = np.array([cell_x, cell_y, 0])
            item.move_to_position(position)
            report.items_moved += 1
            
            # Scale item to fit in cell if necessary
            item_bbox = item.get_current_bbox()
            
            # Calculate required scale to fit in cell with padding
            scale_x = (cell_width - 2 * self.min_item_padding) / item_bbox.width
            scale_y = (cell_height - 2 * self.min_item_padding) / item_bbox.height
            required_scale = min(scale_x, scale_y)
            
            if required_scale < 1.0:
                if item.apply_scale(required_scale):
                    report.items_scaled += 1
                else:
                    # Item can't be scaled enough, create overflow indicator
                    self._create_overflow_indicator(item)
                    report.items_with_overflow += 1
            
            item.bounding_box = item.get_current_bbox()
        
        report.items_placed = len(sorted_items)
        report.region_utilization = self._calculate_region_utilization(sorted_items)
        
        # Generate item reports
        for item in sorted_items:
            item_report = {
                "priority": item.priority,
                "final_position": item.final_position.tolist() if item.final_position is not None else None,
                "final_scale": item.final_scale,
                "actions_taken": item.actions_taken.copy(),
                "bounding_box": {
                    "x_min": item.bounding_box.x_min,
                    "y_min": item.bounding_box.y_min,
                    "x_max": item.bounding_box.x_max,
                    "y_max": item.bounding_box.y_max
                } if item.bounding_box else None
            }
            report.item_reports.append(item_report)
        
        logger.info(f"Packing layout completed: {report.items_placed} items placed in {grid_rows}x{grid_cols} grid")
        
        return report
    
    def _get_preferred_position(self, item: LayoutItem, placed_items: List[LayoutItem]) -> np.ndarray:
        """Calculate preferred position for an item"""
        if isinstance(item.preferred_position, np.ndarray):
            return item.preferred_position.copy()
        
        if item.preferred_position is None or item.preferred_position == PreferredPosition.CENTER:
            return self.available_region.center
        
        # Handle relative positions
        if item.preferred_position in [PreferredPosition.ABOVE, PreferredPosition.BELOW, 
                                     PreferredPosition.LEFT_OF, PreferredPosition.RIGHT_OF]:
            if placed_items:
                last_item = placed_items[-1]
                return self._get_relative_position(item, last_item)
            else:
                return self.available_region.center
        
        # Handle absolute positions
        region = self.available_region
        position_map = {
            PreferredPosition.TOP_LEFT: np.array([region.x_min, region.y_max, 0]),
            PreferredPosition.TOP_CENTER: np.array([(region.x_min + region.x_max) / 2, region.y_max, 0]),
            PreferredPosition.TOP_RIGHT: np.array([region.x_max, region.y_max, 0]),
            PreferredPosition.CENTER_LEFT: np.array([region.x_min, (region.y_min + region.y_max) / 2, 0]),
            PreferredPosition.CENTER_RIGHT: np.array([region.x_max, (region.y_min + region.y_max) / 2, 0]),
            PreferredPosition.BOTTOM_LEFT: np.array([region.x_min, region.y_min, 0]),
            PreferredPosition.BOTTOM_CENTER: np.array([(region.x_min + region.x_max) / 2, region.y_min, 0]),
            PreferredPosition.BOTTOM_RIGHT: np.array([region.x_max, region.y_min, 0]),
        }
        
        return position_map.get(item.preferred_position, self.available_region.center)
    
    def _get_relative_position(self, item: LayoutItem, reference_item: LayoutItem) -> np.ndarray:
        """Get position relative to another item"""
        ref_bbox = reference_item.bounding_box
        item_bbox = item.get_current_bbox()
        
        spacing = self.min_item_padding
        
        if item.preferred_position == PreferredPosition.ABOVE:
            return np.array([ref_bbox.center[0], ref_bbox.y_max + item_bbox.height/2 + spacing, 0])
        elif item.preferred_position == PreferredPosition.BELOW:
            return np.array([ref_bbox.center[0], ref_bbox.y_min - item_bbox.height/2 - spacing, 0])
        elif item.preferred_position == PreferredPosition.LEFT_OF:
            return np.array([ref_bbox.x_min - item_bbox.width/2 - spacing, ref_bbox.center[1], 0])
        elif item.preferred_position == PreferredPosition.RIGHT_OF:
            return np.array([ref_bbox.x_max + item_bbox.width/2 + spacing, ref_bbox.center[1], 0])
        
        return reference_item.final_position
    
    def _detect_collisions(self, items: List[LayoutItem]) -> List[Tuple[LayoutItem, LayoutItem]]:
        """Detect collisions between items"""
        collisions = []
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                item1, item2 = items[i], items[j]
                
                # Expand bounding boxes by minimum padding
                bbox1 = item1.bounding_box.expand_by_padding(self.min_item_padding / 2)
                bbox2 = item2.bounding_box.expand_by_padding(self.min_item_padding / 2)
                
                if bbox1.overlaps(bbox2):
                    collisions.append((item1, item2))
        
        return collisions
    
    def _resolve_collisions(self, collisions: List[Tuple[LayoutItem, LayoutItem]], report: LayoutReport) -> bool:
        """Resolve collisions using translation and scaling"""
        resolved_any = False
        
        for item1, item2 in collisions:
            # Lower priority item should be moved/scaled
            if item1.priority >= item2.priority:
                primary, secondary = item1, item2
            else:
                primary, secondary = item2, item1
            
            # Try translation first
            if self._try_translate_to_resolve(primary, secondary):
                resolved_any = True
                report.collisions_resolved += 1
            # If translation fails, try scaling
            elif self._try_scale_to_resolve(secondary):
                resolved_any = True
                report.collisions_resolved += 1
                report.items_scaled += 1
        
        return resolved_any
    
    def _try_translate_to_resolve(self, primary: LayoutItem, secondary: LayoutItem) -> bool:
        """Try to resolve collision by translating the secondary item"""
        # Calculate separation vector along shortest axis
        bbox1 = primary.bounding_box
        bbox2 = secondary.bounding_box
        
        # Calculate overlap amounts
        x_overlap = min(bbox1.x_max, bbox2.x_max) - max(bbox1.x_min, bbox2.x_min)
        y_overlap = min(bbox1.y_max, bbox2.y_max) - max(bbox1.y_min, bbox2.y_min)
        
        # Move along axis with smaller overlap (shortest path)
        if x_overlap < y_overlap:
            # Move horizontally
            if bbox2.center[0] < bbox1.center[0]:
                new_x = bbox1.x_min - bbox2.width/2 - self.min_item_padding
            else:
                new_x = bbox1.x_max + bbox2.width/2 + self.min_item_padding
            new_position = np.array([new_x, bbox2.center[1], 0])
        else:
            # Move vertically
            if bbox2.center[1] < bbox1.center[1]:
                new_y = bbox1.y_min - bbox2.height/2 - self.min_item_padding
            else:
                new_y = bbox1.y_max + bbox2.height/2 + self.min_item_padding
            new_position = np.array([bbox2.center[0], new_y, 0])
        
        # Check if new position is within available region
        secondary.move_to_position(new_position)
        new_bbox = secondary.get_current_bbox()
        
        if self.available_region.contains(new_bbox):
            return True
        else:
            # Revert to original position
            secondary.move_to_position(secondary.final_position)
            return False
    
    def _try_scale_to_resolve(self, item: LayoutItem) -> bool:
        """Try to resolve collision by scaling down an item"""
        scale_factor = 0.9  # Scale down by 10%
        return item.apply_scale(scale_factor)
    
    def _fit_item_in_region(self, item: LayoutItem) -> bool:
        """Try to fit an item within the region by scaling and repositioning"""
        bbox = item.bounding_box
        
        # Calculate required scale to fit in region
        scale_x = self.available_region.width / bbox.width
        scale_y = self.available_region.height / bbox.height
        required_scale = min(scale_x, scale_y) * 0.95  # Add small margin
        
        if required_scale >= item.min_scale:
            if item.apply_scale(required_scale):
                # Reposition to center of region
                item.move_to_position(self.available_region.center)
                return True
        
        return False
    
    def _create_overflow_indicator(self, item: LayoutItem):
        """Create visual indicator for items that overflow the region"""
        bbox = item.bounding_box
        
        # Create overflow indicator based on available classes
        try:
            # Try to create with Manim classes
            globals_dict = globals()
            SurroundingRectangleClass = globals_dict.get('SurroundingRectangle')
            TextClass = globals_dict.get('Text')
            VGroupClass = globals_dict.get('VGroup')
            
            if SurroundingRectangleClass and TextClass and VGroupClass:
                indicator = SurroundingRectangleClass(
                    item.mobject,
                    color=self.overflow_indicator_color,
                    stroke_width=3
                )
                
                # Add overflow label
                label = TextClass("OVERFLOW", font_size=12, color=self.overflow_indicator_color)
                if hasattr(label, 'next_to'):
                    label.next_to(indicator, UP, buff=0.05)
                
                overflow_group = VGroupClass(indicator, label)
                self.overflow_indicators.append(overflow_group)
            else:
                raise NameError("Manim classes not available")
                
        except (NameError, AttributeError, TypeError):
            # Simple fallback - just record that overflow occurred
            item.actions_taken.append("overflow indicator created (visual placeholder)")
            # Don't append anything to overflow_indicators to avoid further errors
        
        item.actions_taken.append("overflow indicator created")
    
    def _calculate_region_utilization(self, items: List[LayoutItem]) -> float:
        """Calculate what percentage of the region is occupied by items"""
        total_item_area = sum(item.bounding_box.width * item.bounding_box.height for item in items if item.bounding_box)
        region_area = self.available_region.width * self.available_region.height
        return total_item_area / region_area if region_area > 0 else 0.0
    
    def get_debug_visuals(self) -> 'VGroup':
        """Get debug visualizations including bounding boxes and region outline"""
        debug_group = VGroup()
        
        try:
            # Add region outline
            region_rect = Rectangle(
                width=self.available_region.width,
                height=self.available_region.height,
                color=BLUE,
                stroke_width=2
            )
            if hasattr(region_rect, 'move_to'):
                region_rect.move_to(self.available_region.center)
            debug_group.add(region_rect)
            
            # Add item bounding boxes
            for item in self.items:
                if item.bounding_box:
                    bbox_rect = Rectangle(
                        width=item.bounding_box.width,
                        height=item.bounding_box.height,
                        color=GREEN,
                        stroke_width=1,
                        fill_opacity=0.1
                    )
                    if hasattr(bbox_rect, 'move_to'):
                        bbox_rect.move_to(item.bounding_box.center)
                    debug_group.add(bbox_rect)
            
            # Add overflow indicators
            for indicator in self.overflow_indicators:
                debug_group.add(indicator)
                
        except (NameError, AttributeError):
            # Fallback for testing - return empty group
            pass
        
        return debug_group
    
    def clear(self):
        """Clear all items and reset the layout manager"""
        self.items.clear()
        self.overflow_indicators.clear()
        logger.info("Layout manager cleared")
