#!/usr/bin/env python3
"""
Debug script to test Gemini API response structure
"""

from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_response():
    """Test Gemini API response to understand structure"""
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("GOOGLE_API_KEY not found in environment")
        return
    
    client = genai.Client(api_key=api_key)
    
    prompt = "Generate a simple JSON object with a title and description for matrix multiplication."
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1000
            )
        )
        
        print(f"Response type: {type(response)}")
        print(f"Response attributes: {dir(response)}")
        print(f"Response: {response}")
        
        if hasattr(response, 'text'):
            print(f"Response.text type: {type(response.text)}")
            print(f"Response.text: {response.text}")
        
        if hasattr(response, 'candidates'):
            print(f"Candidates: {len(response.candidates) if response.candidates else 'None'}")
            if response.candidates:
                for i, candidate in enumerate(response.candidates):
                    print(f"  Candidate {i}: {type(candidate)}")
                    print(f"  Candidate {i} attributes: {dir(candidate)}")
                    if hasattr(candidate, 'content'):
                        print(f"    Content: {candidate.content}")
                        if hasattr(candidate.content, 'parts'):
                            print(f"    Parts: {len(candidate.content.parts) if candidate.content.parts else 'None'}")
                            if candidate.content.parts:
                                for j, part in enumerate(candidate.content.parts):
                                    print(f"      Part {j}: {type(part)}")
                                    print(f"      Part {j} attributes: {dir(part)}")
                                    if hasattr(part, 'text'):
                                        print(f"        Text: {part.text}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_response()
