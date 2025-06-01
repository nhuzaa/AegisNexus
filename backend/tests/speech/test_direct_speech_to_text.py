#!/usr/bin/env python3
"""
Test script for Azure Speech Service speech-to-text functionality (Direct API)
"""

import os
import sys

# Add the parent directory to the path to import app modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.services.azure_speech_service import AzureSpeechService

def test_speech_to_text(audio_file_path):
    """Test speech-to-text functionality using direct Azure Speech Service"""
    print("🔍 Testing speech-to-text (Direct API)...")
    
    try:
        speech_service = AzureSpeechService()
        result = speech_service.speech_to_text(audio_file_path=audio_file_path)
        
        if result.get("status") == "success":
            print("✅ Speech-to-text succeeded!")
            print(f"📝 Transcribed Text: {result.get('text')}")
            print(f"📊 Confidence: {result.get('confidence')}")
            return result
        else:
            print("❌ Speech-to-text failed!")
            print(f"💥 Error: {result.get('error')}")
            print(f"📋 Error Code: {result.get('error_code')}")
            return result
    except Exception as e:
        error_msg = f"Exception during speech-to-text: {str(e)}"
        print(f"❌ {error_msg}")
        return {
            "status": "error",
            "error": error_msg,
            "error_code": "test_exception"
        }

def test_speech_service_health():
    """Test Azure Speech Service health check"""
    print("🏥 Testing Azure Speech Service health...")
    
    try:
        speech_service = AzureSpeechService()
        result = speech_service.health_check()
        
        if result.get("status") == "healthy":
            print("✅ Azure Speech Service is healthy!")
        else:
            print("❌ Azure Speech Service health check failed!")
            print(f"💥 Error: {result.get('error')}")
    except Exception as e:
        print(f"❌ Health check exception: {str(e)}")

def run_direct_api_tests():
    """Run all direct API speech-to-text tests"""
    print("🧪 Starting Direct API Speech-to-Text Tests")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n📋 Test 1: Azure Speech Service Health Check")
    print("-" * 40)
    test_speech_service_health()
    
    # Test 2: Speech-to-text with audio file
    print("\n📋 Test 2: Speech-to-text from audio file")
    print("-" * 40)
    audio_file_path = "./audio/simplequestion.wav"
    
    if not os.path.exists(audio_file_path):
        print(f"❌ Test audio file not found: {audio_file_path}")
        print("💡 Please ensure the audio file exists for testing")
        return
    
    result = test_speech_to_text(audio_file_path)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"Speech-to-text test: {'✅ PASSED' if result.get('status') == 'success' else '❌ FAILED'}")
    
    if result.get('status') == 'success':
        print(f"📝 Transcribed text: '{result.get('text', 'N/A')}'")
        print(f"📊 Confidence: {result.get('confidence', 'N/A')}")

if __name__ == "__main__":
    run_direct_api_tests()
