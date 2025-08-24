# Migration Guide: From Monolithic to Modular Architecture

## Overview

This guide explains how to migrate from the old monolithic `gem_mnm.py` to the new modular architecture.

## Key Changes

### 1. File Structure

**Old Structure:**
```
gem_mnm.py              # All functionality in one file
layouts.py              # Template system
```

**New Structure:**
```
main.py                 # CLI entry point
config/
  settings.py           # Configuration and constants
src/
  core/
    models.py           # Pydantic data models
    engine.py           # Main orchestration engine
  providers/
    llm.py              # LLM provider implementations
    tts.py              # TTS provider implementations
  templates/
    layouts.py          # Template system (moved)
  utils/
    logging.py          # Logging utilities
    file_ops.py         # File operations
    video.py            # Video processing
tests/
  test_architecture.py  # Architecture tests
docs/                   # Documentation
```

### 2. Usage Changes

**Old Usage:**
```python
# Direct execution
python gem_mnm.py
```

**New Usage:**
```bash
# CLI interface with options
python main.py "machine learning basics"
python main.py "quantum computing" --quality high --tts-provider openai
python main.py "calculus" --no-batch --custom-layout
```

### 3. Configuration Changes

**Old Configuration:**
- Hardcoded constants in gem_mnm.py
- Environment variables scattered throughout

**New Configuration:**
- Centralized in `config/settings.py`
- Environment validation
- Type-safe configuration objects

**Migration Steps:**
1. Copy your `.env` file (API keys remain the same)
2. Update any custom configurations in `config/settings.py`

### 4. Programmatic Usage

**Old API:**
```python
# Direct function calls
from gem_mnm import generate_video
```

**New API:**
```python
from src.core.engine import create_video_engine
from src.core.models import TTSConfig, ManimConfig, RenderConfig

# Create engine with configuration
engine = create_video_engine(
    tts_config=TTSConfig(provider="gemini"),
    manim_config=ManimConfig(use_batch=True),
    render_config=RenderConfig(quality="high")
)

# Generate video
success, summary = engine.generate_video("machine learning")
```

### 5. Customization Changes

**Old Customization:**
- Modify gem_mnm.py directly
- Limited extensibility

**New Customization:**
- Implement provider interfaces
- Add new templates to `src/templates/`
- Extend configuration in `config/settings.py`
- Add custom utilities to `src/utils/`

### 6. Benefits of New Architecture

1. **Modularity**: Clear separation of concerns
2. **Testability**: Each module can be tested independently
3. **Extensibility**: Easy to add new providers or features
4. **Maintainability**: Easier to debug and modify
5. **Type Safety**: Pydantic models prevent configuration errors
6. **Logging**: Comprehensive logging with colored output
7. **Configuration**: Centralized and validated settings
8. **CLI**: Feature-rich command-line interface

### 7. Feature Parity

All features from the original implementation are preserved:

- ✅ Google Gemini & OpenAI LLM integration
- ✅ Multi-provider TTS (Gemini, OpenAI)
- ✅ Batch processing for efficiency
- ✅ Template-based layout system
- ✅ Content archiving and organization
- ✅ Video processing and concatenation
- ✅ Error handling and recovery
- ✅ Progress tracking and statistics

### 8. Testing Migration

Run the architecture test to verify everything works:

```bash
cd langChan_tst
python tests/test_architecture.py
```

### 9. Validation Steps

1. **Environment Check:**
   ```bash
   python main.py --validate-only
   ```

2. **Test Generation:**
   ```bash
   python main.py "test topic" --quality medium
   ```

3. **Compare Output:**
   - Verify same video quality
   - Check archive structure
   - Confirm all features work

### 10. Troubleshooting

**Import Errors:**
- Ensure all `__init__.py` files are present
- Check Python path includes project root

**Configuration Errors:**
- Run `python main.py --validate-only`
- Check `.env` file has all required keys

**Missing Dependencies:**
- Install requirements: `pip install -r requirements.txt`
- Verify Manim installation

**API Issues:**
- Test API connectivity with validation
- Check API key permissions

### 11. Rollback Plan

If issues occur, you can still use the original files:
- `gem_mnm.py` (original monolithic version)
- `langchain_version/` (LangChain implementation)

### 12. Next Steps

After successful migration:

1. **Cleanup**: Remove old files when confident
2. **Customize**: Add your own providers or templates
3. **Test**: Create comprehensive tests for your use cases
4. **Document**: Update any internal documentation
5. **Monitor**: Use the new logging system for debugging

## Support

For migration issues:
1. Check the logs in `logs/` directory
2. Run with `--log-level DEBUG` for detailed output
3. Use `--validate-only` to check configuration
4. Test individual components with the test suite
