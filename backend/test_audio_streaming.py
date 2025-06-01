#!/usr/bin/env python3
"""
Simple WebSocket test for audio streaming functionality
"""

import asyncio
import websockets
import json
import base64
import os

async def test_websocket_streaming():
    """Test the WebSocket streaming endpoint"""
    uri = "ws://localhost:8001/speech-streaming/stream"
    
    print("🔗 Connecting to WebSocket...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Test 1: Send a text message
            text_message = {
                "type": "text",
                "data": "What is the current system status?",
                "metadata": {
                    "with_audio": True,
                    "voice_name": "en-US-AriaNeural"
                }
            }
            
            print("📤 Sending text message...")
            await websocket.send(json.dumps(text_message))
            
            # Receive responses
            response_count = 0
            while response_count < 3:  # Expect sre_response and response_audio
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    response_data = json.loads(response)
                    
                    print(f"📥 Received response {response_count + 1}:")
                    print(f"   Type: {response_data.get('type')}")
                    print(f"   Data length: {len(response_data.get('data', ''))}")
                    
                    if response_data.get('type') == 'response_audio':
                        metadata = response_data.get('metadata', {})
                        print(f"   Audio length: {metadata.get('audio_length')} bytes")
                        print(f"   Voice: {metadata.get('voice_name')}")
                        
                    response_count += 1
                    
                    # Stop after receiving audio response
                    if response_data.get('type') == 'response_audio':
                        break
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"❌ Error receiving response: {e}")
                    break
            
            # Test 2: Send an audio message
            audio_file_path = "./audio/simplequestion.wav"  # Path to test audio file
            if not os.path.exists(audio_file_path):
                print(f"❌ Test audio file not found: {audio_file_path}")
                return

            with open(audio_file_path, "rb") as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode("utf-8")

            audio_message = {
                "type": "audio",
                "data": audio_data,
                "metadata": {
                    "voice_name": "en-US-AriaNeural"
                }
            }

            print("📤 Sending audio message...")
            await websocket.send(json.dumps(audio_message))

            # Receive responses
            response_count = 0
            while response_count < 3:  # Expect transcription and response_audio
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    response_data = json.loads(response)

                    print(f"📥 Received response {response_count + 1}:")
                    print(f"   Type: {response_data.get('type')}")
                    print(f"   Data length: {len(response_data.get('data', ''))}")

                    if response_data.get('type') == 'response_audio':
                        metadata = response_data.get('metadata', {})
                        print(f"   Audio length: {metadata.get('audio_length')} bytes")
                        print(f"   Voice: {metadata.get('voice_name')}")

                    response_count += 1

                    # Stop after receiving audio response
                    if response_data.get('type') == 'response_audio':
                        break

                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"❌ Error receiving response: {e}")
                    break
            
            print("✅ WebSocket test completed successfully!")
            
    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")

if __name__ == "__main__":
    print("🧪 Starting WebSocket audio streaming test")
    asyncio.run(test_websocket_streaming())
