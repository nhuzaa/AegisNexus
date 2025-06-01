#!/usr/bin/env python3
"""
Test script for WebSocket speech-to-text functionality
"""

import os
import asyncio
import websockets
import json
import base64
import sys
import time
from typing import Dict, Any, Optional

# Add the parent directory to the path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class WebSocketSpeechToTextTester:
    """Test class for WebSocket speech-to-text functionality"""
    
    def __init__(self, websocket_url: str = "ws://localhost:8001/speech-streaming/stream"):
        self.websocket_url = websocket_url
        self.websocket = None
        
    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            print(f"🔗 Connecting to WebSocket: {self.websocket_url}")
            self.websocket = await websockets.connect(self.websocket_url)
            print("✅ WebSocket connection established")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to WebSocket: {str(e)}")
            return False
    
    async def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.websocket:
            await self.websocket.close()
            print("🔌 WebSocket connection closed")
    
    async def test_speech_to_text_from_file(self, audio_file_path: str) -> Dict[str, Any]:
        """Test speech-to-text functionality using an audio file"""
        print(f"🔍 Testing speech-to-text with file: {audio_file_path}")
        
        if not os.path.exists(audio_file_path):
            error_msg = f"Audio file not found: {audio_file_path}"
            print(f"❌ {error_msg}")
            return {
                "status": "error",
                "error": error_msg,
                "error_code": "file_not_found"
            }
        
        try:
            # Read and encode audio file
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
            
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Create audio message
            message = {
                "type": "audio",
                "data": audio_b64,
                "metadata": {
                    "voice_name": "en-US-AriaNeural"
                }
            }
            
            print(f"📤 Sending audio data ({len(audio_data)} bytes)...")
            await self.websocket.send(json.dumps(message))
            
            # Collect responses
            responses = []
            transcription_result = None
            timeout_seconds = 30
            
            print("📥 Waiting for responses...")
            
            while len(responses) < 3:  # Expect transcription, sre_response, and response_audio
                try:
                    response = await asyncio.wait_for(
                        self.websocket.recv(), 
                        timeout=timeout_seconds
                    )
                    response_data = json.loads(response)
                    responses.append(response_data)
                    
                    response_type = response_data.get('type')
                    print(f"📋 Received {response_type} response")
                    
                    if response_type == 'transcription':
                        transcribed_text = response_data.get('data', '')
                        confidence = response_data.get('metadata', {}).get('confidence')
                        print(f"✅ Transcribed Text: '{transcribed_text}'")
                        print(f"📊 Confidence: {confidence}")
                        
                        transcription_result = {
                            "status": "success",
                            "text": transcribed_text,
                            "confidence": confidence,
                            "message": "Speech-to-text completed successfully"
                        }
                    
                    elif response_type == 'error':
                        error_data = response_data.get('data', 'Unknown error')
                        error_code = response_data.get('metadata', {}).get('error_code', 'unknown_error')
                        print(f"❌ Error: {error_data}")
                        print(f"📋 Error Code: {error_code}")
                        
                        return {
                            "status": "error",
                            "error": error_data,
                            "error_code": error_code
                        }
                    
                    elif response_type == 'sre_response':
                        sre_text = response_data.get('data', '')
                        print(f"🤖 SRE Response: {sre_text[:100]}{'...' if len(sre_text) > 100 else ''}")
                    
                    elif response_type == 'response_audio':
                        audio_length = response_data.get('metadata', {}).get('audio_length', 0)
                        voice_name = response_data.get('metadata', {}).get('voice_name', 'unknown')
                        print(f"🎵 Response Audio: {audio_length} bytes, Voice: {voice_name}")
                        break  # Stop after receiving audio response
                        
                except asyncio.TimeoutError:
                    print(f"⏰ Timeout waiting for response after {timeout_seconds} seconds")
                    break
                except Exception as e:
                    print(f"❌ Error receiving response: {str(e)}")
                    break
            
            if transcription_result:
                print("✅ Speech-to-text test completed successfully!")
                return transcription_result
            else:
                return {
                    "status": "error",
                    "error": "No transcription response received",
                    "error_code": "no_transcription"
                }
                
        except Exception as e:
            error_msg = f"Exception during speech-to-text test: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "status": "error",
                "error": error_msg,
                "error_code": "test_exception"
            }
    
    async def test_text_only_mode(self, text: str) -> Dict[str, Any]:
        """Test text-only mode (bypass speech-to-text)"""
        print(f"💬 Testing text-only mode with: '{text}'")
        
        try:
            message = {
                "type": "text",
                "data": text,
                "metadata": {
                    "with_audio": True,
                    "voice_name": "en-US-AriaNeural"
                }
            }
            
            print("📤 Sending text message...")
            await self.websocket.send(json.dumps(message))
            
            responses = []
            while len(responses) < 2:  # Expect sre_response and response_audio
                try:
                    response = await asyncio.wait_for(self.websocket.recv(), timeout=20.0)
                    response_data = json.loads(response)
                    responses.append(response_data)
                    
                    response_type = response_data.get('type')
                    print(f"📋 Received {response_type} response")
                    
                    if response_type == 'sre_response':
                        sre_text = response_data.get('data', '')
                        print(f"🤖 SRE Response: {sre_text[:100]}{'...' if len(sre_text) > 100 else ''}")
                    
                    elif response_type == 'response_audio':
                        audio_length = response_data.get('metadata', {}).get('audio_length', 0)
                        print(f"🎵 Response Audio: {audio_length} bytes")
                        break
                    
                    elif response_type == 'error':
                        error_data = response_data.get('data', 'Unknown error')
                        print(f"❌ Error: {error_data}")
                        return {
                            "status": "error",
                            "error": error_data,
                            "error_code": response_data.get('metadata', {}).get('error_code', 'unknown_error')
                        }
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"❌ Error receiving response: {str(e)}")
                    break
            
            print("✅ Text-only mode test completed!")
            return {
                "status": "success",
                "message": "Text-only mode test completed successfully"
            }
            
        except Exception as e:
            error_msg = f"Exception during text-only test: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "status": "error",
                "error": error_msg,
                "error_code": "text_test_exception"
            }

async def run_websocket_speech_tests():
    """Run all WebSocket speech-to-text tests"""
    print("🧪 Starting WebSocket Speech-to-Text Tests with Enhanced Terminal Output")
    print("=" * 80)
    print("📝 This test demonstrates:")
    print("   1. Speech recognition with prominent terminal display")
    print("   2. Automatic SRE agent processing of recognized speech")
    print("   3. Clear visual feedback in the server terminal")
    print("   4. Watch the server terminal for enhanced output!")
    print("=" * 80)
    
    tester = WebSocketSpeechToTextTester()
    
    # Test connection
    if not await tester.connect():
        print("❌ Cannot proceed without WebSocket connection")
        return
    
    try:
        # Test 1: Speech-to-text with audio file
        print("\n📋 Test 1: Speech-to-text from audio file")
        print("-" * 40)
        audio_file_path = "./audio/simplequestion.wav"
        result1 = await tester.test_speech_to_text_from_file(audio_file_path)
        
        # Test 2: Text-only mode (bypass speech recognition)
        print("\n📋 Test 2: Text-only mode")
        print("-" * 40)
        test_text = "What is the current system status?"
        result2 = await tester.test_text_only_mode(test_text)
        
        # Summary
        print("\n📊 Test Summary")
        print("=" * 50)
        print(f"Speech-to-text test: {'✅ PASSED' if result1.get('status') == 'success' else '❌ FAILED'}")
        print(f"Text-only test: {'✅ PASSED' if result2.get('status') == 'success' else '❌ FAILED'}")
        
        if result1.get('status') == 'success':
            print(f"Transcribed text: '{result1.get('text', 'N/A')}'")
            print(f"Confidence: {result1.get('confidence', 'N/A')}")
        
    finally:
        await tester.disconnect()

def check_server_status():
    """Check if the server is running"""
    try:
        import requests
        response = requests.get("http://localhost:8001/speech-streaming/health", timeout=3)
        return response.status_code == 200
    except Exception:
        return False

if __name__ == "__main__":
    # Check if server is running
    if not check_server_status():
        print("❌ Server is not running on localhost:8001")
        print("💡 Please start the server first:")
        print("   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload")
        sys.exit(1)
    
    # Check if test audio file exists
    audio_file_path = "./audio/simplequestion.wav"
    if not os.path.exists(audio_file_path):
        print(f"❌ Test audio file not found: {audio_file_path}")
        print("💡 Please ensure the audio file exists for testing")
        sys.exit(1)
    
    # Run tests
    asyncio.run(run_websocket_speech_tests())
