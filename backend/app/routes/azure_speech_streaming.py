"""
Azure Speech Service API Routes with Streaming and SRE Integration

This module provides FastAPI routes for Azure Speech Service functionality,
implementing secure proxy endpoints with WebSocket streaming support and
SRE agent integration for intelligent audio conversations.
"""

from fastapi import (
    APIRouter, 
    HTTPException, 
    File, 
    UploadFile, 
    WebSocket, 
    WebSocketDisconnect,
    Query
)
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import base64
import logging
import json
import os
import tempfile

from app.services.azure_speech_service import AzureSpeechService
from app.agents.sre_agent import SREAgent

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/speech-streaming", tags=["Azure Speech Streaming"])

# Initialize service instances
speech_service = AzureSpeechService()
sre_agent = SREAgent()


# Pydantic models for streaming requests
class SREAudioRequest(BaseModel):
    """Request model for SRE audio interaction"""
    question: Optional[str] = Field(
        None, description="Optional text question to combine with audio"
    )
    voice_name: Optional[str] = Field(
        "en-US-AriaNeural", description="Voice for response audio"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the current system status?",
                "voice_name": "en-US-AriaNeural"
            }
        }


class StreamingMessage(BaseModel):
    """WebSocket message format for streaming audio"""
    type: str = Field(
        ..., description="Message type: 'audio', 'text', 'response', 'error'"
    )
    data: str = Field(
        ..., description="Base64 encoded audio data or text content"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata"
    )


# WebSocket endpoint for real-time audio streaming with SRE agent
@router.websocket("/stream")
async def websocket_audio_stream(websocket: WebSocket):
    """
    WebSocket endpoint for real-time audio streaming with SRE integration.
    
    Flow:
    1. Client sends audio data (base64 encoded)
    2. Server transcribes audio to text using Azure Speech Service
    3. Server sends transcribed text to SRE agent
    4. Server converts SRE response to speech
    5. Server streams response audio back to client
    """
    await websocket.accept()
    print("🔗 WebSocket connection established for audio streaming")
    
    try:
        while True:
            # Receive message from client
            message_data = await websocket.receive_text()
            
            try:
                message = json.loads(message_data)
                message_type = message.get("type")
                data = message.get("data")
                metadata = message.get("metadata", {})
                
                if message_type == "audio":
                    print("🎵 Received audio data for processing")
                    
                    # Decode audio data
                    try:
                        audio_bytes = base64.b64decode(data)
                        print(f"📦 Decoded audio: {len(audio_bytes)} bytes")
                        
                        # Validate audio format
                        if len(audio_bytes) < 44:  # Minimum WAV header size
                            raise ValueError("Audio data too small to be valid WAV")
                        
                        # Check for WAV header
                        if not audio_bytes.startswith(b'RIFF') or b'WAVE' not in audio_bytes[:12]:
                            print("⚠️ Audio doesn't appear to be WAV format, attempting to process anyway...")
                        
                        # Save audio to temporary file for processing
                        with tempfile.NamedTemporaryFile(
                            suffix=".wav", delete=False
                        ) as temp_file:
                            temp_file.write(audio_bytes)
                            temp_file_path = temp_file.name
                        
                        print(f"💾 Saved audio to temp file: {temp_file_path}")
                        
                        # Transcribe audio to text
                        print("🎧 Transcribing audio to text...")
                        transcription_result = speech_service.speech_to_text(
                            audio_file_path=temp_file_path
                        )
                        
                        # Clean up temp file
                        try:
                            os.unlink(temp_file_path)
                        except Exception:
                            pass
                        
                        if transcription_result.get("status") == "success":
                            transcribed_text = transcription_result.get(
                                "text", ""
                            )
                            
                            # Print prominent recognition result to terminal
                            print("\n" + "="*80)
                            print("🎯 WEBSOCKET SPEECH RECOGNITION COMPLETE!")
                            print("="*80)
                            print(f"🎧 RECOGNIZED SPEECH: '{transcribed_text}'")
                            print(f"📊 CONFIDENCE: {transcription_result.get('confidence', 'N/A')}")
                            print(f"📏 LENGTH: {len(transcribed_text)} characters")
                            print(f"🔄 SENDING TO SRE AGENT: {'YES' if transcribed_text.strip() else 'NO (empty text)'}")
                            print("="*80)
                            
                            # Send transcription back to client
                            transcription_response = {
                                "type": "transcription",
                                "data": transcribed_text,
                                "metadata": {
                                    "confidence": transcription_result.get(
                                        "confidence"
                                    )
                                }
                            }
                            print("📤 SENDING TRANSCRIPTION RESPONSE:")
                            print(f"   {json.dumps(transcription_response, indent=2)}")
                            await websocket.send_text(json.dumps(transcription_response))
                            
                            # Process with SRE agent if text is not empty
                            if transcribed_text.strip():
                                print("\n" + "="*80)
                                print("🤖 PROCESSING WITH SRE AGENT")
                                print("="*80)
                                print(f"📥 INPUT TEXT: '{transcribed_text}'")
                                print("🔄 Calling SRE agent...")
                                
                                sre_response = sre_agent.ask_question(
                                    transcribed_text
                                )
                                
                                # Extract response text with error handling
                                response_text = ""
                                try:
                                    if sre_response.get("langgraph", {}).get("response"):
                                        response_text = str(sre_response["langgraph"]["response"])
                                    elif sre_response.get("llama", {}).get("response"):
                                        response_text = str(sre_response["llama"]["response"])
                                    else:
                                        response_text = "I couldn't process your request at the moment."
                                except Exception as extract_error:
                                    print(f"❌ Error extracting SRE response: {extract_error}")
                                    response_text = "There was an error processing your request."
                                
                                print(f"✅ SRE AGENT RESPONSE GENERATED!")
                                print(f"📤 OUTPUT TEXT: '{response_text[:100]}{'...' if len(response_text) > 100 else ''}'")
                                print(f"📏 RESPONSE LENGTH: {len(response_text)} characters")
                                print("="*80)
                                
                                # Send text response
                                sre_response_msg = {
                                    "type": "sre_response",
                                    "data": response_text,
                                    "metadata": {
                                        "tools_data": sre_response.get(
                                            "tools_data"
                                        ),
                                        "enhanced_context": sre_response.get(
                                            "enhanced_context"
                                        )
                                    }
                                }
                                print("📤 SENDING SRE RESPONSE:")
                                print(f"   {json.dumps(sre_response_msg, indent=2)}")
                                await websocket.send_text(json.dumps(sre_response_msg))
                                
                                # Convert response to speech
                                voice_name = metadata.get(
                                    "voice_name", "en-US-AriaNeural"
                                )
                                print("🎤 Converting response to speech...")
                                tts_result = speech_service.text_to_speech(
                                    response_text, voice_name
                                )
                                
                                if tts_result.get("status") == "success":
                                    # Encode audio as base64 and send
                                    response_audio_b64 = base64.b64encode(
                                        tts_result["audio_data"]
                                    ).decode('utf-8')
                                    
                                    audio_response_msg = {
                                        "type": "response_audio",
                                        "data": response_audio_b64,
                                        "metadata": {
                                            "audio_length": tts_result[
                                                "audio_length"
                                            ],
                                            "voice_name": tts_result[
                                                "voice_name"
                                            ]
                                        }
                                    }
                                    print("📤 SENDING AUDIO RESPONSE:")
                                    print(f"   Type: {audio_response_msg['type']}")
                                    print(f"   Audio Length: {tts_result['audio_length']} bytes")
                                    print(f"   Voice: {tts_result['voice_name']}")
                                    await websocket.send_text(json.dumps(audio_response_msg))
                                    
                                    print(
                                        f"✅ Sent audio response "
                                        f"({tts_result['audio_length']} bytes)"
                                    )
                                else:
                                    await websocket.send_text(json.dumps({
                                        "type": "error",
                                        "data": (
                                            f"TTS Error: "
                                            f"{tts_result.get('error', 'Unknown')}"
                                        ),
                                        "metadata": {
                                            "error_code": tts_result.get(
                                                "error_code"
                                            )
                                        }
                                    }))
                            
                        else:
                            # Transcription failed
                            error_msg = transcription_result.get(
                                "error", "Transcription failed"
                            )
                            error_code = transcription_result.get("error_code", "transcription_failed")
                            
                            print(f"❌ Transcription failed: {error_msg}")
                            print(f"   Error code: {error_code}")
                            
                            # Provide specific guidance for common errors
                            if "INVALID_HEADER" in error_msg or "invalid" in error_msg.lower():
                                helpful_msg = "Audio format error. Please ensure audio is in WAV format (16kHz, 16-bit, mono recommended)"
                            elif "timeout" in error_msg.lower():
                                helpful_msg = "Audio recognition timeout. Try shorter audio clips or check audio quality"
                            elif "network" in error_msg.lower():
                                helpful_msg = "Network error. Please check your connection and try again"
                            else:
                                helpful_msg = "Please check audio format and quality, then try again"
                            
                            await websocket.send_text(json.dumps({
                                "type": "error",
                                "data": f"Transcription Error: {error_msg}. {helpful_msg}",
                                "metadata": {
                                    "error_code": error_code,
                                    "suggestion": helpful_msg,
                                    "supported_formats": ["WAV (16kHz, 16-bit, mono)", "WAV (8kHz, 16-bit, mono)"]
                                }
                            }))
                    
                    except Exception as audio_error:
                        error_msg = f"Audio processing error: {str(audio_error)}"
                        print(f"❌ {error_msg}")
                        await websocket.send_text(json.dumps({
                            "type": "error",
                            "data": error_msg,
                            "metadata": {
                                "error_code": "audio_processing_error"
                            }
                        }))
                
                elif message_type == "text":
                    # Direct text input for SRE agent
                    print("\n" + "="*80)
                    print("💬 TEXT INPUT RECEIVED!")
                    print("="*80)
                    print(f"📥 INPUT TEXT: '{data}'")
                    print(f"📏 LENGTH: {len(data)} characters")
                    print("🤖 SENDING TO SRE AGENT...")
                    print("="*80)
                    
                    sre_response = sre_agent.ask_question(data)
                    
                    # Extract response text
                    response_text = ""
                    if sre_response.get("langgraph", {}).get("response"):
                        response_text = sre_response["langgraph"]["response"]
                    elif sre_response.get("llama", {}).get("response"):
                        response_text = sre_response["llama"]["response"]
                    else:
                        response_text = (
                            "I couldn't process your request at the moment."
                        )
                    
                    print("\n" + "="*80)
                    print("✅ SRE AGENT RESPONSE FOR TEXT INPUT")
                    print("="*80)
                    print(f"📤 OUTPUT TEXT: '{response_text[:100]}{'...' if len(response_text) > 100 else ''}'")
                    print(f"📏 RESPONSE LENGTH: {len(response_text)} characters")
                    print("="*80)
                    
                    # Send text response
                    await websocket.send_text(json.dumps({
                        "type": "sre_response",
                        "data": response_text,
                        "metadata": {
                            "tools_data": sre_response.get("tools_data"),
                            "enhanced_context": sre_response.get(
                                "enhanced_context"
                            )
                        }
                    }))
                    
                    # Convert to speech if requested
                    if metadata.get("with_audio", False):
                        voice_name = metadata.get(
                            "voice_name", "en-US-AriaNeural"
                        )
                        tts_result = speech_service.text_to_speech(
                            response_text, voice_name
                        )
                        
                        if tts_result.get("status") == "success":
                            response_audio_b64 = base64.b64encode(
                                tts_result["audio_data"]
                            ).decode('utf-8')
                            
                            await websocket.send_text(json.dumps({
                                "type": "response_audio",
                                "data": response_audio_b64,
                                "metadata": {
                                    "audio_length": tts_result["audio_length"],
                                    "voice_name": tts_result["voice_name"]
                                }
                            }))
                
                else:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "data": f"Unknown message type: {message_type}",
                        "metadata": {"error_code": "unknown_message_type"}
                    }))
                    
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "data": "Invalid JSON format",
                    "metadata": {"error_code": "invalid_json"}
                }))
            
    except WebSocketDisconnect:
        print("🔌 WebSocket connection closed")
    except Exception as e:
        error_msg = f"WebSocket error: {str(e)}"
        print(f"❌ {error_msg}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "data": error_msg,
                "metadata": {"error_code": "websocket_error"}
            }))
        except Exception:
            pass


# REST endpoint for SRE audio interaction
@router.post("/sre-audio")
async def sre_audio_interaction(
    audio_file: UploadFile = File(...),
    question: Optional[str] = Query(None, description="Optional text question"),
    voice_name: Optional[str] = Query("en-US-AriaNeural", description="TTS voice")
) -> Dict[str, Any]:
    """
    Process audio input through SRE agent and return text and audio response.
    
    Flow:
    1. Transcribe uploaded audio to text
    2. Send transcribed text (+ optional question) to SRE agent
    3. Convert SRE response to speech
    4. Return both text and audio response
    """
    try:
        logger.info(
            f"Received SRE audio interaction request with file: "
            f"{audio_file.filename}"
        )
        
        # Read and save audio file
        audio_content = await audio_file.read()
        temp_file_path = f"/tmp/sre_audio_{audio_file.filename}"
        
        with open(temp_file_path, "wb") as f:
            f.write(audio_content)
        
        print(f"🎧 Transcribing audio file: {audio_file.filename}")
        
        # Transcribe audio
        transcription_result = speech_service.speech_to_text(
            audio_file_path=temp_file_path
        )
        
        # Clean up temp file
        try:
            os.remove(temp_file_path)
        except Exception:
            pass
        
        if transcription_result.get("status") != "success":
            print(f"❌ Transcription failed: {transcription_result.get('error')}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": (
                        f"Transcription failed: "
                        f"{transcription_result.get('error')}"
                    ),
                    "error_code": transcription_result.get("error_code")
                }
            )
        
        transcribed_text = transcription_result.get("text", "")
        print(f"✅ Transcribed text: {transcribed_text}")
        
        # Combine with optional question
        full_question = transcribed_text
        if question:
            full_question = f"{question} Context from audio: {transcribed_text}"
        
        # Process with SRE agent
        print(f"🤖 Processing with SRE agent: {full_question}")
        sre_response = sre_agent.ask_question(full_question)
        
        # Extract response text
        response_text = ""
        if sre_response.get("langgraph", {}).get("response"):
            response_text = sre_response["langgraph"]["response"]
        elif sre_response.get("llama", {}).get("response"):
            response_text = sre_response["llama"]["response"]
        else:
            response_text = "I couldn't process your request at the moment."
        
        print(f"💬 SRE response: {response_text[:100]}...")
        
        # Convert response to speech
        print(f"🎤 Converting response to speech with voice: {voice_name}")
        
        tts_result = speech_service.text_to_speech(response_text, voice_name)
        
        if tts_result.get("status") != "success":
            print(f"❌ TTS failed: {tts_result.get('error')}")
            # Return text response even if TTS fails
            return {
                "transcribed_text": transcribed_text,
                "sre_response": response_text,
                "sre_metadata": {
                    "tools_data": sre_response.get("tools_data"),
                    "enhanced_context": sre_response.get("enhanced_context")
                },
                "audio_response": None,
                "tts_error": tts_result.get("error"),
                "status": "partial_success"
            }
        
        # Encode audio response
        response_audio_b64 = base64.b64encode(
            tts_result["audio_data"]
        ).decode('utf-8')
        
        response = {
            "transcribed_text": transcribed_text,
            "transcription_confidence": transcription_result.get("confidence"),
            "sre_response": response_text,
            "sre_metadata": {
                "tools_data": sre_response.get("tools_data"),
                "enhanced_context": sre_response.get("enhanced_context")
            },
            "audio_response": {
                "audio_base64": response_audio_b64,
                "audio_length": tts_result["audio_length"],
                "voice_name": tts_result["voice_name"]
            },
            "status": "success"
        }
        
        print("✅ SRE audio interaction completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"SRE audio interaction error: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": error_msg,
                "error_code": "sre_audio_error"
            }
        )


# Utility endpoint to test streaming functionality
@router.get("/stream-test")
async def stream_test_info():
    """
    Information about how to use the streaming WebSocket endpoint.
    """
    return {
        "websocket_url": "/speech-streaming/stream",
        "supported_message_types": [
            {
                "type": "audio",
                "description": (
                    "Send base64 encoded audio data for transcription "
                    "and SRE processing"
                ),
                "example": {
                    "type": "audio",
                    "data": "UklGRiQEAABXQVZFZm10IBAAAAAB...",
                    "metadata": {
                        "voice_name": "en-US-AriaNeural"
                    }
                }
            },
            {
                "type": "text",
                "description": "Send text directly to SRE agent",
                "example": {
                    "type": "text",
                    "data": "What is the current system status?",
                    "metadata": {
                        "with_audio": True,
                        "voice_name": "en-US-AriaNeural"
                    }
                }
            }
        ],
        "response_types": [
            "transcription",
            "sre_response",
            "response_audio",
            "error"
        ],
        "usage_notes": [
            "Audio must be WAV format (RIFF header required)",
            "Recommended: 16kHz sample rate, 16-bit depth, mono channel",
            "Supported: 8kHz or 16kHz sample rates",
            "Audio should be base64 encoded for transmission",
            "Use voice_name metadata to specify TTS voice",
            "Set with_audio=True in text messages to get audio response",
            "WebSocket maintains connection for real-time interaction"
        ]
    }


# Health check endpoint for the integrated system
@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check for the integrated Speech + SRE system.
    """
    try:
        print("🏥 Performing integrated system health check")
        
        # Check speech service
        speech_health = speech_service.health_check()
        
        # Check SRE agent (simple test)
        try:
            sre_test = sre_agent.ask_question("health check")
            sre_healthy = not sre_test.get("error")
        except Exception:
            sre_healthy = False
        
        overall_status = "healthy" if (
            speech_health.get("status") == "healthy" and sre_healthy
        ) else "unhealthy"
        
        response = {
            "overall_status": overall_status,
            "components": {
                "azure_speech_service": speech_health,
                "sre_agent": {
                    "status": "healthy" if sre_healthy else "unhealthy",
                    "service": "SRE Agent"
                }
            },
            "streaming_available": True,
            "supported_features": [
                "text_to_speech",
                "speech_to_text",
                "voice_listing",
                "websocket_streaming",
                "sre_integration"
            ]
        }
        
        print(f"✅ Integrated system health: {overall_status}")
        return response
        
    except Exception as e:
        error_msg = f"Health check error: {str(e)}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")
        return {
            "overall_status": "unhealthy",
            "error": error_msg,
            "error_code": "health_check_failed"
        }
