#!/usr/bin/env python3
"""
Enhanced Speech Recognition Demo

This demo shows the complete flow of speech recognition with enhanced terminal output:
1. Speech-to-text with prominent terminal display
2. Automatic SRE agent processing
3. Text-to-speech response generation

Run this after starting the server to see the enhanced terminal output in action.
"""

import asyncio
import websockets
import json
import base64
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class EnhancedSpeechDemo:
    """Demo class showcasing enhanced speech recognition with terminal output"""
    
    def __init__(self):
        self.websocket_url = "ws://localhost:8001/speech-streaming/stream"
        self.websocket = None
    
    async def connect(self):
        """Connect to WebSocket server"""
        try:
            print("🔗 Connecting to WebSocket server...")
            self.websocket = await websockets.connect(self.websocket_url)
            print("✅ Connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            return False
    
    async def demonstrate_speech_recognition(self, audio_file_path: str):
        """Demonstrate speech recognition with enhanced output"""
        print("\n" + "="*100)
        print("🎤 SPEECH RECOGNITION DEMONSTRATION")
        print("="*100)
        print("🎯 WHAT TO WATCH:")
        print("   1. Client side: This terminal will show test progress")
        print("   2. Server side: The server terminal will show ENHANCED OUTPUT including:")
        print("      • Prominent speech recognition results")
        print("      • SRE agent processing with clear visual feedback")
        print("      • Response generation status")
        print("="*100)
        
        if not os.path.exists(audio_file_path):
            print(f"❌ Audio file not found: {audio_file_path}")
            return
        
        # Read and encode audio
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        message = {
            "type": "audio",
            "data": audio_b64,
            "metadata": {
                "voice_name": "en-US-AriaNeural"
            }
        }
        
        print(f"\n🎧 CLIENT: Sending audio file ({len(audio_data)} bytes)")
        print("📡 CLIENT: Audio data transmitted to server...")
        print("👀 CLIENT: Now check the SERVER TERMINAL for enhanced output!")
        print("🔄 CLIENT: Waiting for responses...")
        
        await self.websocket.send(json.dumps(message))
        
        # Collect responses with client-side feedback
        response_count = 0
        transcribed_text = ""
        
        while response_count < 3:  # Expect 3 responses
            try:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=30)
                response_data = json.loads(response)
                response_count += 1
                
                response_type = response_data.get('type')
                
                if response_type == 'transcription':
                    transcribed_text = response_data.get('data', '')
                    confidence = response_data.get('metadata', {}).get('confidence')
                    print(f"\n📥 CLIENT: Received transcription response")
                    print(f"🎯 CLIENT: Recognized text: '{transcribed_text}'")
                    print(f"📊 CLIENT: Confidence: {confidence}")
                    
                elif response_type == 'sre_response':
                    sre_text = response_data.get('data', '')
                    print(f"\n🤖 CLIENT: Received SRE agent response")
                    print(f"💬 CLIENT: Response preview: '{sre_text[:80]}{'...' if len(sre_text) > 80 else ''}'")
                    
                elif response_type == 'response_audio':
                    audio_length = response_data.get('metadata', {}).get('audio_length', 0)
                    voice_name = response_data.get('metadata', {}).get('voice_name', 'unknown')
                    print(f"\n🎵 CLIENT: Received response audio")
                    print(f"🔊 CLIENT: Audio length: {audio_length} bytes")
                    print(f"🎙️ CLIENT: Voice: {voice_name}")
                    break
                    
                elif response_type == 'error':
                    error_msg = response_data.get('data', 'Unknown error')
                    print(f"\n❌ CLIENT: Error received: {error_msg}")
                    break
                    
            except asyncio.TimeoutError:
                print("\n⏰ CLIENT: Timeout waiting for response")
                break
            except Exception as e:
                print(f"\n❌ CLIENT: Error receiving response: {str(e)}")
                break
        
        print("\n" + "="*100)
        print("✅ DEMONSTRATION COMPLETE!")
        print("="*100)
        print("📋 SUMMARY:")
        print(f"   • Input audio file: {audio_file_path}")
        print(f"   • Recognized speech: '{transcribed_text}'")
        print(f"   • Responses received: {response_count}")
        print("💡 ENHANCED OUTPUT:")
        print("   • Check the server terminal for detailed visual feedback")
        print("   • Speech recognition results are prominently displayed")
        print("   • SRE agent processing is clearly marked")
        print("   • Each step is visually separated for clarity")
        print("="*100)
    
    async def demonstrate_text_input(self, text: str):
        """Demonstrate text input processing"""
        print("\n" + "="*100)
        print("💬 TEXT INPUT DEMONSTRATION")
        print("="*100)
        print("🎯 WHAT TO WATCH:")
        print("   • Server terminal will show enhanced text processing output")
        print("   • SRE agent processing will be clearly visible")
        print("="*100)
        
        message = {
            "type": "text",
            "data": text,
            "metadata": {
                "with_audio": True,
                "voice_name": "en-US-AriaNeural"
            }
        }
        
        print(f"\n💬 CLIENT: Sending text input: '{text}'")
        print("👀 CLIENT: Check the SERVER TERMINAL for enhanced text processing output!")
        
        await self.websocket.send(json.dumps(message))
        
        response_count = 0
        while response_count < 2:  # Expect SRE response and audio
            try:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=20)
                response_data = json.loads(response)
                response_count += 1
                
                response_type = response_data.get('type')
                
                if response_type == 'sre_response':
                    sre_text = response_data.get('data', '')
                    print(f"\n🤖 CLIENT: SRE response received")
                    print(f"💬 CLIENT: Response: '{sre_text[:80]}{'...' if len(sre_text) > 80 else ''}'")
                    
                elif response_type == 'response_audio':
                    audio_length = response_data.get('metadata', {}).get('audio_length', 0)
                    print(f"\n🎵 CLIENT: Audio response received ({audio_length} bytes)")
                    break
                    
            except asyncio.TimeoutError:
                print("\n⏰ CLIENT: Timeout waiting for response")
                break
            except Exception as e:
                print(f"\n❌ CLIENT: Error: {str(e)}")
                break
        
        print("\n✅ TEXT INPUT DEMONSTRATION COMPLETE!")
    
    async def disconnect(self):
        """Disconnect from server"""
        if self.websocket:
            await self.websocket.close()
            print("🔌 Disconnected from server")

async def run_enhanced_demo():
    """Run the complete enhanced speech recognition demo"""
    print("🚀 ENHANCED SPEECH RECOGNITION DEMO")
    print("="*100)
    print("📋 This demo showcases the enhanced terminal output features:")
    print("   • Clear visual separation of processing steps")
    print("   • Prominent display of speech recognition results")
    print("   • Enhanced SRE agent processing feedback")
    print("   • Color-coded status indicators")
    print("\n💡 IMPORTANT: Keep both terminals visible:")
    print("   • This terminal: Shows client-side progress")
    print("   • Server terminal: Shows enhanced server-side output")
    print("="*100)
    
    demo = EnhancedSpeechDemo()
    
    if not await demo.connect():
        print("❌ Cannot proceed without connection")
        return
    
    try:
        # Demo 1: Speech recognition with audio file
        await demo.demonstrate_speech_recognition("./audio/simplequestion.wav")
        
        # Wait a moment between demos
        print("\n⏳ Pausing between demonstrations...")
        await asyncio.sleep(2)
        
        # Demo 2: Text input processing
        await demo.demonstrate_text_input("Show me the system health status and any current alerts")
        
    finally:
        await demo.disconnect()

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check server
    try:
        import requests
        response = requests.get("http://localhost:8001/speech-streaming/health", timeout=3)
        if response.status_code != 200:
            print("❌ Server health check failed")
            return False
        print("✅ Server is running")
    except Exception:
        print("❌ Server is not running on localhost:8001")
        print("💡 Start the server with: uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload")
        return False
    
    # Check audio file
    audio_file = "./audio/simplequestion.wav"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        print("💡 Please ensure the test audio file exists")
        return False
    print("✅ Test audio file found")
    
    return True

if __name__ == "__main__":
    print("🎤 Enhanced Speech Recognition Demo")
    print("="*50)
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please resolve the issues above.")
        sys.exit(1)
    
    print("\n🚀 Starting enhanced demo...")
    print("👀 Watch both terminals for complete experience!")
    
    asyncio.run(run_enhanced_demo())
