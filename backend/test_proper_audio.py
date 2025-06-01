#!/usr/bin/env python3
"""
WebSocket client to test audio streaming with proper WAV format
"""

import asyncio
import websockets
import json
import base64
import wave
import numpy as np

def create_test_wav_audio():
    """Create a simple test WAV audio file in memory"""
    # Create a simple sine wave audio (440 Hz for 1 second)
    sample_rate = 16000
    duration = 1.0  # seconds
    frequency = 440  # Hz (A note)
    
    # Generate sine wave
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create WAV file in memory
    import io
    wav_buffer = io.BytesIO()
    
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    wav_buffer.seek(0)
    return wav_buffer.getvalue()

async def test_websocket_with_audio():
    """Test WebSocket with properly formatted audio"""
    uri = "ws://localhost:8001/speech-streaming/stream"
    
    print("🔗 Connecting to WebSocket...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Create test audio
            print("🎵 Creating test WAV audio...")
            test_audio_bytes = create_test_wav_audio()
            print(f"📦 Generated {len(test_audio_bytes)} bytes of WAV audio")
            
            # Encode as base64
            audio_base64 = base64.b64encode(test_audio_bytes).decode('utf-8')
            
            # Send audio message
            audio_message = {
                "type": "audio",
                "data": audio_base64,
                "metadata": {
                    "voice_name": "en-US-AriaNeural",
                    "format": "wav",
                    "sample_rate": 16000,
                    "channels": 1,
                    "bit_depth": 16
                }
            }
            
            print("📤 Sending audio message...")
            await websocket.send(json.dumps(audio_message))
            
            # Receive responses
            response_count = 0
            max_responses = 3
            
            while response_count < max_responses:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    response_data = json.loads(response)
                    
                    print(f"📥 Received response {response_count + 1}:")
                    print(f"   Type: {response_data.get('type')}")
                    
                    if response_data.get('type') == 'error':
                        print(f"   ❌ Error: {response_data.get('data')}")
                        error_metadata = response_data.get('metadata', {})
                        if 'suggestion' in error_metadata:
                            print(f"   💡 Suggestion: {error_metadata['suggestion']}")
                        break
                    elif response_data.get('type') == 'transcription':
                        print(f"   📝 Transcribed: '{response_data.get('data')}'")
                    elif response_data.get('type') == 'sre_response':
                        print(f"   🤖 SRE Response: {response_data.get('data')}")
                    elif response_data.get('type') == 'response_audio':
                        metadata = response_data.get('metadata', {})
                        print(f"   🎤 Audio response: {metadata.get('audio_length')} bytes")
                        print(f"   🎭 Voice: {metadata.get('voice_name')}")
                        break
                    
                    response_count += 1
                    
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"❌ Error receiving response: {e}")
                    break
            
            print("✅ Audio test completed")
            
    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")

async def test_text_message():
    """Test with a simple text message first"""
    uri = "ws://localhost:8001/speech-streaming/stream"
    
    print("\n🔗 Testing text message...")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected successfully!")
            
            # Send text message
            text_message = {
                "type": "text",
                "data": "Hello, this is a test message",
                "metadata": {
                    "with_audio": True,
                    "voice_name": "en-US-AriaNeural"
                }
            }
            
            print("📤 Sending text message...")
            await websocket.send(json.dumps(text_message))
            
            # Receive responses
            response_count = 0
            while response_count < 2:  # Expect text response and audio response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                    response_data = json.loads(response)
                    
                    print(f"📥 Received response {response_count + 1}:")
                    print(f"   Type: {response_data.get('type')}")
                    
                    if response_data.get('type') == 'error':
                        print(f"   ❌ Error: {response_data.get('data')}")
                        break
                    elif response_data.get('type') == 'sre_response':
                        print(f"   🤖 SRE Response: {response_data.get('data')}")
                    elif response_data.get('type') == 'response_audio':
                        metadata = response_data.get('metadata', {})
                        print(f"   🎤 Audio response: {metadata.get('audio_length')} bytes")
                        break
                    
                    response_count += 1
                    
                except asyncio.TimeoutError:
                    print("⏰ Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"❌ Error receiving response: {e}")
                    break
            
            print("✅ Text test completed")
            
    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")

if __name__ == "__main__":
    print("🧪 Starting WebSocket audio streaming tests")
    
    try:
        import numpy as np
        
        # Test 1: Simple text message
        asyncio.run(test_text_message())
        
        # Test 2: Audio message with proper WAV format
        asyncio.run(test_websocket_with_audio())
        
    except ImportError:
        print("❌ numpy not available, install with: pip install numpy")
        print("🔄 Running text-only test...")
        asyncio.run(test_text_message())
