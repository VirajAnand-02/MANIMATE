#!/usr/bin/env python3
"""
Simple test script to debug Google GenAI API issues
"""
import os
from dotenv import load_dotenv

load_dotenv()

GENAI_API_KEY = os.environ.get("GENAI_API_KEY")
print(f"API Key found: {bool(GENAI_API_KEY)}")
print(f"API Key (first 10 chars): {GENAI_API_KEY[:10] if GENAI_API_KEY else 'None'}")

try:
    from google import genai
    from google.genai import types
    print("Successfully imported google.genai")
    
    # Initialize the GenAI client with the API key
    client = genai.Client(api_key=GENAI_API_KEY)
    print("Successfully created GenAI client")
    
    # Test a simple API call
    print("Testing simple API call...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Say hello world",
        config=types.GenerateContentConfig(
            max_output_tokens=50,
        ),
    )
    
    print(f"Response type: {type(response)}")
    print(f"Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
    
    # Try to extract text
    if hasattr(response, 'text'):
        print(f"response.text: {response.text}")
    
    if hasattr(response, 'candidates'):
        print(f"response.candidates: {response.candidates}")
        if response.candidates:
            candidate = response.candidates[0]
            print(f"candidate type: {type(candidate)}")
            print(f"candidate attributes: {[attr for attr in dir(candidate) if not attr.startswith('_')]}")
            
            if hasattr(candidate, 'content'):
                content = candidate.content
                print(f"content type: {type(content)}")
                print(f"content attributes: {[attr for attr in dir(content) if not attr.startswith('_')]}")
                
                if hasattr(content, 'parts'):
                    print(f"content.parts: {content.parts}")
                    if content.parts:
                        part = content.parts[0]
                        print(f"part type: {type(part)}")
                        print(f"part attributes: {[attr for attr in dir(part) if not attr.startswith('_')]}")
                        if hasattr(part, 'text'):
                            print(f"part.text: {part.text}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
