#!/usr/bin/env python3
"""
Manim Layout Manager Examples and Tests

This file contains example scenes demonstrating the layout manager's capabilities
and automated tests to verify collision-free placement and boundary constraints.
"""

from manim import *
from manim_layout_manager import (
    LayoutManager, LayoutStrategy, PreferredPosition, BoundingBox
)
import random
import numpy as np


class LayoutManagerDemo1(Scene):
    """
    Demo Scene 1: Small number of large objects with preferred positioning
    
    Demonstrates:
    - Title at top, formula in center, diagram at bottom
    - Automatic scaling to fit
    - Preferred position handling
    """
    
    def construct(self):
        # Define the layout region (most of the screen)
        camera_width = self.camera.frame_width
        camera_height = self.camera.frame_height
        
        region = BoundingBox(
            x_min=-camera_width/2 + 1,
            y_min=-camera_height/2 + 1,
            x_max=camera_width/2 - 1,
            y_max=camera_height/2 - 1
        )
        
        # Create layout manager
        layout_manager = LayoutManager(
            region=region,
            padding=0.1,
            strategy=LayoutStrategy.CONSTRAINT_BASED
        )
        
        # Create large objects
        title = Text("Advanced Mathematics", font_size=48, color=BLUE)
        
        formula = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
            font_size=36,
            color=WHITE
        )
        
        # Create a complex diagram
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 1, 0.5],
            x_length=4,
            y_length=2,
            tips=False
        )
        
        func = axes.plot(lambda x: np.exp(-x**2) / np.sqrt(np.pi), color=YELLOW)
        diagram = VGroup(axes, func)
        
        # Add description
        description = Text(
            "This demonstrates automatic layout\nof mathematical content",
            font_size=24,
            color=GRAY
        )
        
        # Add items to layout manager with priorities
        layout_manager.add(title, PreferredPosition.TOP_CENTER, priority=10)
        layout_manager.add(formula, PreferredPosition.CENTER, priority=8)
        layout_manager.add(diagram, PreferredPosition.BOTTOM_CENTER, priority=6)
        layout_manager.add(description, PreferredPosition.BOTTOM_LEFT, priority=4)
        
        # Perform layout
        report = layout_manager.layout()
        
        # Display the laid out objects
        for item in layout_manager.items:
            self.add(item.mobject)
        
        # Show debug visualizations
        debug_visuals = layout_manager.get_debug_visuals()
        self.add(debug_visuals)
        
        # Display layout report
        report_text = self._create_report_text(report)
        report_text.to_corner(UR)
        self.add(report_text)
        
        self.wait(3)
    
    def _create_report_text(self, report) -> Text:
        """Create a text summary of the layout report"""
        summary = f"Layout Report:\n"
        summary += f"Items: {report.items_placed}/{report.total_items}\n"
        summary += f"Scaled: {report.items_scaled}\n"
        summary += f"Moved: {report.items_moved}\n"
        summary += f"Collisions: {report.collisions_resolved}\n"
        summary += f"Utilization: {report.region_utilization:.1%}\n"
        summary += f"Strategy: {report.strategy_used.value}"
        
        return Text(summary, font_size=16, color=YELLOW)


class LayoutManagerDemo2(Scene):
    """
    Demo Scene 2: Many small objects using packing strategy
    
    Demonstrates:
    - Grid-based packing algorithm
    - Automatic scaling for many items
    - Priority-based ordering
    """
    
    def construct(self):
        # Define layout region
        camera_width = self.camera.frame_width
        camera_height = self.camera.frame_height
        
        region = BoundingBox(
            x_min=-camera_width/2 + 0.5,
            y_min=-camera_height/2 + 0.5,
            x_max=camera_width/2 - 0.5,
            y_max=camera_height/2 - 0.5
        )
        
        # Create layout manager with packing strategy
        layout_manager = LayoutManager(
            region=region,
            padding=0.05,
            strategy=LayoutStrategy.PACKING_BASED,
            min_item_padding=0.02
        )
        
        # Create many small objects with random properties
        random.seed(42)  # For deterministic results
        
        objects = []
        for i in range(24):
            # Random geometric shapes
            shape_type = random.choice(['circle', 'square', 'triangle'])
            color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE])
            
            if shape_type == 'circle':
                obj = Circle(radius=random.uniform(0.1, 0.3), color=color, fill_opacity=0.7)
            elif shape_type == 'square':
                size = random.uniform(0.2, 0.6)
                obj = Square(side_length=size, color=color, fill_opacity=0.7)
            else:  # triangle
                obj = Triangle(color=color, fill_opacity=0.7).scale(random.uniform(0.3, 0.8))
            
            # Add label
            label = Text(f"{i+1}", font_size=12, color=WHITE)
            labeled_obj = VGroup(obj, label)
            
            # Random priority
            priority = random.randint(1, 5)
            
            layout_manager.add(labeled_obj, priority=priority)
            objects.append(labeled_obj)
        
        # Perform layout
        report = layout_manager.layout()
        
        # Display all objects
        for item in layout_manager.items:
            self.add(item.mobject)
        
        # Show debug visualizations
        debug_visuals = layout_manager.get_debug_visuals()
        self.add(debug_visuals)
        
        # Create and display report
        report_text = self._create_packing_report(report)
        report_text.to_corner(UL)
        self.add(report_text)
        
        self.wait(4)
    
    def _create_packing_report(self, report) -> Text:
        """Create a detailed packing report"""
        summary = f"Packing Report:\n"
        summary += f"Total Items: {report.total_items}\n"
        summary += f"Successfully Placed: {report.items_placed}\n"
        summary += f"Items Scaled: {report.items_scaled}\n"
        summary += f"Overflow Items: {report.items_with_overflow}\n"
        summary += f"Region Utilization: {report.region_utilization:.1%}\n"
        summary += f"Strategy: {report.strategy_used.value}"
        
        return Text(summary, font_size=14, color=CYAN)


class LayoutManagerValidationScene(Scene):
    """
    Validation Scene: Automated tests for collision detection and boundary compliance
    
    This scene creates a complex layout and then programmatically verifies:
    1. No overlaps between any items
    2. All items within region bounds
    3. Proper padding respected
    """
    
    def construct(self):
        # Define test region
        region = BoundingBox(-5, -3, 5, 3)
        
        layout_manager = LayoutManager(
            region=region,
            padding=0.1,
            strategy=LayoutStrategy.CONSTRAINT_BASED,
            min_item_padding=0.05
        )
        
        # Create test objects with challenging constraints
        test_objects = [
            (Circle(radius=0.8, color=RED, fill_opacity=0.5), PreferredPosition.CENTER, 10),
            (Square(side_length=1.2, color=BLUE, fill_opacity=0.5), PreferredPosition.TOP_LEFT, 8),
            (Triangle(color=GREEN, fill_opacity=0.5).scale(1.5), PreferredPosition.TOP_RIGHT, 8),
            (Rectangle(width=2, height=0.8, color=YELLOW, fill_opacity=0.5), PreferredPosition.BOTTOM_CENTER, 6),
            (RegularPolygon(n=6, color=PURPLE, fill_opacity=0.5), PreferredPosition.CENTER_LEFT, 4),
            (Star(color=ORANGE, fill_opacity=0.5), PreferredPosition.CENTER_RIGHT, 4),
        ]
        
        for obj, pos, priority in test_objects:
            layout_manager.add(obj, pos, priority)
        
        # Perform layout
        report = layout_manager.layout()
        
        # Run validation tests
        validation_results = self._run_validation_tests(layout_manager)
        
        # Display objects
        for item in layout_manager.items:
            self.add(item.mobject)
        
        # Show debug visualizations
        debug_visuals = layout_manager.get_debug_visuals()
        self.add(debug_visuals)
        
        # Display validation results
        validation_text = self._create_validation_report(validation_results, report)
        validation_text.to_corner(DR)
        self.add(validation_text)
        
        self.wait(5)
    
    def _run_validation_tests(self, layout_manager: LayoutManager) -> dict:
        """Run automated validation tests"""
        results = {
            "overlap_test": True,
            "boundary_test": True,
            "padding_test": True,
            "overlap_details": [],
            "boundary_violations": [],
            "padding_violations": []
        }
        
        items = layout_manager.items
        region = layout_manager.available_region
        
        # Test 1: Check for overlaps
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                item1, item2 = items[i], items[j]
                if item1.bounding_box and item2.bounding_box:
                    if item1.bounding_box.overlaps(item2.bounding_box):
                        results["overlap_test"] = False
                        results["overlap_details"].append(f"Items {i} and {j} overlap")
        
        # Test 2: Check boundary compliance
        for i, item in enumerate(items):
            if item.bounding_box:
                if not region.contains(item.bounding_box):
                    results["boundary_test"] = False
                    results["boundary_violations"].append(f"Item {i} exceeds boundaries")
        
        # Test 3: Check minimum padding between items
        min_padding = layout_manager.min_item_padding
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                item1, item2 = items[i], items[j]
                if item1.bounding_box and item2.bounding_box:
                    # Calculate minimum distance between bounding boxes
                    dx = max(0, max(item1.bounding_box.x_min - item2.bounding_box.x_max,
                                   item2.bounding_box.x_min - item1.bounding_box.x_max))
                    dy = max(0, max(item1.bounding_box.y_min - item2.bounding_box.y_max,
                                   item2.bounding_box.y_min - item1.bounding_box.y_max))
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance < min_padding and distance > 0:
                        results["padding_test"] = False
                        results["padding_violations"].append(
                            f"Items {i} and {j} too close: {distance:.3f} < {min_padding}"
                        )
        
        return results
    
    def _create_validation_report(self, validation_results: dict, layout_report) -> Text:
        """Create validation test report"""
        summary = "VALIDATION TESTS:\n"
        summary += f"✓ No Overlaps: {'PASS' if validation_results['overlap_test'] else 'FAIL'}\n"
        summary += f"✓ Within Bounds: {'PASS' if validation_results['boundary_test'] else 'FAIL'}\n"
        summary += f"✓ Proper Padding: {'PASS' if validation_results['padding_test'] else 'FAIL'}\n"
        
        if not validation_results['overlap_test']:
            summary += f"\nOverlap Issues: {len(validation_results['overlap_details'])}\n"
        
        if not validation_results['boundary_test']:
            summary += f"Boundary Issues: {len(validation_results['boundary_violations'])}\n"
        
        if not validation_results['padding_test']:
            summary += f"Padding Issues: {len(validation_results['padding_violations'])}\n"
        
        summary += f"\nItems Placed: {layout_report.items_placed}/{layout_report.total_items}\n"
        summary += f"Utilization: {layout_report.region_utilization:.1%}"
        
        color = GREEN if all([validation_results['overlap_test'], 
                             validation_results['boundary_test'], 
                             validation_results['padding_test']]) else RED
        
        return Text(summary, font_size=12, color=color)


class RandomStressTestScene(Scene):
    """
    Stress test with many random objects to demonstrate performance and robustness
    """
    
    def construct(self):
        # Large region for stress testing
        region = BoundingBox(-6, -4, 6, 4)
        
        layout_manager = LayoutManager(
            region=region,
            padding=0.05,
            strategy=LayoutStrategy.PACKING_BASED,
            min_item_padding=0.02
        )
        
        # Create many random objects
        random.seed(123)  # Deterministic for testing
        
        for i in range(50):  # Stress test with 50 items
            # Random shape and size
            shape_choice = random.choice(['circle', 'square', 'triangle', 'text'])
            color = Color(hue=random.random(), saturation=0.8, luminance=0.6)
            
            if shape_choice == 'circle':
                obj = Circle(radius=random.uniform(0.05, 0.2), color=color, fill_opacity=0.6)
            elif shape_choice == 'square':
                obj = Square(side_length=random.uniform(0.1, 0.3), color=color, fill_opacity=0.6)
            elif shape_choice == 'triangle':
                obj = Triangle(color=color, fill_opacity=0.6).scale(random.uniform(0.2, 0.5))
            else:  # text
                obj = Text(f"{i}", font_size=random.randint(8, 16), color=color)
            
            priority = random.randint(1, 10)
            layout_manager.add(obj, priority=priority, min_scale=0.05, max_scale=1.0)
        
        # Perform layout
        report = layout_manager.layout()
        
        # Display objects
        for item in layout_manager.items:
            self.add(item.mobject)
        
        # Show region boundary only (debug visuals would be too cluttered)
        region_rect = Rectangle(
            width=region.width,
            height=region.height,
            color=WHITE,
            stroke_width=2
        ).move_to(region.center)
        self.add(region_rect)
        
        # Display performance report
        perf_text = Text(
            f"Stress Test Results:\n"
            f"Objects: {report.total_items}\n"
            f"Placed: {report.items_placed}\n"
            f"Scaled: {report.items_scaled}\n"
            f"Utilization: {report.region_utilization:.1%}\n"
            f"Overflow: {report.items_with_overflow}",
            font_size=16,
            color=YELLOW
        ).to_corner(UL)
        self.add(perf_text)
        
        self.wait(6)


# Utility function to render all examples
def render_all_examples():
    """Render all example scenes"""
    scenes = [
        LayoutManagerDemo1,
        LayoutManagerDemo2,
        LayoutManagerValidationScene,
        RandomStressTestScene
    ]
    
    for scene_class in scenes:
        print(f"Rendering {scene_class.__name__}...")
        # This would be called from command line typically
        # manim examples.py SceneName


if __name__ == "__main__":
    print("Manim Layout Manager Examples")
    print("Available scenes:")
    print("- LayoutManagerDemo1: Large objects with preferred positioning")
    print("- LayoutManagerDemo2: Many small objects with packing")
    print("- LayoutManagerValidationScene: Automated collision/boundary tests")
    print("- RandomStressTestScene: Performance stress test with 50 objects")
    print("\nRun with: manim layout_examples.py <SceneName>")
