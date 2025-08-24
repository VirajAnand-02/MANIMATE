# Manim CLI Command Fix

## Issue
The code was using custom resolution and frame rate flags that are unreliable:
```bash
manim script.py SceneName --resolution=1280,720 --frame_rate=60
```

## Solution
Replaced with Manim's built-in quality presets which are more stable:
```bash
manim script.py SceneName -qh
```

## Quality Options Available
- `-ql` - Low quality (854x480 15FPS) - for rapid prototyping
- `-qm` - Medium quality (1280x720 30FPS) - balanced
- `-qh` - High quality (1920x1080 60FPS) - good quality ✓ **SELECTED**
- `-qp` - 2K quality (2560x1440 60FPS) - very high quality
- `-qk` - 4K quality (3840x2160 60FPS) - maximum quality

## Benefits
1. **Reliability**: Built-in presets are more stable than custom flags
2. **Consistency**: Standard presets ensure consistent output across systems
3. **Performance**: High quality preset provides good balance of quality vs render time
4. **Compatibility**: Works with all Manim versions

## Technical Details
- Changed in `save_and_render_manim()` function
- Removed `RESOLUTION` and `FRAME_RATE` constants dependency
- Using `-qh` for 1920x1080@60FPS output
- Maintains existing timeout and error handling

## Testing
- Syntax validation: ✓ Passed
- Ready for integration testing with video generation
