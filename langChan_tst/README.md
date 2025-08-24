# AI-Powered Educational Video Generator v2.0

A modular, extensible system for creating educational videos using Large Language Models and Manim animation framework.

## 🚀 Features

- **Multi-LLM Support**: Google Gemini and OpenAI integration
- **Batch Processing**: Efficient generation of multiple scenes
- **Multi-TTS Providers**: Gemini and OpenAI text-to-speech
- **Template System**: Pre-built layouts for consistent video design
- **Content Archiving**: Comprehensive organization of generated content
- **Modular Architecture**: Clean, maintainable, and extensible codebase
- **Type Safety**: Pydantic models for configuration validation
- **Rich CLI**: Feature-rich command-line interface
- **Comprehensive Logging**: Colored output with progress tracking

## 🏗️ Architecture

```
langChan_tst/
├── main.py                 # CLI entry point
├── config/
│   └── settings.py         # Configuration management
├── src/
│   ├── core/
│   │   ├── models.py       # Pydantic data models
│   │   └── engine.py       # Main orchestration engine
│   ├── providers/
│   │   ├── llm.py          # LLM implementations
│   │   └── tts.py          # TTS implementations
│   ├── templates/
│   │   └── layouts.py      # Manim templates
│   └── utils/
│       ├── logging.py      # Logging utilities
│       ├── file_ops.py     # File operations
│       └── video.py        # Video processing
├── tests/                  # Test suite
├── docs/                   # Documentation
└── logs/                   # Log files
```

## 🔧 Installation

1. **Clone and Setup:**
   ```bash
   cd langChan_tst
   pip install -r requirements.txt
   ```

2. **Environment Configuration:**
   Create a `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_key_here
   OPENAI_API_KEY=your_openai_key_here
   ```

3. **Validate Setup:**
   ```bash
   python main.py --validate-only
   ```

## 🎬 Quick Start

### Basic Usage

```bash
# Generate a video about machine learning
python main.py "machine learning basics"

# High quality video with OpenAI TTS
python main.py "quantum computing" --quality high --tts-provider openai

# Custom layout without batch processing
python main.py "calculus introduction" --custom-layout --no-batch
```

### Advanced Options

```bash
# Full feature example
python main.py "neural networks" \
  --quality 2k \
  --tts-provider openai \
  --tts-voice alloy \
  --no-thinking \
  --output-dir ./my_videos \
  --log-level DEBUG
```

## 📋 CLI Reference

### Main Options
- `topic`: The educational topic for video generation
- `--quality`: Video quality (low, medium, high, 2k, 4k)
- `--tts-provider`: TTS provider (gemini, gemini_batch, openai)
- `--tts-voice`: Voice to use for TTS
- `--format`: Output format (mp4, gif)

### Generation Options
- `--no-batch`: Disable batch processing
- `--no-thinking`: Disable LLM thinking mode
- `--thinking-budget`: Token budget for thinking (default: 6000)
- `--custom-layout`: Use custom layout generation

### Output Options
- `--output-dir`: Custom output directory
- `--archive-only`: Only create archive, don't save to renders

### System Options
- `--validate-only`: Validate configuration and exit
- `--cleanup`: Clean up old temporary files
- `--version`: Show version information
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## 🔌 Programmatic Usage

```python
from src.core.engine import create_video_engine
from src.core.models import TTSConfig, ManimConfig, RenderConfig
from src.core.models import TTSProvider, QualityPreset

# Configure the system
tts_config = TTSConfig(
    provider=TTSProvider.GEMINI,
    voice="Kore"
)

manim_config = ManimConfig(
    use_thinking=True,
    thinking_budget=6000,
    use_batch=True
)

render_config = RenderConfig(
    quality=QualityPreset.HIGH,
    output_format="mp4"
)

# Create and use the engine
engine = create_video_engine(
    tts_config=tts_config,
    manim_config=manim_config,
    render_config=render_config
)

success, summary = engine.generate_video("machine learning basics")

if success:
    print(f"Generated {summary.total_scenes} scenes")
    print(f"TTS Success: {summary.tts_stats.success}/{summary.total_scenes}")
    print(f"Manim Success: {summary.manim_stats.success}/{summary.total_scenes}")
```

## 🧩 Extending the System

### Adding New TTS Providers

1. Implement the `BaseTTSProvider` interface:

```python
from src.providers.tts import BaseTTSProvider

class CustomTTSProvider(BaseTTSProvider):
    def generate_speech(self, text: str, output_path: Path) -> bool:
        # Your implementation here
        pass
```

2. Register in `TTSProviderFactory`

### Adding New Templates

1. Create a new template class in `src/templates/`:

```python
from src.templates.layouts import TemplateScene

class MyCustomTemplate(TemplateScene):
    def create_scene(self):
        # Your Manim scene implementation
        pass
```

### Adding New Utilities

Add utility modules to `src/utils/` and update `__init__.py`

## 🧪 Testing

Run the architecture test:

```bash
python tests/test_architecture.py
```

Run specific tests:

```bash
python -m unittest tests.test_architecture.TestArchitecture.test_model_creation
```

## 📊 Output Structure

Generated content is organized as follows:

```
outputs/
├── renders/                    # Final video outputs
│   └── GeneratedScene-timestamp.mp4
└── archives/                   # Complete generation archives
    └── video_timestamp/
        ├── script.json         # Generated script
        ├── scenes/             # Individual scene files
        ├── audio/              # TTS audio files
        ├── manim_code/         # Generated Manim code
        ├── renders/            # Scene renders
        └── final_video.mp4     # Combined video
```

## 🔍 Debugging

### Enable Debug Logging

```bash
python main.py "topic" --log-level DEBUG
```

### Check Configuration

```bash
python main.py --validate-only
```

### Monitor Real-time

Logs are written to `logs/video_generation.log` with colored console output.

## 🔄 Migration from v1.0

If migrating from the monolithic `gem_mnm.py` version, see [`docs/migration_guide.md`](docs/migration_guide.md) for detailed instructions.

## 📚 Dependencies

- **Core**: Python 3.8+, Pydantic, python-dotenv
- **AI**: google-generativeai, openai
- **Video**: manim, ffmpeg-python
- **Utilities**: colorama, pathlib

## 🤝 Contributing

1. **Architecture**: Follow the modular design patterns
2. **Testing**: Add tests for new functionality
3. **Documentation**: Update docstrings and README
4. **Configuration**: Use the centralized settings system

## 📝 License

See LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all `__init__.py` files are present
2. **API Errors**: Validate API keys with `--validate-only`
3. **Video Errors**: Check FFmpeg installation
4. **Permission Errors**: Ensure write access to output directories

### Getting Help

1. Check logs in `logs/` directory
2. Run with `--log-level DEBUG`
3. Use `--validate-only` for configuration issues
4. Review the migration guide for v1.0 users

## 🎯 Roadmap

- [ ] Web interface
- [ ] Additional LLM providers
- [ ] Real-time streaming
- [ ] Interactive templates
- [ ] Cloud deployment options
