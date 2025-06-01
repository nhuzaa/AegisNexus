#!/usr/bin/env python3
"""
WebSocket Audio Streaming Client Example

This script demonstrates how to use the WebSocket streaming endpoint
for real-time audio interaction with the SRE agent.
"""

import asyncio
import websockets
import json
import base64
import wave
import io
from pathlib import Path


class AudioStreamingClient:
    """Client for WebSocket audio streaming with SRE agent"""
    
    def __init__(self, websocket_url: str = "ws://localhost:8000/speech-streaming/stream"):
        self.websocket_url = websocket_url
        self.websocket = None
    
    async def connect(self):
        """Connect to the WebSocket server"""
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            print(f"🔗 Connected to {self.websocket_url}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from the WebSocket server"""
        if self.websocket:
            await self.websocket.close()
            print("🔌 Disconnected from server")
    
    async def send_audio_file(self, audio_file_path: str, voice_name: str = "en-US-AriaNeural"):
        """Send an audio file for processing"""
        try:
            # Read and encode audio file
            with open(audio_file_path, "rb") as f:
                audio_data = f.read()
            
            audio_b64 = base64.b64encode(audio_data).decode('utf-8')
            
            # Create message
            message = {
                "type": "audio",
                "data": audio_b64,
                "metadata": {
                    "voice_name": voice_name
                }
            }
            
            print(f"🎵 Sending audio file: {audio_file_path}")
            await self.websocket.send(json.dumps(message))
            
        except Exception as e:
            print(f"❌ Error sending audio: {e}")
    
    async def send_text(self, text: str, with_audio: bool = True, voice_name: str = "en-US-AriaNeural"):
        """Send text directly to SRE agent"""
        try:
            message = {
                "type": "text",
                "data": text,
                "metadata": {
                    "with_audio": with_audio,
                    "voice_name": voice_name
                }
            }
            
            print(f"💬 Sending text: {text}")
            await self.websocket.send(json.dumps(message))
            
        except Exception as e:
            print(f"❌ Error sending text: {e}")
    
    async def listen_for_responses(self):
        """Listen for responses from the server"""
        try:
            while True:
                response = await self.websocket.recv()
                data = json.loads(response)
                
                message_type = data.get("type")
                content = data.get("data")
                metadata = data.get("metadata", {})
                
                if message_type == "transcription":
                    print(f"🎧 Transcription: {content}")
                    confidence = metadata.get("confidence")
                    if confidence:
                        print(f"   Confidence: {confidence}")
                
                elif message_type == "sre_response":
                    print(f"🤖 SRE Response: {content}")
                    if metadata.get("enhanced_context"):
                        print("   ✅ Enhanced with SRE tools data")
                
                elif message_type == "response_audio":
                    print(f"🎤 Received audio response ({metadata.get('audio_length', 0)} bytes)")
                    voice = metadata.get("voice_name", "Unknown")
                    print(f"   Voice: {voice}")
                    
                    # Optionally save audio to file
                    audio_data = base64.b64decode(content)
                    output_file = f"response_audio_{len(audio_data)}.wav"
                    with open(output_file, "wb") as f:
                        f.write(audio_data)
                    print(f"   Saved to: {output_file}")
                
                elif message_type == "error":
                    print(f"❌ Error: {content}")
                    error_code = metadata.get("error_code", "unknown")
                    print(f"   Error Code: {error_code}")
                
                else:
                    print(f"📨 Unknown message type: {message_type}")
                    print(f"   Content: {content}")
                
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed by server")
        except Exception as e:
            print(f"❌ Error listening for responses: {e}")


async def interactive_session():
    """Interactive session for testing the streaming client"""
    client = AudioStreamingClient()
    
    # Connect to server
    if not await client.connect():
        return
    
    # Start listening for responses in background
    listen_task = asyncio.create_task(client.listen_for_responses())
    
    try:
        print("\n🎙️  Audio Streaming Client - Interactive Mode")
        print("Commands:")
        print("  text <message>     - Send text to SRE agent")
        print("  audio <file>       - Send audio file")
        print("  quit              - Exit")
        print()
        
        while True:
            try:
                command = input(">>> ").strip()
                
                if command.lower() == "quit":
                    break
                
                elif command.startswith("text "):
                    text_message = command[5:]
                    await client.send_text(text_message)
                
                elif command.startswith("audio "):
                    audio_file = command[6:]
                    if Path(audio_file).exists():
                        await client.send_audio_file(audio_file)
                    else:
                        print(f"❌ Audio file not found: {audio_file}")
                
                elif command == "help":
                    print("Available commands:")
                    print("  text <message>     - Send text to SRE agent")
                    print("  audio <file>       - Send audio file")
                    print("  quit              - Exit")
                
                else:
                    print("❌ Unknown command. Type 'help' for available commands.")
                
                # Small delay to allow responses to be processed
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                break
            except EOFError:
                break
    
    finally:
        # Cancel listening task and disconnect
        listen_task.cancel()
        await client.disconnect()


async def demo_session():
    """Demo session with predefined interactions"""
    client = AudioStreamingClient()
    
    # Connect to server
    if not await client.connect():
        return
    
    # Start listening for responses
    listen_task = asyncio.create_task(client.listen_for_responses())
    
    try:
        print("\n🎭 Running Demo Session...")
        
        # Test text interaction
        print("\n1. Testing text interaction with SRE agent...")
        await client.send_text("What is the current system health status?")
        await asyncio.sleep(3)
        
        # Test another SRE query
        print("\n2. Testing SRE tools integration...")
        await client.send_text("Show me recent alerts and CPU metrics")
        await asyncio.sleep(3)
        
        # Test incident response
        print("\n3. Testing incident response workflow...")
        await client.send_text("We have a high CPU alert, what should I do?")
        await asyncio.sleep(3)
        
        print("\n✅ Demo completed!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
    
    finally:
        listen_task.cancel()
        await client.disconnect()


def create_sample_audio():
    """Create a sample WAV file for testing (silence)"""
    sample_rate = 16000
    duration = 2  # seconds
    filename = "sample_test_audio.wav"
    
    # Generate silence (you could replace with actual audio data)
    frames = sample_rate * duration
    audio_data = b'\x00\x00' * frames  # 16-bit silence
    
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)
    
    print(f"📁 Created sample audio file: {filename}")
    return filename


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        # Run demo session
        asyncio.run(demo_session())
    elif len(sys.argv) > 1 and sys.argv[1] == "create-sample":
        # Create sample audio file
        create_sample_audio()
    else:
        # Run interactive session
        asyncio.run(interactive_session())
