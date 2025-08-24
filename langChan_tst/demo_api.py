#!/usr/bin/env python3

import os
import sys
import json
import uuid
import time
import logging
import copy
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Any, Dict
import google.generativeai as genai
from google.generativeai.types import GenerationConfig
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------------------------
# Setup logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,   # DEBUG so we see everything
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()
GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
if not GENAI_API_KEY:
    logger.error("GENAI_API_KEY not found in environment variables.")
    raise ValueError("GENAI_API_KEY not found in environment variables.")

# -------------------------------------------------
# Configure GenAI
# -------------------------------------------------
genai.configure(api_key=GENAI_API_KEY)

# -------------------------------------------------
# Pydantic models
# -------------------------------------------------
class Scene(BaseModel):
    seq: int
    text: str
    anim: str

class VideoScript(BaseModel):
    title: str
    scenes: List[Scene]

# -------------------------------------------------
# Minimal schema Gemini understands
# -------------------------------------------------
VIDEO_SCRIPT_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "seq": {"type": "integer"},
                    "text": {"type": "string"},
                    "anim": {"type": "string"}
                },
                "required": ["seq", "text", "anim"]
            }
        }
    },
    "required": ["title", "scenes"]
}

# -------------------------------------------------
# Script generation function
# -------------------------------------------------
def call_script_llm(topic: str, max_retries=3):
    user_prompt = f"""
    Create a JSON structure for an educational video about "{topic}".

    Format requirements:
    - Return ONLY valid JSON
    - 3-5 scenes
    - Narration text should be clear and educational
    - Animation descriptions should be specific and visual
    """

    logger.debug(f"Generated user prompt:\n{user_prompt}")

    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Script LLM (Attempt {attempt+1})...")

            response = model.generate_content(
                user_prompt,
                generation_config=GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=VIDEO_SCRIPT_SCHEMA
                )
            )

            json_text = response.text.strip()
            logger.debug(f"Raw model response (string):\n{json_text}")

            # Try parsing
            video_script_dict = json.loads(json_text)
            logger.debug(f"Parsed JSON (dict): {json.dumps(video_script_dict, indent=2)}")

            # Validate with Pydantic
            validated = VideoScript(**video_script_dict)
            logger.debug(f"Validated Pydantic object: {validated.model_dump_json(indent=2)}")

            logger.info("✓ Successfully generated and validated video script.")
            return video_script_dict

        except Exception as e:
            logger.warning(f"[script LLM] attempt {attempt+1} failed: {e}", exc_info=True)
            if attempt < max_retries - 1:
                time.sleep(2)

    raise RuntimeError("Script LLM failed after all retries.")

# -------------------------------------------------
# FastAPI setup
# -------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to log every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    body = await request.body()
    if body:
        try:
            logger.debug(f"Request body: {body.decode()}")
        except:
            logger.debug(f"Request body (binary): {body}")
    response = await call_next(request)
    logger.info(f"Completed request with status {response.status_code}")
    return response

# In-memory storage
scripts_storage: Dict[str, Any] = {}

class GenVidRequest(BaseModel):
    topic: str

class GetScriptRequest(BaseModel):
    token: str

# -----------------------
# New request models
# -----------------------
class SetScriptRequest(BaseModel):
    token: str
    script: Dict[str, Any]

class StartGenVideoRequest(BaseModel):
    token: str

# -----------------------
# Helper: merge scripts
# -----------------------
def merge_scripts(existing: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge `updates` into `existing` without removing keys missing from `updates`.
    Special handling for 'scenes' (list of scene dicts with 'seq'):
      - If an incoming scene has the same seq as an existing scene, update its fields.
      - If an incoming scene has a new seq, append it.
      - Order scenes by seq ascending after merge.
    For other top-level keys, updates overwrite existing values.
    """
    if existing is None:
        existing = {}

    result = copy.deepcopy(existing)

    for k, v in updates.items():
        if k == "scenes":
            if not isinstance(v, list):
                raise ValueError("'scenes' must be a list when provided.")
            existing_scenes = {s['seq']: copy.deepcopy(s) for s in result.get('scenes', []) if 'seq' in s}
            for incoming in v:
                if 'seq' not in incoming:
                    raise ValueError("Each scene in updates must include a 'seq' integer.")
                seq = incoming['seq']
                if seq in existing_scenes:
                    # update existing scene fields (don't remove unspecified keys)
                    existing_scenes[seq].update(incoming)
                else:
                    # new scene: ensure it has all required fields (validation later)
                    existing_scenes[seq] = copy.deepcopy(incoming)
            # Rebuild scenes list ordered by seq
            result['scenes'] = [existing_scenes[s] for s in sorted(existing_scenes.keys())]
        else:
            # For non-scenes keys, simply overwrite (this is intended)
            result[k] = copy.deepcopy(v)

    return result

# -------------------------------------------------
# Existing endpoints
# -------------------------------------------------
@app.post("/gen_vid")
def gen_vid(request: GenVidRequest):
    logger.info(f"/gen_vid called with topic: {request.topic}")
    try:
        tokens = []  # <-- list to collect all tokens
        for i in range(3):  # generate 3 scripts
            logger.info(f"Generating script #{i+1} for topic: {request.topic}")
            script_data = call_script_llm(request.topic)
            token = uuid.uuid4().hex[:8]
            scripts_storage[token] = script_data
            tokens.append(token)   # <-- append to the list, not the string
            logger.info(f"Generated script #{i+1} stored under token {token}")

        return {"tokens": tokens}  # return list of tokens
    except Exception as e:
        logger.error(f"Failed to generate scripts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate scripts: {str(e)}")


@app.get("/get_script")
def get_script(token: str):
    logger.info(f"/get_script called with token: {token}")
    if token not in scripts_storage:
        logger.warning(f"Token {token} not found in storage")
        raise HTTPException(status_code=404, detail="Token not found")
    logger.debug("Returning script for token %s:\n%s", token, json.dumps(scripts_storage[token], indent=2))
    return scripts_storage[token]

# -------------------------------------------------
# New endpoint: /set_script
# -------------------------------------------------
@app.post("/set_script")
def set_script(req: SetScriptRequest):
    token = req.token
    incoming_script = req.script
    logger.info(f"/set_script called for token: {token}")

    try:
        if token in scripts_storage:
            logger.debug(f"Token {token} exists — merging incoming script into stored script.")
            merged = merge_scripts(scripts_storage[token], incoming_script)
        else:
            logger.debug(f"Token {token} does not exist — creating new script entry.")
            merged = copy.deepcopy(incoming_script)

        # Validate merged with Pydantic VideoScript to ensure final shape is valid.
        # This will raise a ValidationError if required fields are missing or wrong types.
        validated = VideoScript(**merged)
        # If validation passes, store
        scripts_storage[token] = merged
        logger.info(f"Script for token {token} set/updated successfully.")
        return {"token": token, "script": merged}
    except Exception as e:
        logger.error(f"Failed to set/update script for token {token}: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Failed to set/update script: {str(e)}")

# -------------------------------------------------
# New endpoint: /start_gen_video
# -------------------------------------------------
@app.post("/start_gen_video")
def start_gen_video(req: StartGenVideoRequest):
    token = req.token
    logger.info(f"/start_gen_video called for token: {token}")

    if token not in scripts_storage:
        logger.warning(f"Token {token} not found when attempting to start generation.")
        raise HTTPException(status_code=404, detail="Token not found")

    # Placeholder: user asked to leave this blank for now.
    # You can replace the following stub with actual generation logic (e.g., call exporter, renderer, queue tasks, etc.)
    logger.info(f"start_gen_video stub invoked for token {token}. No generation implemented yet.")
    return {"status": "accepted", "message": "start_gen_video is a stub for now. Replace with generation logic when ready."}

# -------------------------------------------------
# Run server
# -------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
