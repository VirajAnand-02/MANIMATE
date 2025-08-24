#!/usr/bin/env python3
"""
tts_tester.py

Simple CLI tester for two TTS endpoints:

  - /v1/audio/speech  (OpenAI-compatible)
    payload keys: input, voice, response_format, speed, seed

  - /tts  (Custom)
    payload keys: text, voice_mode, clone_reference_filename,
                  transcript, output_format, max_tokens,
                  cfg_scale, temperature, top_p, cfg_filter_top_k,
                  speed_factor, seed, split_text, chunk_size

Features:
 - Choose endpoint (v1 or tts)
 - Loads text from argument or file
 - Optional local chunking for /v1 endpoint (saves parts separately)
 - Saves audio to disk
 - Uses Authorization: Bearer <API_KEY> if provided
"""

import argparse
import json
import math
import os
import sys
from typing import List, Tuple

import requests


def split_text(text: str, chunk_size: int) -> List[str]:
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


def save_audio_bytes(data: bytes, filename: str) -> None:
    with open(filename, "wb") as f:
        f.write(data)
    print(f"Saved audio -> {filename}")


def choose_extension(format_name: str, content_type: str = None) -> str:
    if format_name:
        if format_name.lower() in ("wav", "wave"):
            return "wav"
        if format_name.lower() in ("opus",):
            # opus often in .opus or inside ogg; use .opus
            return "opus"
    if content_type:
        if "wav" in content_type:
            return "wav"
        if "opus" in content_type or "ogg" in content_type:
            return "opus"
    return "bin"


def call_v1_audio_speech(
    base_url: str,
    api_key: str,
    text: str,
    voice: str = "S1",
    response_format: str = "wav",
    speed: float = 1.0,
    seed: int = -1,
    timeout: int = 30,
) -> Tuple[bytes, requests.Response]:
    url = base_url.rstrip("/") + "/v1/audio/speech"
    payload = {
        "input": text,
        "voice": voice,
        "response_format": response_format,
        "speed": speed,
        "seed": seed,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    # Return raw bytes and response object for inspection
    return resp.content, resp


def call_custom_tts(
    base_url: str,
    api_key: str,
    text: str,
    voice_mode: str = "single_s1",
    clone_reference_filename: str = None,
    transcript: str = None,
    output_format: str = "wav",
    max_tokens: int = None,
    cfg_scale: float = None,
    temperature: float = None,
    top_p: float = None,
    cfg_filter_top_k: int = None,
    speed_factor: float = 1.0,
    seed: int = -1,
    split_text: bool = True,
    chunk_size: int = 120,
    timeout: int = 60,
) -> Tuple[bytes, requests.Response]:
    url = base_url.rstrip("/") + "/tts"
    payload = {
        "text": text,
        "voice_mode": voice_mode,
        "clone_reference_filename": clone_reference_filename,
        "transcript": transcript,
        "output_format": output_format,
        "speed_factor": speed_factor,
        "seed": seed,
        "split_text": split_text,
        "chunk_size": chunk_size,
    }
    # Only include optional numeric params if provided
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if cfg_scale is not None:
        payload["cfg_scale"] = cfg_scale
    if temperature is not None:
        payload["temperature"] = temperature
    if top_p is not None:
        payload["top_p"] = top_p
    if cfg_filter_top_k is not None:
        payload["cfg_filter_top_k"] = cfg_filter_top_k

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    return resp.content, resp


def handle_response_and_save(
    resp: requests.Response, content: bytes, out_base: str, fmt_hint: str = None
) -> None:
    ctype = resp.headers.get("Content-Type", "")
    if "application/json" in ctype:
        # Server returned JSON (likely error or structured response)
        try:
            obj = resp.json()
            print("Server returned JSON:")
            print(json.dumps(obj, indent=2))
        except Exception:
            print("JSON response (couldn't parse). Raw:")
            print(content.decode("utf-8", errors="ignore"))
        return

    ext = choose_extension(fmt_hint, ctype)
    out_name = f"{out_base}.{ext}"
    save_audio_bytes(content, out_name)


def main():
    parser = argparse.ArgumentParser(description="TTS API tester")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for the API")
    parser.add_argument("--api-key", default=None, help="Authorization Bearer token (optional)")
    parser.add_argument("--endpoint", choices=["v1", "tts"], default="v1", help="Which endpoint to call")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Text to synthesize (wrap in quotes)")
    group.add_argument("--text-file", help="Path to a text file to load")

    # v1 params
    parser.add_argument("--voice", default="S1", help="voice for /v1 (S1|S2|dialogue|filename.wav|reference.wav)")
    parser.add_argument("--response-format", default="wav", choices=["wav", "opus"], help="response format for /v1")

    # custom tts params
    parser.add_argument("--voice-mode", default="single_s1", help="voice_mode for /tts (dialogue|single_s1|single_s2|clone|predefined)")
    parser.add_argument("--clone-reference", default=None, help="filename for clone or predefined (relative path on server)")
    parser.add_argument("--transcript", default=None, help="explicit transcript (only for clone mode)")

    # common/generation params
    parser.add_argument("--speed", type=float, default=1.0, help="playback speed (v1 uses 'speed', tts uses 'speed_factor')")
    parser.add_argument("--seed", type=int, default=-1, help="seed (-1 for random)")
    parser.add_argument("--output", default="out", help="output base filename (extension added)")
    parser.add_argument("--timeout", type=int, default=60, help="request timeout seconds")

    # advanced tts-only generation params
    parser.add_argument("--output-format", default="wav", choices=["wav", "opus"], help="output_format for /tts")
    parser.add_argument("--max-tokens", type=int, default=None)
    parser.add_argument("--cfg-scale", type=float, default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--top-p", type=float, default=None)
    parser.add_argument("--cfg-filter-top-k", type=int, default=None)
    parser.add_argument("--split-text", type=lambda s: s.lower() in ("1", "true", "yes"), default=True)
    parser.add_argument("--chunk-size", type=int, default=120, help="target chunk size (chars) for server-side chunking")
    parser.add_argument("--auto-chunk-v1", action="store_true", help="If set, split large text locally for /v1 and save multiple parts")

    args = parser.parse_args()

    if args.text_file:
        if not os.path.exists(args.text_file):
            print("Text file not found:", args.text_file)
            sys.exit(2)
        with open(args.text_file, "r", encoding="utf-8") as f:
            text = f.read().strip()
    else:
        text = args.text.strip()

    if not text:
        print("Empty text provided.")
        sys.exit(2)

    try:
        if args.endpoint == "v1":
            # If user asked for auto-chunking, split locally and call repeatedly
            if args.auto_chunk_v1:
                chunks = split_text(text, args.chunk_size)
                print(f"Local chunking enabled: {len(chunks)} parts (chunk_size={args.chunk_size})")
                for i, c in enumerate(chunks, start=1):
                    content, resp = call_v1_audio_speech(
                        base_url=args.base_url,
                        api_key=args.api_key,
                        text=c,
                        voice=args.voice,
                        response_format=args.response_format,
                        speed=args.speed,
                        seed=args.seed,
                        timeout=args.timeout,
                    )
                    out_base = f"{args.output}_part{i}"
                    handle_response_and_save(resp, content, out_base, fmt_hint=args.response_format)
                print("All parts done.")
            else:
                content, resp = call_v1_audio_speech(
                    base_url=args.base_url,
                    api_key=args.api_key,
                    text=text,
                    voice=args.voice,
                    response_format=args.response_format,
                    speed=args.speed,
                    seed=args.seed,
                    timeout=args.timeout,
                )
                handle_response_and_save(resp, content, args.output, fmt_hint=args.response_format)
        else:
            content, resp = call_custom_tts(
                base_url=args.base_url,
                api_key=args.api_key,
                text=text,
                voice_mode=args.voice_mode,
                clone_reference_filename=args.clone_reference,
                transcript=args.transcript,
                output_format=args.output_format,
                max_tokens=args.max_tokens,
                cfg_scale=args.cfg_scale,
                temperature=args.temperature,
                top_p=args.top_p,
                cfg_filter_top_k=args.cfg_filter_top_k,
                speed_factor=args.speed,
                seed=args.seed,
                split_text=args.split_text,
                chunk_size=args.chunk_size,
                timeout=args.timeout,
            )
            handle_response_and_save(resp, content, args.output, fmt_hint=args.output_format)

    except requests.exceptions.RequestException as e:
        print("Request failed:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
