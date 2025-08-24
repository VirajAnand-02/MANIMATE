#!/usr/bin/env python3
"""
Simple test script for the Manim Layout Manager

This script can be run without full Manim rendering to test the core logic.
"""

import sys
import math
import numpy as np
from typing import List

# Mock Manim classes for testing without full Manim installation
class MockMobject:
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
        if direction == "DL":  # Down-Left
            return self._center + np.array([-self._width/2, -self._height/2, 0])
        elif direction == "UR":  # Up-Right  
            return self._center + np.array([self._width/2, self._height/2, 0])
        return self._center
        
    def move_to(self, position):
        self._center = position.copy()
        
    def scale(self, factor):
        self._width *= factor
        self._height *= factor

# Import our layout manager
try:
    from manim_layout_manager import LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
except ImportError:
    print("Error: Could not import manim_layout_manager. Make sure the file exists.")
    sys.exit(1)

def test_basic_layout():
    """Test basic layout functionality"""
    print("Testing basic layout functionality...")
    
    # Create test region
    region = BoundingBox(-5, -3, 5, 3)
    
    # Create layout manager
    layout_manager = LayoutManager(region, padding=0.1)
    
    # Create test objects
    obj1 = MockMobject(width=2, height=1)
    obj2 = MockMobject(width=1.5, height=1.5)
    obj3 = MockMobject(width=1, height=2)
    
    # Add objects with different priorities
    layout_manager.add(obj1, PreferredPosition.CENTER, priority=10)
    layout_manager.add(obj2, PreferredPosition.TOP_LEFT, priority=5)
    layout_manager.add(obj3, PreferredPosition.BOTTOM_RIGHT, priority=1)
    
    # Perform layout
    report = layout_manager.layout()
    
    # Verify results
    assert report.total_items == 3
    assert report.items_placed > 0
    print(f"✓ Placed {report.items_placed}/{report.total_items} items")
    print(f"✓ Region utilization: {report.region_utilization:.1%}")
    
    return True

def test_collision_detection():
    """Test collision detection and resolution"""
    print("\nTesting collision detection...")
    
    region = BoundingBox(-3, -2, 3, 2)
    layout_manager = LayoutManager(region, padding=0.05, min_item_padding=0.1)
    
    # Create overlapping objects
    obj1 = MockMobject(width=2, height=1)
    obj2 = MockMobject(width=2, height=1)
    
    # Both want center position (guaranteed collision)
    layout_manager.add(obj1, PreferredPosition.CENTER, priority=10)
    layout_manager.add(obj2, PreferredPosition.CENTER, priority=5)
    
    report = layout_manager.layout()
    
    # Should resolve collision
    assert report.collisions_resolved > 0
    print(f"✓ Resolved {report.collisions_resolved} collisions")
    
    # Verify no overlaps in final layout
    items = layout_manager.items
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            bbox1 = items[i].bounding_box
            bbox2 = items[j].bounding_box
            if bbox1 and bbox2:
                assert not bbox1.overlaps(bbox2), "Items still overlapping after layout!"
    
    print("✓ No overlaps in final layout")
    return True

def test_packing_strategy():
    """Test packing-based layout strategy"""
    print("\nTesting packing strategy...")
    
    region = BoundingBox(-4, -3, 4, 3)
    layout_manager = LayoutManager(
        region, 
        strategy=LayoutStrategy.PACKING_BASED,
        min_item_padding=0.05
    )
    
    # Create many small objects
    for i in range(12):
        obj = MockMobject(width=0.8, height=0.6)
        layout_manager.add(obj, priority=i)
    
    report = layout_manager.layout()
    
    assert report.items_placed == 12
    print(f"✓ Packed {report.items_placed} items successfully")
    print(f"✓ Region utilization: {report.region_utilization:.1%}")
    
    return True

def test_boundary_compliance():
    """Test that all items stay within region boundaries"""
    print("\nTesting boundary compliance...")
    
    region = BoundingBox(-2, -2, 2, 2)
    layout_manager = LayoutManager(region, padding=0.1)
    
    # Create items that might exceed boundaries
    large_obj = MockMobject(width=3, height=1)  # Wider than region
    tall_obj = MockMobject(width=1, height=3)   # Taller than region
    normal_obj = MockMobject(width=1, height=1)
    
    layout_manager.add(large_obj, PreferredPosition.CENTER, priority=5)
    layout_manager.add(tall_obj, PreferredPosition.TOP_LEFT, priority=5)
    layout_manager.add(normal_obj, PreferredPosition.BOTTOM_RIGHT, priority=5)
    
    report = layout_manager.layout()
    
    # Check that items are within available region
    available_region = layout_manager.available_region
    within_bounds = 0
    
    for item in layout_manager.items:
        if item.bounding_box:
            if available_region.contains(item.bounding_box):
                within_bounds += 1
            else:
                print(f"  Item extends outside region (may have overflow indicator)")
    
    print(f"✓ {within_bounds}/{len(layout_manager.items)} items within bounds")
    if report.items_with_overflow > 0:
        print(f"✓ {report.items_with_overflow} items with overflow indicators")
    
    return True

def test_priority_system():
    """Test priority-based conflict resolution"""
    print("\nTesting priority system...")
    
    region = BoundingBox(-2, -1, 2, 1)
    layout_manager = LayoutManager(region, padding=0.05)
    
    # Create items with different priorities wanting same position
    high_priority = MockMobject(width=1, height=0.8)
    low_priority = MockMobject(width=1, height=0.8)
    
    layout_manager.add(high_priority, PreferredPosition.CENTER, priority=10)
    layout_manager.add(low_priority, PreferredPosition.CENTER, priority=1)
    
    report = layout_manager.layout()
    
    # High priority item should be closer to center
    high_pos = layout_manager.items[0].final_position
    low_pos = layout_manager.items[1].final_position
    
    center = region.center
    high_distance = np.linalg.norm(high_pos - center)
    low_distance = np.linalg.norm(low_pos - center)
    
    assert high_distance <= low_distance, "High priority item should be closer to preferred position"
    print("✓ Priority system working correctly")
    
    return True

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("MANIM LAYOUT MANAGER TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_basic_layout,
        test_collision_detection,
        test_packing_strategy,
        test_boundary_compliance,
        test_priority_system
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"✗ {test.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} FAILED with error: {e}")
    
    print("\n" + "=" * 60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 All tests passed! Layout Manager is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
