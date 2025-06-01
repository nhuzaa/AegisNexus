#!/usr/bin/env python3
"""
Test script for Azure Speech Service speech-to-text functionality
"""

import os
from app.services.azure_speech_service import AzureSpeechService

def test_speech_to_text(audio_file_path):
    """Test speech-to-text functionality"""
    print("🔍 Testing speech-to-text...")
    
    try:
        speech_service = AzureSpeechService()
        result = speech_service.speech_to_text(audio_file_path=audio_file_path)
        
        if result.get("status") == "success":
            print("✅ Speech-to-text succeeded!")
            print(f"Transcribed Text: {result.get('text')}")
            print(f"Confidence: {result.get('confidence')}")
        else:
            print("❌ Speech-to-text failed!")
            print(f"Error: {result.get('error')}")
            print(f"Error Code: {result.get('error_code')}")
    except Exception as e:
        print(f"❌ Exception during speech-to-text: {str(e)}")

if __name__ == "__main__":
    audio_file_path = "./audio/simplequestion.wav"  # Replace with the path to your test audio file
    if not os.path.exists(audio_file_path):
        print(f"❌ Test audio file not found: {audio_file_path}")
    else:
        test_speech_to_text(audio_file_path)
