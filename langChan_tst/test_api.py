#!/usr/bin/env python3
"""
Test script for the AI Video Generator API
"""

import requests
import json
import time
from typing import Dict, Any

API_BASE = "http://localhost:8001"

def test_api():
    """Test the API endpoints"""
    print("🧪 Testing AI Video Generator API")
    print(f"Base URL: {API_BASE}")
    print("-" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
            return
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    print()
    
    # Test 2: Generate scripts
    print("2. Testing script generation...")
    try:
        script_request = {
            "topic": "Simple Math",
            "quality": "low",
            "tts_provider": "mock"
        }
        response = requests.post(f"{API_BASE}/api/generate_scripts", json=script_request)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Generated {result['count']} scripts")
            print(f"   Tokens: {result['tokens']}")
            print("   ✅ Script generation passed")
            
            # Store first token for further testing
            test_token = result['tokens'][0] if result['tokens'] else None
            
        else:
            print(f"   ❌ Script generation failed: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Script generation failed: {e}")
        return
    
    print()
    
    if not test_token:
        print("❌ No token available for further testing")
        return
    
    # Test 3: Get script
    print("3. Testing script retrieval...")
    try:
        response = requests.get(f"{API_BASE}/api/script/{test_token}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            script = response.json()
            print(f"   Script title: {script.get('title', 'N/A')}")
            print(f"   Number of scenes: {len(script.get('scenes', []))}")
            print("   ✅ Script retrieval passed")
        else:
            print(f"   ❌ Script retrieval failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Script retrieval failed: {e}")
    
    print()
    
    # Test 4: Update script
    print("4. Testing script update...")
    try:
        update_data = {
            "title": "Updated Simple Math",
            "scenes": [
                {
                    "seq": 1,
                    "text": "Updated narration for scene 1",
                    "anim": "Updated animation description"
                }
            ]
        }
        
        response = requests.post(f"{API_BASE}/api/script/{test_token}", json=update_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Updated script title: {result['script'].get('title', 'N/A')}")
            print("   ✅ Script update passed")
        else:
            print(f"   ❌ Script update failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Script update failed: {e}")
    
    print()
    
    # Test 5: Validate config
    print("5. Testing config validation...")
    try:
        response = requests.post(f"{API_BASE}/api/validate_config")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Config valid: {result.get('valid', False)}")
            if result.get('valid'):
                print("   ✅ Config validation passed")
            else:
                print(f"   ❌ Config validation failed: {result.get('errors', [])}")
        else:
            print(f"   ❌ Config validation request failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Config validation failed: {e}")
    
    print()
    
    # Test 6: List jobs
    print("6. Testing job listing...")
    try:
        response = requests.get(f"{API_BASE}/api/jobs")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Total jobs: {result.get('total', 0)}")
            print("   ✅ Job listing passed")
        else:
            print(f"   ❌ Job listing failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Job listing failed: {e}")
    
    print()
    print("🎉 API testing completed!")
    print()
    print("Available endpoints:")
    print("  - GET  /                     - Health check")
    print("  - POST /api/generate_scripts - Generate script variations") 
    print("  - GET  /api/script/{token}   - Get script by token")
    print("  - POST /api/script/{token}   - Update script")
    print("  - POST /api/generate/{token} - Start video generation")
    print("  - GET  /api/job/{job_id}     - Check generation status")
    print("  - GET  /api/jobs             - List all jobs")
    print("  - POST /api/validate_config  - Validate system configuration")
    print()
    print("API Documentation: http://localhost:8001/docs")

if __name__ == "__main__":
    test_api()
