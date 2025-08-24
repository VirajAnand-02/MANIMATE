# DiaTTS Provider Documentation

## Overview

The DiaTTS provider enables integration with custom TTS endpoints that follow a specific API pattern. This provider is designed as a fallback TTS option with robust configuration and chunking capabilities.

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Enable DiaTTS provider
TTS_PROVIDER=dia

# DiaTTS endpoint configuration
DIA_TTS_BASE_URL=http://139.84.154.247:8003
DIA_TTS_API_KEY=your_api_key_here  # Optional

# Voice configuration (optional, defaults to dialogue mode)
TTS_VOICE_NAME=dialogue
```

### Default Configuration

The DiaTTS provider uses these optimized defaults based on your reference command:

```python
{
    "voice_mode": "dialogue",
    "output_format": "wav", 
    "speed_factor": 1.0,
    "cfg_scale": 3.0,
    "temperature": 1.3,
    "top_p": 0.95,
    "cfg_filter_top_k": 35,
    "seed": 42,
    "split_text": True,
    "chunk_size": 120,
    "timeout": 60
}
```

## API Compatibility

The DiaTTS provider expects the following endpoint:

**POST** `/tts`

### Request Payload
```json
{
    "text": "Text to synthesize",
    "voice_mode": "dialogue",
    "output_format": "wav",
    "speed_factor": 1.0,
    "cfg_scale": 3.0,
    "temperature": 1.3,
    "top_p": 0.95,
    "cfg_filter_top_k": 35,
    "seed": 42,
    "split_text": true,
    "chunk_size": 120
}
```

### Response
- **Success**: Binary audio data (WAV/OPUS) with appropriate `Content-Type`
- **Error**: JSON response with error details

## Features

### 1. Automatic Chunking
- **Server-side chunking** (default): Lets the TTS service handle text splitting
- **Client-side chunking**: Splits text locally for compatibility

### 2. Format Detection
Automatically detects output format from:
- Explicit format parameter
- HTTP Content-Type header  
- Falls back to binary format

### 3. Error Handling
- Comprehensive request/response error handling
- JSON error message parsing and logging
- Network timeout configuration

### 4. Flexible Configuration
All TTS parameters can be customized via the config system.

## Usage Examples

### Basic Usage
```python
from src.providers.tts import create_tts_provider
from src.core.models import TTSConfig, TTSProvider

# Create DiaTTS provider
config = TTSConfig(provider=TTSProvider.DIA, voice="dialogue")
provider = create_tts_provider("dia", **config.get_provider_config())

# Synthesize text
success = provider.synthesize("Hello world", Path("output.wav"))
```

### Advanced Usage with Custom Settings
```python
# Create provider with custom endpoint
provider = DiaTTSProvider(
    config=config,
    base_url="http://your-custom-endpoint:8000",
    api_key="your-key"
)

# Use chunked synthesis for long text
success = provider.synthesize_chunked(
    long_text, 
    Path("output.wav"), 
    chunk_locally=True
)
```

### Integration with Video Generation
Set in your `.env`:
```env
TTS_PROVIDER=dia
```

The video generation system will automatically use DiaTTS for all TTS operations.

## Testing

Run the test script to verify functionality:
```bash
python test_dia_tts.py
```

This will test:
- Provider creation and configuration
- Basic text synthesis  
- Chunked synthesis for longer texts
- Error handling and response processing

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify `DIA_TTS_BASE_URL` is correct and accessible
   - Check network connectivity to the TTS endpoint

2. **JSON Response Errors**  
   - Server returned error instead of audio
   - Check logs for detailed error messages
   - Verify API key if authentication is required

3. **Format Issues**
   - Ensure output format matches expected type
   - Check Content-Type headers in server response

### Debug Mode
Enable detailed logging:
```python
import logging
logging.getLogger('src.providers.tts').setLevel(logging.DEBUG)
```

## Reference Command
This implementation is based on the optimal configuration:
```bash
python dia_test.py --endpoint tts --text-file dialog.txt --voice-mode dialogue \
  --output-format wav --speed 1.0 --cfg-scale 3.0 --temperature 1.3 \
  --top-p 0.95 --cfg-filter-top-k 35 --seed 42 --split-text true \
  --chunk-size 120 --base-url http://139.84.154.247:8003 --output dialog_demo
```
