"""
Text-to-Speech provider implementations with parallel processing support
"""

import logging
import asyncio
import concurrent.futures
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import wave
import base64
import requests
import json
import time

# Optional imports that might cause issues
try:
    # Enable Google GenAI import
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_AVAILABLE = True
    
    # # Create stubs to prevent import errors
    # class genai:
    #     class Client:
    #         def __init__(self, api_key): pass
    #         
    # class types:
    #     class GenerateContentConfig:
    #         def __init__(self, **kwargs): pass
    #     class SpeechConfig:
    #         def __init__(self, **kwargs): pass
    #     class VoiceConfig:
    #         def __init__(self, **kwargs): pass
    #     class PrebuiltVoiceConfig:
    #         def __init__(self, **kwargs): pass
    # 
    # GOOGLE_GENAI_AVAILABLE = False
    # logger = logging.getLogger(__name__)
    # logger.info("Google GenAI temporarily disabled - using stubs")
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("Google GenAI not available - Gemini TTS provider will be disabled")
    GOOGLE_GENAI_AVAILABLE = False

try:
    # Temporarily disabled due to import issues 
    # from openai import OpenAI
    class OpenAI:
        def __init__(self, api_key): pass
    OPENAI_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.info("OpenAI temporarily disabled")
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("OpenAI not available - OpenAI TTS provider will be disabled")
    OPENAI_AVAILABLE = False

import sys
from pathlib import Path
# Add project root to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.models import TTSConfig, TTSProvider, BatchRequest, BatchResponse

from config.settings import GOOGLE_API_KEY, OPENAI_API_KEY, DIA_TTS_BASE_URL, DIA_TTS_API_KEY, DIA_TTS_TIMEOUT

logger = logging.getLogger(__name__)


class BaseTTSProvider(ABC):
    """Abstract base class for TTS providers with parallel processing support"""
    
    def __init__(self, config: TTSConfig):
        self.config = config
    
    @abstractmethod
    def synthesize(self, text: str, output_path: Path) -> bool:
        """Synthesize text to speech"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get provider name"""
        pass
    
    def synthesize_batch(self, tts_requests: List[Tuple[str, Path]], max_workers: int = 4) -> Dict[str, bool]:
        """Synthesize multiple texts in parallel"""
        logger.info(f"Starting batch TTS synthesis for {len(tts_requests)} requests with {max_workers} workers")
        
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_id = {}
            for i, (text, output_path) in enumerate(tts_requests):
                request_id = f"tts_{i}"
                future = executor.submit(self.synthesize, text, output_path)
                future_to_id[future] = request_id
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_id, timeout=300):
                request_id = future_to_id[future]
                try:
                    success = future.result(timeout=180)  # 3 minutes per request
                    results[request_id] = success
                    logger.debug(f"TTS request {request_id} completed: {success}")
                except concurrent.futures.TimeoutError:
                    logger.error(f"TTS request {request_id} timed out")
                    results[request_id] = False
                except Exception as e:
                    logger.error(f"TTS request {request_id} failed: {e}")
                    results[request_id] = False
        
        successful = sum(1 for success in results.values() if success)
        logger.info(f"Batch TTS synthesis completed: {successful}/{len(tts_requests)} successful")
        return results
    
    async def synthesize_async(self, text: str, output_path: Path) -> bool:
        """Async wrapper for synthesize method"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.synthesize, text, output_path)
    
    async def synthesize_batch_async(self, tts_requests: List[Tuple[str, Path]], max_concurrent: int = 4) -> Dict[str, bool]:
        """Synthesize multiple texts asynchronously"""
        logger.info(f"Starting async batch TTS synthesis for {len(tts_requests)} requests")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def synthesize_with_semaphore(request_id: str, text: str, output_path: Path):
            async with semaphore:
                try:
                    result = await self.synthesize_async(text, output_path)
                    logger.debug(f"Async TTS request {request_id} completed: {result}")
                    return request_id, result
                except Exception as e:
                    logger.error(f"Async TTS request {request_id} failed: {e}")
                    return request_id, False
        
        # Create coroutines for all requests
        coroutines = [
            synthesize_with_semaphore(f"tts_{i}", text, output_path)
            for i, (text, output_path) in enumerate(tts_requests)
        ]
        
        # Wait for all to complete
        try:
            task_results = await asyncio.wait_for(
                asyncio.gather(*coroutines, return_exceptions=True),
                timeout=300  # 5 minutes total
            )
            
            results = {}
            for result in task_results:
                if isinstance(result, Exception):
                    logger.error(f"Async task failed: {result}")
                    continue
                request_id, success = result
                results[request_id] = success
                
        except asyncio.TimeoutError:
            logger.error("Async batch TTS synthesis timed out")
            results = {f"tts_{i}": False for i in range(len(tts_requests))}
        
        successful = sum(1 for success in results.values() if success)
        logger.info(f"Async batch TTS synthesis completed: {successful}/{len(tts_requests)} successful")
        return results


class GeminiTTSProvider(BaseTTSProvider):
    """Gemini TTS provider implementation"""
    
    def __init__(self, config: TTSConfig):
        super().__init__(config)
        if not GOOGLE_GENAI_AVAILABLE:
            raise ValueError("Google GenAI package not available - install with 'pip install google-genai'")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required for Gemini TTS")
        
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
    
    def _write_wave_file(self, filename: Path, pcm_data: bytes, channels=1, rate=24000, sample_width=2):
        """Write PCM data to wave file"""
        with wave.open(str(filename), "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
    
    def synthesize(self, text: str, output_path: Path) -> bool:
        """Synthesize text using Gemini TTS"""
        try:
            logger.info(f"Generating TTS with Gemini voice: {self.config.voice}")
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=text,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=self.config.voice,
                            )
                        )
                    ),
                )
            )
            
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Extract PCM data from the response
                        pcm_data = part.inline_data.data
                        
                        # Write as WAV file using the helper function
                        self._write_wave_file(output_path, pcm_data)
                        logger.info(f"✓ TTS successful: {output_path}")
                        return True
            
            logger.error("No audio content found in Gemini response")
            return False
            
        except Exception as e:
            logger.error(f"Gemini TTS failed: {e}")
            return False
    
    def get_provider_name(self) -> str:
        return "gemini"


class GeminiBatchTTSProvider(BaseTTSProvider):
    """Gemini Batch TTS provider for cost-effective processing"""
    
    def __init__(self, config: TTSConfig):
        super().__init__(config)
        if not GOOGLE_GENAI_AVAILABLE:
            raise ValueError("Google GenAI package not available - install with 'pip install google-genai'")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is required for Gemini Batch TTS")
        
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.batch_requests: List[BatchRequest] = []
        self.batch_id: Optional[str] = None
    
    def _write_wave_file(self, filename: Path, pcm_data: bytes, channels=1, rate=24000, sample_width=2):
        """Write PCM data to wave file"""
        with wave.open(str(filename), "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm_data)
    
    def add_to_batch(self, text: str, output_path: Path, request_id: str):
        """Add TTS request to batch"""
        request = BatchRequest(
            id=request_id,
            scene_data={"text": text, "output_path": str(output_path)},
            layout="tts",  # Not applicable for TTS but required by model
            system_prompt="Generate speech from text",
            user_prompt=text
        )
        self.batch_requests.append(request)
        logger.info(f"Added TTS request {request_id} to batch")
    
    def process_batch(self) -> Dict[str, bool]:
        """Process all TTS requests in batch"""
        if not self.batch_requests:
            return {}
        
        try:
            logger.info(f"Processing batch with {len(self.batch_requests)} TTS requests")
            
            # Create batch job
            batch_data = []
            for req in self.batch_requests:
                batch_data.append({
                    'contents': [{
                        'parts': [{'text': req.user_prompt}],
                        'role': 'user'
                    }],
                    'generation_config': {
                        'response_modalities': ['AUDIO'],
                        'speech_config': {
                            'voice_config': {
                                'prebuilt_voice_config': {
                                    'voice_name': self.config.voice
                                }
                            }
                        }
                    }
                })
            
            # Submit batch (simplified - actual implementation would use batch API)
            results = {}
            for i, req in enumerate(self.batch_requests):
                try:
                    response = self.client.models.generate_content(
                        model="gemini-2.5-flash-preview-tts",
                        contents=req.user_prompt,
                        config=types.GenerateContentConfig(
                            response_modalities=["AUDIO"],
                            speech_config=types.SpeechConfig(
                                voice_config=types.VoiceConfig(
                                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                        voice_name=self.config.voice,
                                    )
                                )
                            ),
                        )
                    )
                    
                    output_path = Path(req.scene_data["output_path"])
                    if response.candidates and response.candidates[0].content.parts:
                        for part in response.candidates[0].content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # Extract PCM data and write as WAV
                                pcm_data = part.inline_data.data
                                self._write_wave_file(output_path, pcm_data)
                                results[req.id] = True
                                break
                        else:
                            results[req.id] = False
                    else:
                        results[req.id] = False
                        
                except Exception as e:
                    logger.error(f"Batch TTS failed for request {req.id}: {e}")
                    results[req.id] = False
            
            # Clear batch
            self.batch_requests.clear()
            logger.info(f"✓ Batch TTS processing completed")
            return results
            
        except Exception as e:
            logger.error(f"Batch TTS processing failed: {e}")
            return {req.id: False for req in self.batch_requests}
    
    def synthesize(self, text: str, output_path: Path) -> bool:
        """Individual synthesis - not used in batch mode"""
        request_id = f"tts_{len(self.batch_requests)}"
        self.add_to_batch(text, output_path, request_id)
        results = self.process_batch()
        return results.get(request_id, False)
    
    def get_provider_name(self) -> str:
        return "gemini_batch"


class MockTTSProvider(BaseTTSProvider):
    """Mock TTS provider for testing"""
    
    def __init__(self, config: TTSConfig):
        super().__init__(config)
    
    def synthesize(self, text: str, output_path: Path) -> bool:
        """Create a silent audio file for testing"""
        try:
            import wave
            import struct
            
            logger.info(f"Creating mock TTS for: {text[:50]}...")
            
            # Create a short silent WAV file
            sample_rate = 22050
            duration = min(len(text) / 150.0 * 5, 10.0)  # Rough estimate based on text length
            frames = int(sample_rate * duration)
            
            with wave.open(str(output_path), 'w') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # Write silent frames
                for _ in range(frames):
                    wav_file.writeframes(struct.pack('<h', 0))  # silent frame
            
            logger.info(f"✓ Mock TTS successful: {output_path} ({duration:.1f}s)")
            return True
            
        except Exception as e:
            logger.error(f"Mock TTS failed: {e}")
            return False
    
    def get_provider_name(self) -> str:
        return "mock"


class OpenAITTSProvider(BaseTTSProvider):
    """OpenAI TTS provider implementation"""
    
    def __init__(self, config: TTSConfig):
        super().__init__(config)
        if not OPENAI_AVAILABLE:
            raise ValueError("OpenAI package not available - install with 'pip install openai'")
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI TTS")
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def synthesize(self, text: str, output_path: Path) -> bool:
        """Synthesize text using OpenAI TTS"""
        try:
            logger.info(f"Generating TTS with OpenAI voice: {self.config.voice}")
            
            model = self.config.model or "tts-1"
            response = self.client.audio.speech.create(
                model=model,
                voice=self.config.voice,
                input=text,
                response_format="wav"
            )
            
            output_path.write_bytes(response.content)
            logger.info(f"✓ TTS successful: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"OpenAI TTS failed: {e}")
            return False
    
    def get_provider_name(self) -> str:
        return "openai"


class DiaTTSProvider(BaseTTSProvider):
    """Dia TTS provider implementation using custom TTS endpoint"""
    
    def __init__(self, config: TTSConfig, base_url: Optional[str] = None, 
                 api_key: Optional[str] = None, enable_fallback: bool = True,
                 use_openai_compatible: bool = False):
        super().__init__(config)
        self.base_url = (base_url or DIA_TTS_BASE_URL).rstrip("/")
        self.api_key = api_key or DIA_TTS_API_KEY
        self.enable_fallback = enable_fallback
        self.use_openai_compatible = use_openai_compatible  # Use /v1/audio/speech endpoint
        self._fallback_provider = None
        
        # Default configuration based on API specification
        self.default_config = {
            "voice_mode": "single_s1",
            "output_format": "wav",
            "speed_factor": 0.9,
            "cfg_scale": 2.0,
            "temperature": 1.2,
            "top_p": 0.95,
            "cfg_filter_top_k": 35,
            "seed": 42,
            "split_text": True,
            "chunk_size": 300,  # API default chunk size
            "timeout": DIA_TTS_TIMEOUT  # Use configurable timeout
        }
    
    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        """Simple whitespace-aware splitter targeting chunk_size characters."""
        words = text.split()
        chunks = []
        cur = []
        cur_len = 0
        for w in words:
            if cur_len + len(w) + (1 if cur else 0) > chunk_size and cur:
                chunks.append(" ".join(cur))
                cur = [w]
                cur_len = len(w)
            else:
                cur.append(w)
                cur_len += len(w) + (1 if cur_len else 0)
        if cur:
            chunks.append(" ".join(cur))
        return chunks
    
    def _get_fallback_provider(self):
        """Get fallback provider (mock TTS) for when DiaTTS is unavailable"""
        if self._fallback_provider is None:
            logger.warning("Creating fallback Mock TTS provider due to DiaTTS unavailability")
            from src.core.models import TTSConfig, TTSProvider
            fallback_config = TTSConfig(provider=TTSProvider.MOCK, voice=self.config.voice)
            self._fallback_provider = MockTTSProvider(fallback_config)
        return self._fallback_provider
    
    def _choose_extension(self, format_name: str, content_type: str = None) -> str:
        """Choose appropriate file extension based on format"""
        if format_name:
            if format_name.lower() in ("wav", "wave"):
                return "wav"
            if format_name.lower() in ("opus",):
                return "opus"
        if content_type:
            if "wav" in content_type:
                return "wav"
            if "opus" in content_type or "ogg" in content_type:
                return "opus"
        return "bin"
    
    def _call_custom_tts(self, text: str, **kwargs) -> Tuple[bytes, requests.Response]:
        """Call the custom TTS endpoint following the API specification"""
        url = f"{self.base_url}/tts"
        
        # Merge default config with provided kwargs
        config = self.default_config.copy()
        config.update(kwargs)
        
        # Build payload according to API spec
        payload = {
            "text": text,
            "voice_mode": config.get("voice_mode", "dialogue"),
            "output_format": config.get("output_format", "wav"),
            "speed_factor": config.get("speed_factor", 1.0),
            "seed": config.get("seed", 42),
            "split_text": config.get("split_text", True),
            "chunk_size": config.get("chunk_size", 120),
        }
        
        # Add optional parameters only if they exist
        if config.get("clone_reference_filename"):
            payload["clone_reference_filename"] = config["clone_reference_filename"]
        
        if config.get("transcript"):
            payload["transcript"] = config["transcript"]
        
        # Add optional generation parameters if provided
        for param in ["max_tokens", "cfg_scale", "temperature", "top_p", "cfg_filter_top_k"]:
            value = config.get(param)
            if value is not None:
                payload[param] = value
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        timeout = config.get("timeout", 60)
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        
        return response.content, response
    
    def _call_openai_compatible_tts(self, text: str, **kwargs) -> Tuple[bytes, requests.Response]:
        """Call the OpenAI-compatible TTS endpoint (/v1/audio/speech)"""
        url = f"{self.base_url}/v1/audio/speech"
        
        # Merge default config with provided kwargs
        config = self.default_config.copy()
        config.update(kwargs)
        
        # Map voice_mode to OpenAI-compatible voice parameter
        voice_mode = config.get("voice_mode", "dialogue")
        if voice_mode == "single_s1":
            voice = "S1"
        elif voice_mode == "single_s2":
            voice = "S2"
        elif voice_mode == "dialogue":
            voice = "dialogue"
        else:
            # For clone or predefined modes, use the filename as voice
            voice = config.get("clone_reference_filename", "dialogue")
        
        # Build payload according to OpenAI-compatible API spec
        payload = {
            "input": text,
            "voice": voice,
            "response_format": config.get("output_format", "wav"),
            "speed": config.get("speed_factor", 1.0),
        }
        
        # Add seed if specified (not -1)
        seed = config.get("seed", 42)
        if seed != -1:
            payload["seed"] = seed
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        timeout = config.get("timeout", 60)
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        
        return response.content, response
    
    def _handle_response_and_save(self, response: requests.Response, content: bytes, 
                                  output_path: Path, fmt_hint: str = None) -> bool:
        """Handle TTS response and save audio file"""
        try:
            content_type = response.headers.get("Content-Type", "")
            
            if "application/json" in content_type:
                # Server returned JSON (likely error)
                try:
                    error_obj = response.json()
                    logger.error(f"Dia TTS server error: {json.dumps(error_obj, indent=2)}")
                except Exception:
                    logger.error(f"Dia TTS JSON response (couldn't parse): {content.decode('utf-8', errors='ignore')}")
                return False
            
            # Save audio content
            ext = self._choose_extension(fmt_hint, content_type)
            
            # Ensure output path has correct extension
            if output_path.suffix.lower() != f".{ext}":
                output_path = output_path.with_suffix(f".{ext}")
            
            with open(output_path, "wb") as f:
                f.write(content)
            
            logger.info(f"✓ Dia TTS successful: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save Dia TTS response: {e}")
            return False
    
    def synthesize(self, text: str, output_path: Path) -> bool:
        """Synthesize text using Dia TTS with retry logic"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                logger.info(f"Generating TTS with Dia TTS (voice_mode: {self.default_config['voice_mode']}) - Attempt {retry_count + 1}/{max_retries}")
                
                # Choose endpoint based on configuration
                if self.use_openai_compatible:
                    content, response = self._call_openai_compatible_tts(text)
                else:
                    content, response = self._call_custom_tts(text)
                
                # Handle response and save
                success = self._handle_response_and_save(
                    response, content, output_path, 
                    fmt_hint=self.default_config["output_format"]
                )
                
                if success:
                    return True
                else:
                    logger.warning(f"Dia TTS attempt {retry_count + 1} failed, response indicated error")
                    
            except requests.exceptions.Timeout as e:
                retry_count += 1
                logger.warning(f"Dia TTS timeout on attempt {retry_count}/{max_retries} (timeout: {self.default_config['timeout']}s): {str(e)}")
                if retry_count < max_retries:
                    logger.info(f"Retrying in 5 seconds...")
                    import time
                    time.sleep(5)
                else:
                    logger.error(f"Dia TTS failed after {max_retries} timeout attempts")
                    if self.enable_fallback:
                        logger.warning("All DiaTTS attempts timed out, falling back to Mock TTS provider")
                        fallback = self._get_fallback_provider()
                        return fallback.synthesize(text, output_path)
                    
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Dia TTS connection failed: {str(e)}")
                logger.error(f"Check if TTS server at {self.base_url} is accessible")
                if self.enable_fallback and retry_count == 0:  # Only try fallback on first connection error
                    logger.warning("Attempting fallback to Mock TTS provider")
                    fallback = self._get_fallback_provider()
                    return fallback.synthesize(text, output_path)
                break  # Don't retry connection errors
                
            except requests.exceptions.RequestException as e:
                retry_count += 1
                logger.warning(f"Dia TTS request failed on attempt {retry_count}/{max_retries}: {str(e)}")
                if retry_count < max_retries:
                    logger.info(f"Retrying in 3 seconds...")
                    import time
                    time.sleep(3)
                else:
                    logger.error(f"Dia TTS failed after {max_retries} request attempts")
                    if self.enable_fallback:
                        logger.warning("All DiaTTS attempts failed, falling back to Mock TTS provider")
                        fallback = self._get_fallback_provider()
                        return fallback.synthesize(text, output_path)
                    
            except Exception as e:
                logger.error(f"Dia TTS unexpected error: {e}")
                break  # Don't retry unexpected errors
        
        return False
    
    def synthesize_batch_optimized(self, tts_requests: List[Tuple[str, Path]], max_workers: int = 6) -> Dict[str, bool]:
        """Optimized batch synthesis for DiaTTS with connection pooling and smart retry"""
        logger.info(f"Starting optimized DiaTTS batch synthesis for {len(tts_requests)} requests with {max_workers} workers")
        
        results = {}
        
        # Use session for connection pooling
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(pool_connections=max_workers, pool_maxsize=max_workers*2))
        session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=max_workers, pool_maxsize=max_workers*2))
        
        def synthesize_with_session(request_id: str, text: str, output_path: Path) -> bool:
            """Synthesize single request using shared session"""
            max_retries = 2  # Reduced retries for batch processing
            
            for attempt in range(max_retries):
                try:
                    url = f"{self.base_url}/tts"
                    
                    config = self.default_config.copy()
                    # Build payload according to API spec
                    payload = {
                        "text": text,
                        "voice_mode": config.get("voice_mode", "dialogue"),
                        "output_format": config.get("output_format", "wav"),
                        "speed_factor": config.get("speed_factor", 1.0),
                        "seed": config.get("seed", 42),
                        "split_text": config.get("split_text", True),
                        "chunk_size": config.get("chunk_size", 120),
                    }
                    
                    # Add optional generation parameters if provided
                    for param in ["max_tokens", "cfg_scale", "temperature", "top_p", "cfg_filter_top_k"]:
                        value = config.get(param)
                        if value is not None:
                            payload[param] = value
                    
                    # Add optional parameters only if they exist
                    if config.get("clone_reference_filename"):
                        payload["clone_reference_filename"] = config["clone_reference_filename"]
                    
                    if config.get("transcript"):
                        payload["transcript"] = config["transcript"]
                    
                    headers = {"Content-Type": "application/json"}
                    if self.api_key:
                        headers["Authorization"] = f"Bearer {self.api_key}"
                    
                    # Shorter timeout for batch processing
                    timeout = min(config.get("timeout", 60), 120)
                    
                    response = session.post(url, headers=headers, json=payload, timeout=timeout)
                    
                    # Handle response
                    content_type = response.headers.get("Content-Type", "")
                    
                    if "application/json" in content_type:
                        try:
                            error_obj = response.json()
                            logger.warning(f"DiaTTS error for {request_id}: {error_obj}")
                        except:
                            logger.warning(f"DiaTTS JSON error for {request_id}")
                        continue  # Try again
                    
                    # Save audio content
                    ext = self._choose_extension(config.get("output_format", "wav"), content_type)
                    if output_path.suffix.lower() != f".{ext}":
                        output_path = output_path.with_suffix(f".{ext}")
                    
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    
                    logger.debug(f"DiaTTS batch request {request_id} successful")
                    return True
                    
                except requests.exceptions.Timeout:
                    logger.warning(f"DiaTTS timeout for {request_id}, attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        time.sleep(2)  # Brief pause before retry
                except Exception as e:
                    logger.warning(f"DiaTTS error for {request_id}, attempt {attempt + 1}/{max_retries}: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)
            
            # All attempts failed
            logger.error(f"DiaTTS batch request {request_id} failed after all attempts")
            return False
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks
                future_to_id = {}
                for i, (text, output_path) in enumerate(tts_requests):
                    request_id = f"dia_batch_{i}"
                    future = executor.submit(synthesize_with_session, request_id, text, output_path)
                    future_to_id[future] = request_id
                
                # Collect results as they complete
                for future in concurrent.futures.as_completed(future_to_id, timeout=600):  # 10 minutes total
                    request_id = future_to_id[future]
                    try:
                        success = future.result(timeout=180)  # 3 minutes per request
                        results[request_id] = success
                    except concurrent.futures.TimeoutError:
                        logger.error(f"DiaTTS batch request {request_id} timed out")
                        results[request_id] = False
                    except Exception as e:
                        logger.error(f"DiaTTS batch request {request_id} failed: {e}")
                        results[request_id] = False
        
        finally:
            session.close()
        
        successful = sum(1 for success in results.values() if success)
        logger.info(f"DiaTTS optimized batch synthesis completed: {successful}/{len(tts_requests)} successful")
        
        # If many failed and fallback is enabled, try fallback for failed requests
        if self.enable_fallback and successful < len(tts_requests) * 0.5:  # Less than 50% success
            logger.warning("Low DiaTTS success rate, using fallback for failed requests")
            fallback = self._get_fallback_provider()
            
            # Get failed requests
            failed_requests = []
            for i, (text, output_path) in enumerate(tts_requests):
                request_id = f"dia_batch_{i}"
                if not results.get(request_id, False):
                    failed_requests.append((text, output_path))
            
            if failed_requests:
                fallback_results = fallback.synthesize_batch(failed_requests, max_workers=max_workers)
                # Update results
                failed_idx = 0
                for i, (text, output_path) in enumerate(tts_requests):
                    request_id = f"dia_batch_{i}"
                    if not results.get(request_id, False):
                        fallback_key = f"tts_{failed_idx}"
                        if fallback_key in fallback_results:
                            results[request_id] = fallback_results[fallback_key]
                        failed_idx += 1
        
        return results
    
    def synthesize_chunked(self, text: str, output_path: Path, chunk_locally: bool = False) -> bool:
        """Synthesize text with optional local chunking"""
        try:
            if chunk_locally and len(text) > self.default_config["chunk_size"]:
                # Split text locally and process multiple chunks
                chunks = self._split_text(text, self.default_config["chunk_size"])
                logger.info(f"Local chunking enabled: {len(chunks)} parts")
                
                all_content = []
                for i, chunk in enumerate(chunks, start=1):
                    logger.info(f"Processing chunk {i}/{len(chunks)}")
                    content, response = self._call_custom_tts(chunk)
                    
                    if "application/json" in response.headers.get("Content-Type", ""):
                        logger.error(f"Chunk {i} failed")
                        return False
                    
                    all_content.append(content)
                
                # Combine all chunks into one file (simple concatenation for WAV)
                combined_content = b"".join(all_content)
                with open(output_path, "wb") as f:
                    f.write(combined_content)
                
                logger.info(f"✓ Dia TTS chunked synthesis successful: {output_path}")
                return True
            else:
                # Use server-side chunking (default)
                return self.synthesize(text, output_path)
                
        except Exception as e:
            logger.error(f"Dia TTS chunked synthesis failed: {e}")
            return False
    
    def get_provider_name(self) -> str:
        return "dia"


class TTSProviderFactory:
    """Factory for creating TTS providers"""
    
    _providers = {
        TTSProvider.GEMINI: GeminiTTSProvider,
        TTSProvider.GEMINI_BATCH: GeminiBatchTTSProvider,
        TTSProvider.OPENAI: OpenAITTSProvider,
        TTSProvider.DIA: DiaTTSProvider,
        TTSProvider.MOCK: MockTTSProvider
    }
    
    @classmethod
    def create_provider(cls, provider_type: TTSProvider, config: TTSConfig) -> BaseTTSProvider:
        """Create TTS provider instance"""
        if provider_type not in cls._providers:
            raise ValueError(f"Unknown TTS provider: {provider_type}")
        
        provider_class = cls._providers[provider_type]
        return provider_class(config)
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available providers"""
        return [provider.value for provider in TTSProvider]


def create_tts_provider(provider_name: str, **kwargs) -> BaseTTSProvider:
    """Convenience function to create TTS provider"""
    try:
        provider_type = TTSProvider(provider_name)
    except ValueError:
        raise ValueError(f"Unknown TTS provider: {provider_name}")
    
    # Create config from kwargs
    config = TTSConfig(provider=provider_type, **kwargs)
    
    return TTSProviderFactory.create_provider(provider_type, config)
