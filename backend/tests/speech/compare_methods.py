#!/usr/bin/env python3
"""
Comparison Test: Direct API vs WebSocket Speech-to-Text

This test demonstrates the differences between direct Azure Speech Service API calls
and WebSocket streaming for speech-to-text functionality.
"""

import os
import sys
import asyncio
import time
from typing import Dict, Any

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

async def compare_speech_to_text_methods():
    """Compare direct API vs WebSocket speech-to-text methods"""
    print("🔍 Speech-to-Text Method Comparison")
    print("=" * 60)
    
    audio_file_path = "./audio/simplequestion.wav"
    
    if not os.path.exists(audio_file_path):
        print(f"❌ Test audio file not found: {audio_file_path}")
        return
    
    # Test 1: Direct API Method
    print("\n📋 Method 1: Direct Azure Speech Service API")
    print("-" * 45)
    
    try:
        from app.services.azure_speech_service import AzureSpeechService
        
        start_time = time.time()
        speech_service = AzureSpeechService()
        direct_result = speech_service.speech_to_text(audio_file_path=audio_file_path)
        direct_duration = time.time() - start_time
        
        print(f"⏱️ Duration: {direct_duration:.2f} seconds")
        if direct_result.get("status") == "success":
            print(f"✅ Success: {direct_result.get('text')}")
            print(f"📊 Confidence: {direct_result.get('confidence')}")
        else:
            print(f"❌ Failed: {direct_result.get('error')}")
            
    except Exception as e:
        print(f"❌ Direct API error: {str(e)}")
        direct_result = {"status": "error", "error": str(e)}
        direct_duration = 0
    
    # Test 2: WebSocket Method
    print("\n📋 Method 2: WebSocket Streaming")
    print("-" * 35)
    
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:8001/speech-streaming/health", timeout=3)
        server_running = response.status_code == 200
    except Exception:
        server_running = False
    
    if not server_running:
        print("⚠️ Server not running - WebSocket test skipped")
        print("💡 Start server: uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload")
        websocket_result = {"status": "skipped"}
        websocket_duration = 0
    else:
        try:
            from tests.speech.test_websocket_speech_to_text import WebSocketSpeechToTextTester
            
            start_time = time.time()
            tester = WebSocketSpeechToTextTester()
            
            if await tester.connect():
                websocket_result = await tester.test_speech_to_text_from_file(audio_file_path)
                await tester.disconnect()
            else:
                websocket_result = {"status": "error", "error": "Connection failed"}
            
            websocket_duration = time.time() - start_time
            
            print(f"⏱️ Duration: {websocket_duration:.2f} seconds")
            if websocket_result.get("status") == "success":
                print(f"✅ Success: {websocket_result.get('text')}")
                print(f"📊 Confidence: {websocket_result.get('confidence')}")
            else:
                print(f"❌ Failed: {websocket_result.get('error')}")
                
        except Exception as e:
            print(f"❌ WebSocket error: {str(e)}")
            websocket_result = {"status": "error", "error": str(e)}
            websocket_duration = 0
    
    # Comparison Summary
    print("\n📊 Comparison Summary")
    print("=" * 60)
    
    print("🔗 Direct API Method:")
    print(f"   Status: {'✅ Success' if direct_result.get('status') == 'success' else '❌ Failed'}")
    print(f"   Duration: {direct_duration:.2f} seconds")
    print(f"   Use Case: Simple, one-off transcriptions")
    print(f"   Pros: Fast, direct, minimal overhead")
    print(f"   Cons: No SRE integration, no audio response")
    
    print("\n🌐 WebSocket Streaming Method:")
    if websocket_result.get("status") == "skipped":
        print(f"   Status: ⏭️ Skipped (server not running)")
    else:
        print(f"   Status: {'✅ Success' if websocket_result.get('status') == 'success' else '❌ Failed'}")
        print(f"   Duration: {websocket_duration:.2f} seconds")
    print(f"   Use Case: Interactive conversations")
    print(f"   Pros: SRE integration, audio responses, real-time")
    print(f"   Cons: Requires server, more complex, higher latency")
    
    # Text Comparison
    if (direct_result.get("status") == "success" and 
        websocket_result.get("status") == "success"):
        
        direct_text = direct_result.get("text", "").strip()
        websocket_text = websocket_result.get("text", "").strip()
        
        print(f"\n📝 Transcription Comparison:")
        print(f"   Direct API:  '{direct_text}'")
        print(f"   WebSocket:   '{websocket_text}'")
        
        if direct_text.lower() == websocket_text.lower():
            print(f"   Result: ✅ Identical transcriptions")
        else:
            print(f"   Result: ⚠️ Different transcriptions (may vary slightly)")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    print(f"   • Use Direct API for: Simple transcription tasks")
    print(f"   • Use WebSocket for: Interactive AI conversations")
    print(f"   • Consider WebSocket for: SRE agent integration")
    print(f"   • Consider Direct API for: Batch processing")

if __name__ == "__main__":
    asyncio.run(compare_speech_to_text_methods())
