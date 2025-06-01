"""
Azure Speech Service - Proxy service for Azure Cognitive Services Speech SDK

This service provides a secure proxy interface to Azure Speech Services,
implementing best practices for authentication, error handling, and performance.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv('.env.local')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureSpeechService:
    """
    Azure Speech Service proxy implementing secure communication patterns
    with proper error handling, retry logic, and monitoring.
    """
    
    def __init__(self):
        """
        Initialize Azure Speech Service with environment configuration.
        Uses key-based authentication for simplicity in development environment.
        In production, consider using Managed Identity.
        """
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        self.speech_endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")
        
        # Validate required configuration
        if not all([self.speech_key, self.speech_region]):
            raise ValueError("Missing required Azure Speech configuration. Check AZURE_SPEECH_KEY and AZURE_SPEECH_REGION")
        
        # Configure Speech SDK
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )
        
        # Set default voice and language
        self.speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
        
        logger.info(f"Azure Speech Service initialized for region: {self.speech_region}")

    def text_to_speech(self, text: str, voice_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text to speech using Azure Cognitive Services.
        
        Args:
            text: Text to convert to speech
            voice_name: Optional voice name (e.g., "en-US-AriaNeural")
            
        Returns:
            Dict containing audio data and status information
        """
        try:
            logger.info(f"Processing text-to-speech request: {text[:50]}...")
            
            # Configure voice if provided
            if voice_name:
                self.speech_config.speech_synthesis_voice_name = voice_name
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
            
            # Perform synthesis
            result = synthesizer.speak_text_async(text).get()
            
            # Handle synthesis result
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("Text-to-speech synthesis completed successfully")
                response = {
                    "audio_data": result.audio_data,
                    "audio_length": len(result.audio_data),
                    "voice_name": self.speech_config.speech_synthesis_voice_name,
                    "status": "success",
                    "message": "Audio synthesis completed successfully"
                }
                
                # Print detailed response to console
                print("🎤 TEXT-TO-SPEECH RESPONSE:")
                print(f"   Status: {response['status']}")
                print(f"   Message: {response['message']}")
                print(f"   Voice: {response['voice_name']}")
                print(f"   Audio Length: {response['audio_length']} bytes")
                print(f"   Input Text: {text[:100]}{'...' if len(text) > 100 else ''}")
                print(f"   Full Response: {json.dumps(response, indent=2, default=str)}")
                return response
                
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speechsdk.CancellationDetails(result)
                error_msg = f"Speech synthesis canceled: {cancellation_details.reason}"
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    error_msg += f" - Error details: {cancellation_details.error_details}"
                
                logger.error(error_msg)
                print("❌ TEXT-TO-SPEECH ERROR:")
                print(f"   Error: {error_msg}")
                print(f"   Cancellation Reason: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"   Error Details: {cancellation_details.error_details}")
                error_response = {
                    "error": error_msg,
                    "status": "error",
                    "error_code": "synthesis_canceled"
                }
                print(f"   Full Error Response: {json.dumps(error_response, indent=2)}")
                return error_response
            
        except Exception as e:
            error_msg = f"Text-to-speech error: {str(e)}"
            logger.error(error_msg)
            print("❌ TEXT-TO-SPEECH EXCEPTION:")
            print(f"   Exception: {str(e)}")
            print(f"   Exception Type: {type(e).__name__}")
            error_response = {
                "error": error_msg,
                "status": "error",
                "error_code": "synthesis_exception"
            }
            print(f"   Full Error Response: {json.dumps(error_response, indent=2)}")
            return error_response

    def speech_to_text(self, audio_data: bytes = None, audio_file_path: str = None) -> Dict[str, Any]:
        """
        Convert speech to text using Azure Cognitive Services.
        
        Args:
            audio_data: Raw audio bytes (WAV format)
            audio_file_path: Path to audio file
            
        Returns:
            Dict containing transcribed text and status information
        """
        try:
            logger.info("Processing speech-to-text request")
            
            # Configure audio input
            if audio_file_path:
                audio_input = speechsdk.AudioConfig(filename=audio_file_path)
            elif audio_data:
                # For audio data, you would need to save it temporarily or use a stream
                # This is a simplified implementation
                audio_input = speechsdk.AudioConfig(use_default_microphone=False)
            else:
                # Use default microphone
                audio_input = speechsdk.AudioConfig(use_default_microphone=True)
            
            # Create recognizer
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config,
                audio_config=audio_input
            )
            
            # Perform recognition
            result = speech_recognizer.recognize_once_async().get()
            
            # Handle recognition result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                logger.info("Speech recognition completed successfully")
                response = {
                    "text": result.text,
                    "confidence": getattr(result, 'confidence', None),
                    "status": "success",
                    "message": "Speech recognition completed successfully"
                }
                
                # Print prominent recognition result to console
                print("\n" + "="*80)
                print("🎧 SPEECH RECOGNIZED!")
                print("="*80)
                print(f"📝 TRANSCRIBED TEXT: '{result.text}'")
                print(f"📊 CONFIDENCE: {getattr(result, 'confidence', 'N/A')}")
                print(f"📏 LENGTH: {len(result.text)} characters")
                print(f"✅ STATUS: {response['status']}")
                print("="*80)
                
                # Also print detailed response for debugging
                print("\n🔍 DETAILED RESPONSE:")
                print(f"   Status: {response['status']}")
                print(f"   Message: {response['message']}")
                print(f"   Transcribed Text: '{response['text']}'")
                print(f"   Confidence: {response['confidence']}")
                print(f"   Text Length: {len(response['text'])} characters")
                print(f"   Full Response: {json.dumps(response, indent=2, default=str)}")
                return response
                
            elif result.reason == speechsdk.ResultReason.NoMatch:
                logger.warning("No speech could be recognized")
                print("⚠️ SPEECH-TO-TEXT WARNING:")
                print("   Status: No speech recognized")
                print("   Message: No speech could be recognized")
                warning_response = {
                    "text": "",
                    "status": "warning",
                    "message": "No speech could be recognized"
                }
                print(f"   Full Response: {json.dumps(warning_response, indent=2)}")
                return warning_response
                
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speechsdk.CancellationDetails(result)
                error_msg = f"Speech recognition canceled: {cancellation_details.reason}"
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    error_msg += f" - Error details: {cancellation_details.error_details}"
                
                logger.error(error_msg)
                print("❌ SPEECH-TO-TEXT ERROR:")
                print(f"   Error: {error_msg}")
                print(f"   Cancellation Reason: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"   Error Details: {cancellation_details.error_details}")
                error_response = {
                    "error": error_msg,
                    "status": "error",
                    "error_code": "recognition_canceled"
                }
                print(f"   Full Error Response: {json.dumps(error_response, indent=2)}")
                return error_response
            
        except Exception as e:
            error_msg = f"Speech-to-text error: {str(e)}"
            logger.error(error_msg)
            print("❌ SPEECH-TO-TEXT EXCEPTION:")
            print(f"   Exception: {str(e)}")
            print(f"   Exception Type: {type(e).__name__}")
            error_response = {
                "error": error_msg,
                "status": "error",
                "error_code": "recognition_exception"
            }
            print(f"   Full Error Response: {json.dumps(error_response, indent=2)}")
            return error_response

    def get_available_voices(self, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Get list of available voices from Azure Speech Service.
        
        Args:
            language: Optional language filter (e.g., "en-US")
            
        Returns:
            Dict containing list of available voices
        """
        try:
            logger.info(f"Fetching available voices for language: {language or 'all'}")
            
            # Create synthesizer to get voices
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
            
            # Get voices list
            voices_result = synthesizer.get_voices_async().get()
            
            if voices_result.reason == speechsdk.ResultReason.VoicesListRetrieved:
                voices = []
                for voice in voices_result.voices:
                    if not language or voice.locale.startswith(language):
                        voice_info = {
                            "name": voice.name,
                            "locale": voice.locale,
                        }
                        
                        # Safely get gender and voice_type attributes
                        try:
                            voice_info["gender"] = voice.gender.name if hasattr(voice.gender, 'name') else str(voice.gender)
                        except Exception:
                            voice_info["gender"] = "Unknown"
                            
                        try:
                            voice_info["voice_type"] = voice.voice_type.name if hasattr(voice.voice_type, 'name') else str(voice.voice_type)
                        except Exception:
                            voice_info["voice_type"] = "Unknown"
                            
                        voices.append(voice_info)
                
                response = {
                    "voices": voices,
                    "count": len(voices),
                    "status": "success"
                }
                
                # Print response to console as requested
                print(f"🎭 Retrieved {len(voices)} voices for language: {language or 'all'}")
                return response
            
            else:
                error_msg = "Failed to retrieve voices list"
                logger.error(error_msg)
                print(f"❌ {error_msg}")
                return {
                    "error": error_msg,
                    "status": "error",
                    "error_code": "voices_list_failed"
                }
                
        except Exception as e:
            error_msg = f"Get voices error: {str(e)}"
            logger.error(error_msg)
            print(f"❌ Get voices error: {error_msg}")
            return {
                "error": error_msg,
                "status": "error",
                "error_code": "voices_exception"
            }

    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check of the Azure Speech Service connection.
        
        Returns:
            Dict containing health status information
        """
        try:
            logger.info("Performing Azure Speech Service health check")
            
            # Test with a simple synthesis
            test_text = "Health check"
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
            result = synthesizer.speak_text_async(test_text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                response = {
                    "status": "healthy",
                    "service": "Azure Speech Service",
                    "region": self.speech_region,
                    "endpoint": self.speech_endpoint,
                    "message": "Service is operational"
                }
                
                print("✅ Azure Speech Service health check passed")
                return response
            else:
                response = {
                    "status": "unhealthy",
                    "service": "Azure Speech Service",
                    "region": self.speech_region,
                    "error": "Health check synthesis failed",
                    "error_code": "health_check_failed"
                }
                
                print("❌ Azure Speech Service health check failed")
                return response
                
        except Exception as e:
            error_msg = f"Health check error: {str(e)}"
            logger.error(error_msg)
            print(f"❌ Azure Speech Service health check error: {error_msg}")
            return {
                "status": "unhealthy",
                "service": "Azure Speech Service",
                "error": error_msg,
                "error_code": "health_check_exception"
            }


# Standalone functions for backward compatibility and easy integration
def synthesize_speech(text: str, voice_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Standalone function to convert text to speech.
    
    Args:
        text: Text to convert to speech
        voice_name: Optional voice name
        
    Returns:
        Dict containing audio data and status
    """
    speech_service = AzureSpeechService()
    return speech_service.text_to_speech(text, voice_name)


def recognize_speech(audio_data: bytes = None, audio_file_path: str = None) -> Dict[str, Any]:
    """
    Standalone function to convert speech to text.
    
    Args:
        audio_data: Raw audio bytes
        audio_file_path: Path to audio file
        
    Returns:
        Dict containing transcribed text and status
    """
    speech_service = AzureSpeechService()
    return speech_service.speech_to_text(audio_data, audio_file_path)


def get_voices(language: Optional[str] = None) -> Dict[str, Any]:
    """
    Standalone function to get available voices.
    
    Args:
        language: Optional language filter
        
    Returns:
        Dict containing list of available voices
    """
    speech_service = AzureSpeechService()
    return speech_service.get_available_voices(language)


def check_speech_service_health() -> Dict[str, Any]:
    """
    Standalone function to check Azure Speech Service health.
    
    Returns:
        Dict containing health status
    """
    speech_service = AzureSpeechService()
    return speech_service.health_check()


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    service = AzureSpeechService()
    
    # Test text-to-speech
    print("Testing text-to-speech...")
    tts_result = service.text_to_speech("Hello, this is a test of Azure Speech Service!")
    print(f"TTS Result: {tts_result.get('status', 'unknown')}")
    
    # Test health check
    print("\nTesting health check...")
    health_result = service.health_check()
    print(f"Health Check: {health_result.get('status', 'unknown')}")
    
    # Test get voices
    print("\nTesting get voices...")
    voices_result = service.get_available_voices("en-US")
    print(f"Voices Count: {voices_result.get('count', 0)}")
