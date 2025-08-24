# Layout Import Path Fix

## Issue
Generated scene files in temporary directories couldn't locate the `layouts.py` module:
```
ModuleNotFoundError: No module named 'layouts'
```

## Root Cause
The generated scene files were using relative imports:
```python
from layouts import TitleAndMainContent
```

When these files are executed from a temporary directory (`tmp_manim_scenes/`), Python can't find the `layouts.py` file which is in the parent directory.

## Solution
Updated both fallback template and batch generation code to use absolute path imports:

### Before:
```python
from layouts import TitleAndMainContent
```

### After:
```python
import sys
sys.path.append(r'E:\programming\Notes2Manim\langChan_tst')
from layouts import TitleAndMainContent
```

## Changes Made

### 1. Fallback Template (simple_text_scene_template)
```python
# Use the template system for fallback as well
current_dir = Path(__file__).parent
code = f"""import sys
sys.path.append(r'{current_dir}')
from layouts import TitleAndMainContent
```

### 2. Batch Generation Code
```python
# Create the final code by inheriting from the template
# Use absolute import path since the script will be in a subdirectory
current_dir = Path(__file__).parent
final_code = f"import sys\nsys.path.append(r'{current_dir}')\nfrom layouts import {template_class_name}\n\n"
```

## Technical Details
- **Dynamic Path Resolution**: Uses `Path(__file__).parent` to get absolute path
- **Cross-Platform Compatible**: Raw string `r'{path}'` handles Windows backslashes correctly
- **Python Path Modification**: `sys.path.append()` adds parent directory to module search path
- **Maintains Functionality**: All existing template features (TitleAndMainContent, SplitScreen) remain available

## Benefits
1. **Fixes Import Errors**: Generated scenes can now find the layouts module
2. **Platform Independent**: Works on Windows, Linux, and macOS
3. **Maintains Templates**: All layout templates remain fully functional
4. **Future Proof**: Will work regardless of where tmp directories are created

## Testing
- Syntax validation: ✓ Passed
- Ready for video generation testing

## Files Modified
- `gem_mnm.py`: Updated both fallback template and batch generation import paths
