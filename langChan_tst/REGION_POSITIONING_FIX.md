# Region Positioning Fix

## Issue
Generated Manim scenes were failing with positioning errors:
```
title_text.move_to(self.title_region)  # Error: Cannot use Rectangle directly as position
```

**Error Details:**
- The LLM was generating code that used region objects directly for positioning
- Manim requires position coordinates, not Rectangle objects
- This caused runtime failures when scenes tried to execute

## Root Cause
The LLM generation prompts were incomplete. They told the LLM about regions but didn't specify HOW to use them for positioning:

### Before (Incomplete Instructions):
```
1. Create the title text using `self.create_textbox` and place it in the title/text region.
2. Create the main animation described in "anim" and place it in the main/diagram region.  
3. Use `self.play()` and `self.wait()` as normal.
4. Output ONLY the Python code for the *body* of the `construct_scene` method.
```

### After (Complete Instructions):
```
1. Create the title text using `self.create_textbox` and place it in the title/text region.
2. Create the main animation described in "anim" and place it in the main/diagram region.
3. Use `self.play()` and `self.wait()` as normal.
4. For positioning: Use `text.move_to(self.region_name.get_center())` to position objects in regions.
5. For sizing: Use `self.region_name.width` and `self.region_name.height` for dimensions.
6. Output ONLY the Python code for the *body* of the `construct_scene` method.
```

## Solution
Updated both individual and batch LLM generation prompts to include explicit positioning instructions:

### Key Addition:
```
4. For positioning: Use `text.move_to(self.region_name.get_center())` to position objects in regions.
5. For sizing: Use `self.region_name.width` and `self.region_name.height` for dimensions.
```

## Technical Details

### Correct Usage Pattern:
```python
# Correct: Get center point for positioning
title_text.move_to(self.title_region.get_center())

# Correct: Use width/height for sizing
title_text = self.create_textbox(text, self.title_region.width, self.title_region.height)
```

### Incorrect Usage (Previous):
```python
# Wrong: Using Rectangle object directly as position
title_text.move_to(self.title_region)  # This causes the error
```

## Changes Made

### 1. Individual LLM Generation (`call_manim_llm_single`)
- Updated user_prompt to include positioning instructions
- Line ~440 in gem_mnm.py

### 2. Batch LLM Generation (`prepare_manim_batch_request`)  
- Updated user_prompt to include positioning instructions
- Line ~595 in gem_mnm.py

## Benefits
1. **Prevents Runtime Errors**: LLM now generates correct positioning code
2. **Clearer Instructions**: Explicit examples of how to use regions
3. **Consistent Behavior**: Both individual and batch generation use same clear instructions
4. **Better Reliability**: Reduces need for fallback templates due to LLM errors

## Testing
- Syntax validation: ✓ Passed
- Ready for video generation testing with corrected LLM instructions

## Files Modified
- `gem_mnm.py`: Updated both individual and batch LLM generation prompts with positioning instructions
