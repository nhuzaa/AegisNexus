#!/usr/bin/env python3
"""
Speech Test Runner

Runs all speech-to-text tests including direct API and WebSocket tests.
"""

import os
import sys
import asyncio
import subprocess
from typing import Dict, Any

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def check_server_status():
    """Check if the server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8001/speech-streaming/health", timeout=3)
        return response.status_code == 200
    except Exception:
        return False

def check_audio_file():
    """Check if test audio file exists"""
    audio_file_path = "./audio/simplequestion.wav"
    return os.path.exists(audio_file_path)

async def run_websocket_tests():
    """Run WebSocket speech-to-text tests"""
    print("\n🌐 Running WebSocket Speech-to-Text Tests")
    print("=" * 60)
    
    try:
        from tests.speech.test_websocket_speech_to_text import run_websocket_speech_tests
        await run_websocket_speech_tests()
        return True
    except Exception as e:
        print(f"❌ WebSocket tests failed: {str(e)}")
        return False

def run_direct_api_tests():
    """Run direct API speech-to-text tests"""
    print("\n🔗 Running Direct API Speech-to-Text Tests")
    print("=" * 60)
    
    try:
        from tests.speech.test_direct_speech_to_text import run_direct_api_tests
        run_direct_api_tests()
        return True
    except Exception as e:
        print(f"❌ Direct API tests failed: {str(e)}")
        return False

async def run_all_speech_tests():
    """Run all speech-to-text tests"""
    print("🧪 AegisNexus Speech-to-Text Test Suite")
    print("=" * 60)
    print("🎯 Testing both Direct API and WebSocket implementations")
    
    # Pre-flight checks
    print("\n🔍 Pre-flight Checks")
    print("-" * 30)
    
    # Check audio file
    if not check_audio_file():
        print("❌ Test audio file not found: ./audio/simplequestion.wav")
        print("💡 Please ensure the audio file exists for testing")
        return
    else:
        print("✅ Test audio file found")
    
    # Check server status for WebSocket tests
    server_running = check_server_status()
    if server_running:
        print("✅ Server is running (WebSocket tests available)")
    else:
        print("⚠️ Server is not running (WebSocket tests will be skipped)")
        print("💡 To run WebSocket tests, start the server:")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload")
    
    # Run tests
    results = {}
    
    # 1. Direct API Tests (always available)
    print("\n" + "=" * 60)
    direct_api_success = run_direct_api_tests()
    results['direct_api'] = direct_api_success
    
    # 2. WebSocket Tests (only if server is running)
    if server_running:
        print("\n" + "=" * 60)
        websocket_success = await run_websocket_tests()
        results['websocket'] = websocket_success
    else:
        results['websocket'] = 'skipped'
    
    # Final Summary
    print("\n" + "=" * 60)
    print("📊 Final Test Results")
    print("=" * 60)
    
    direct_status = "✅ PASSED" if results['direct_api'] else "❌ FAILED"
    print(f"Direct API Tests:     {direct_status}")
    
    if results['websocket'] == 'skipped':
        print(f"WebSocket Tests:      ⏭️ SKIPPED (server not running)")
    else:
        websocket_status = "✅ PASSED" if results['websocket'] else "❌ FAILED"
        print(f"WebSocket Tests:      {websocket_status}")
    
    # Overall result
    if results['direct_api'] and (results['websocket'] in [True, 'skipped']):
        print("\n🎉 Overall Result: SUCCESS")
        if results['websocket'] == 'skipped':
            print("   (WebSocket tests were skipped - start server to run all tests)")
    else:
        print("\n💥 Overall Result: SOME TESTS FAILED")
    
    print("\n💡 Tips:")
    print("   - For WebSocket tests: Start the server first")
    print("   - For audio tests: Ensure ./audio/simplequestion.wav exists")
    print("   - Check Azure Speech Service configuration in .env.local")

if __name__ == "__main__":
    asyncio.run(run_all_speech_tests())
