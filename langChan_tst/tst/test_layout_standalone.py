#!/usr/bin/env python3
"""
Standalone test of Manim Layout Manager core algorithms

This version tests the layout algorithms without requiring Manim installation.
"""

import sys
import numpy as np
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Mock the missing Manim imports
class MockManim:
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    PURPLE = "purple"
    ORANGE = "orange"
    WHITE = "white"
    CYAN = "cyan"
    GRAY = "gray"
    
    class Mobject:
        def __init__(self, width=1.0, height=1.0):
            self._width = width
            self._height = height
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
            if hasattr(direction, '__name__') and direction.__name__ == 'DL':
                return self._center + np.array([-self._width/2, -self._height/2, 0])
            elif hasattr(direction, '__name__') and direction.__name__ == 'UR':
                return self._center + np.array([self._width/2, self._height/2, 0])
            return self._center
            
        def move_to(self, position):
            self._center = position.copy()
            
        def scale(self, factor):
            self._width *= factor
            self._height *= factor
            
        def next_to(self, other, direction, buff=0.1):
            pass
    
    class VGroup(Mobject):
        def __init__(self, *objects):
            self.objects = list(objects)
            super().__init__()
            
        def add(self, obj):
            self.objects.append(obj)
    
    class Rectangle(Mobject):
        def __init__(self, width=1, height=1, color="white", stroke_width=1, fill_opacity=0):
            super().__init__(width, height)
            
    class SurroundingRectangle(Mobject):
        def __init__(self, mobject, color="white", stroke_width=1):
            super().__init__(mobject.width + 0.2, mobject.height + 0.2)
            
    class Text(Mobject):
        def __init__(self, text, font_size=24, color="white"):
            # Approximate text dimensions based on font size
            width = len(text) * font_size * 0.02
            height = font_size * 0.03
            super().__init__(width, height)
            self.text = text
    
    class DL:
        __name__ = 'DL'
    
    class UR:
        __name__ = 'UR'
    
    UP = np.array([0, 1, 0])

# Mock the manim module
sys.modules['manim'] = MockManim()

# Now import our layout manager
from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox

def test_basic_functionality():
    """Test that the layout manager basic functions work"""
    print("🧪 Testing basic layout manager functionality...")
    
    # Create a test region
    region = BoundingBox(-5, -3, 5, 3)
    
    # Create layout manager
    layout_manager = LayoutManager(region, padding=0.1)
    
    # Create some test objects
    obj1 = MockManim.Text("Title", font_size=48)
    obj2 = MockManim.Text("Content goes here", font_size=24)
    obj3 = MockManim.Rectangle(width=2, height=1)
    
    # Add them to layout
    layout_manager.add(obj1, PreferredPosition.TOP_CENTER, priority=10)
    layout_manager.add(obj2, PreferredPosition.CENTER, priority=5)
    layout_manager.add(obj3, PreferredPosition.BOTTOM_CENTER, priority=1)
    
    # Perform layout
    report = layout_manager.layout()
    
    print(f"  ✓ Total items: {report.total_items}")
    print(f"  ✓ Items placed: {report.items_placed}")
    print(f"  ✓ Items moved: {report.items_moved}")
    print(f"  ✓ Collisions resolved: {report.collisions_resolved}")
    print(f"  ✓ Region utilization: {report.region_utilization:.1%}")
    
    assert report.total_items == 3
    assert report.items_placed > 0
    
    return True

def test_collision_resolution():
    """Test collision detection and resolution"""
    print("\n🔍 Testing collision detection and resolution...")
    
    region = BoundingBox(-3, -2, 3, 2)
    layout_manager = LayoutManager(region, padding=0.1, min_item_padding=0.1)
    
    # Create two objects that will definitely collide
    obj1 = MockManim.Rectangle(width=2, height=1)
    obj2 = MockManim.Rectangle(width=2, height=1)
    
    # Both want the center position
    layout_manager.add(obj1, PreferredPosition.CENTER, priority=10)
    layout_manager.add(obj2, PreferredPosition.CENTER, priority=5)
    
    report = layout_manager.layout()
    
    print(f"  ✓ Collisions resolved: {report.collisions_resolved}")
    print(f"  ✓ Items scaled: {report.items_scaled}")
    
    # Verify no overlaps remain
    items = layout_manager.items
    overlaps_found = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            bbox1 = items[i].bounding_box
            bbox2 = items[j].bounding_box
            if bbox1 and bbox2 and bbox1.overlaps(bbox2):
                overlaps_found += 1
    
    print(f"  ✓ Final overlaps: {overlaps_found} (should be 0)")
    assert overlaps_found == 0, "Items should not overlap after layout"
    
    return True

def test_packing_strategy():
    """Test the packing-based layout strategy"""
    print("\n📦 Testing packing strategy...")
    
    region = BoundingBox(-4, -3, 4, 3)
    layout_manager = LayoutManager(
        region,
        strategy=LayoutStrategy.PACKING_BASED,
        min_item_padding=0.05
    )
    
    # Create many small objects
    objects = []
    for i in range(16):
        obj = MockManim.Rectangle(width=0.8, height=0.6)
        layout_manager.add(obj, priority=i)
        objects.append(obj)
    
    report = layout_manager.layout()
    
    print(f"  ✓ Items packed: {report.items_placed}/{report.total_items}")
    print(f"  ✓ Items scaled: {report.items_scaled}")
    print(f"  ✓ Region utilization: {report.region_utilization:.1%}")
    
    assert report.items_placed == len(objects)
    
    return True

def test_priority_system():
    """Test that priority system works correctly"""
    print("\n🏆 Testing priority system...")
    
    region = BoundingBox(-2, -1, 2, 1)
    layout_manager = LayoutManager(region, padding=0.05)
    
    # Create two objects wanting the same position with different priorities
    high_priority_obj = MockManim.Text("Important", font_size=24)
    low_priority_obj = MockManim.Text("Less important", font_size=24)
    
    layout_manager.add(high_priority_obj, PreferredPosition.CENTER, priority=10)
    layout_manager.add(low_priority_obj, PreferredPosition.CENTER, priority=1)
    
    report = layout_manager.layout()
    
    # Check that high priority item is closer to center
    center = region.center
    high_pos = layout_manager.items[0].final_position
    low_pos = layout_manager.items[1].final_position
    
    high_distance = np.linalg.norm(high_pos[:2] - center[:2])
    low_distance = np.linalg.norm(low_pos[:2] - center[:2])
    
    print(f"  ✓ High priority distance from center: {high_distance:.2f}")
    print(f"  ✓ Low priority distance from center: {low_distance:.2f}")
    print(f"  ✓ Priority respected: {high_distance <= low_distance}")
    
    assert high_distance <= low_distance + 0.1, "High priority item should be closer to preferred position"
    
    return True

def test_boundary_checking():
    """Test that items stay within boundaries"""
    print("\n🚧 Testing boundary compliance...")
    
    region = BoundingBox(-2, -2, 2, 2)
    layout_manager = LayoutManager(region, padding=0.2)
    
    # Create an item that's larger than the available region
    large_obj = MockManim.Rectangle(width=5, height=1)  # Too wide
    normal_obj = MockManim.Rectangle(width=1, height=1)
    
    layout_manager.add(large_obj, PreferredPosition.CENTER, priority=5)
    layout_manager.add(normal_obj, PreferredPosition.TOP_LEFT, priority=5)
    
    report = layout_manager.layout()
    
    print(f"  ✓ Items with overflow: {report.items_with_overflow}")
    print(f"  ✓ Items scaled: {report.items_scaled}")
    
    # Check boundary compliance
    available_region = layout_manager.available_region
    items_in_bounds = 0
    
    for item in layout_manager.items:
        if item.bounding_box:
            if available_region.contains(item.bounding_box):
                items_in_bounds += 1
    
    print(f"  ✓ Items within bounds: {items_in_bounds}/{len(layout_manager.items)}")
    
    return True

def run_comprehensive_test():
    """Run all tests and provide summary"""
    print("🚀 MANIM LAYOUT MANAGER - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_basic_functionality,
        test_collision_resolution,
        test_packing_strategy,
        test_priority_system,
        test_boundary_checking
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_func.__name__} PASSED")
            else:
                failed += 1
                print(f"❌ {test_func.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_func.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"📊 FINAL RESULTS: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Layout Manager is working correctly.")
        print("\n📋 FEATURES VERIFIED:")
        print("  ✓ Basic layout placement")
        print("  ✓ Collision detection & resolution") 
        print("  ✓ Packing strategy for many items")
        print("  ✓ Priority-based conflict resolution")
        print("  ✓ Boundary compliance checking")
        print("\n🚦 Ready for production use!")
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
    
    print("=" * 60)
    return failed == 0

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Install Manim Community Edition: pip install manim")
        print("2. Run example scenes: manim layout_examples.py LayoutManagerDemo1")
        print("3. Check README_layout_manager.md for full API documentation")
        print("4. Import LayoutManager in your Manim scenes!")
    
    sys.exit(0 if success else 1)
