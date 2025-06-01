# Speech Testing Suite

This directory contains comprehensive tests for the AegisNexus speech-to-text functionality, covering both direct API calls and WebSocket streaming implementations.

## Test Files

### Core Test Files
- `test_direct_speech_to_text.py` - Tests direct Azure Speech Service API calls
- `test_websocket_speech_to_text.py` - Tests WebSocket streaming speech-to-text functionality
- `enhanced_speech_demo.py` - **NEW!** Interactive demo showcasing enhanced terminal output
- `run_all_tests.py` - Runs all speech tests with comprehensive reporting
- `run_tests_with_uv.py` - **NEW!** uv run compatible test runner
- `compare_methods.py` - Compares direct API vs WebSocket approaches

### Test Structure
```
tests/speech/
├── __init__.py                           # Module initialization
├── README.md                            # This documentation
├── quick_start.py                       # 🚀 Interactive quick start script
├── run_all_tests.py                     # Original test runner
├── run_tests_with_uv.py                 # 🆕 uv run compatible test runner
├── test_direct_speech_to_text.py        # Direct API tests
├── test_websocket_speech_to_text.py     # WebSocket streaming tests
├── enhanced_speech_demo.py              # 🆕 Interactive demo with enhanced output
└── compare_methods.py                   # Method comparison tests
```

## Prerequisites

### 1. Audio Test File
Ensure you have a test audio file at:
```
./audio/simplequestion.wav
```

### 2. Environment Configuration
Make sure your `.env.local` file contains the Azure Speech Service configuration:
```env
AZURE_SPEECH_KEY=your_speech_service_key
AZURE_SPEECH_REGION=your_region
```

### 3. Server Running (for WebSocket tests)
For WebSocket tests, the server must be running:
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Running Tests

### 🚀 Quick Start (Recommended)
```bash
# Interactive menu with guided setup
uv run python tests/speech/quick_start.py
```

### Run All Tests (Using uv run - Recommended)
```bash
# From the backend directory
uv run python tests/speech/run_tests_with_uv.py
```

### Run All Tests (Alternative)
```bash
# From the backend directory
uv run python tests/speech/run_all_tests.py
```

### Run Individual Tests

#### Direct API Tests Only
```bash
uv run python tests/speech/test_direct_speech_to_text.py
```

#### WebSocket Tests Only
```bash
uv run python tests/speech/test_websocket_speech_to_text.py
```

#### Enhanced Speech Demo (NEW!)
```bash
uv run python tests/speech/enhanced_speech_demo.py
```

This interactive demo showcases the enhanced terminal output features and demonstrates the complete speech-to-text → SRE agent → text-to-speech pipeline.

## Test Scenarios

### Direct API Tests (`test_direct_speech_to_text.py`)
1. **Health Check** - Verifies Azure Speech Service connectivity
2. **Speech-to-Text** - Tests audio file transcription using direct API

**Expected Output:**
```
🧪 Starting Direct API Speech-to-Text Tests
==================================================

📋 Test 1: Azure Speech Service Health Check
----------------------------------------
✅ Azure Speech Service is healthy!

📋 Test 2: Speech-to-text from audio file
----------------------------------------
✅ Speech-to-text succeeded!
📝 Transcribed Text: [Your audio transcription]
📊 Confidence: [Confidence score]
```

### WebSocket Tests (`test_websocket_speech_to_text.py`)
1. **Audio Upload & Transcription** - Tests end-to-end WebSocket audio processing
2. **Text-Only Mode** - Tests direct text input via WebSocket

**Expected Flow:**
1. Connect to WebSocket endpoint
2. Send base64-encoded audio data
3. Receive transcription response
4. Receive SRE agent response
5. Receive synthesized audio response

**Expected Output:**
```
🧪 Starting WebSocket Speech-to-Text Tests
==================================================

📋 Test 1: Speech-to-text from audio file
----------------------------------------
🔗 Connecting to WebSocket: ws://localhost:8001/speech-streaming/stream
✅ WebSocket connection established
📤 Sending audio data (XXXX bytes)...
📥 Waiting for responses...
📋 Received transcription response
✅ Transcribed Text: '[Your audio transcription]'
📊 Confidence: [Confidence score]
📋 Received sre_response response
🤖 SRE Response: [SRE agent response]
📋 Received response_audio response
🎵 Response Audio: XXXX bytes, Voice: en-US-AriaNeural
```

## Enhanced Terminal Output Features

### 🎯 What's New
The speech recognition system now features **enhanced terminal output** that provides clear visual feedback for all processing steps:

#### Speech Recognition Display
When speech is recognized, you'll see:
```
================================================================================
🎧 SPEECH RECOGNIZED!
================================================================================
📝 TRANSCRIBED TEXT: 'What is the current system status?'
📊 CONFIDENCE: 0.95
📏 LENGTH: 32 characters
✅ STATUS: success
================================================================================
```

#### SRE Agent Processing
When the recognized speech is sent to the SRE agent:
```
================================================================================
🤖 PROCESSING WITH SRE AGENT
================================================================================
📥 INPUT TEXT: 'What is the current system status?'
🔄 Calling SRE agent...
✅ SRE AGENT RESPONSE GENERATED!
📤 OUTPUT TEXT: 'The system is currently running normally...'
📏 RESPONSE LENGTH: 156 characters
================================================================================
```

#### WebSocket Text Input
For direct text input via WebSocket:
```
================================================================================
💬 TEXT INPUT RECEIVED!
================================================================================
📥 INPUT TEXT: 'Show me system health'
📏 LENGTH: 19 characters
🤖 SENDING TO SRE AGENT...
================================================================================
```

### 🎪 Interactive Demo
Use the enhanced demo to see these features in action:
```bash
# Terminal 1: Start the server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Run the interactive demo
uv run python tests/speech/enhanced_speech_demo.py
```

The demo will guide you through both speech and text input while showing the enhanced output in the server terminal.

## Complete Workflow

### 1. Speech Recognition → Agent Response → Audio Output
The enhanced system follows this workflow:

```
🎤 Audio Input → 🎧 Speech Recognition → 🤖 SRE Agent → 🎵 Audio Response
```

Each step is clearly displayed in the terminal with enhanced visual feedback:

1. **Audio Processing**: Convert speech to text with confidence scoring
2. **Agent Processing**: Send recognized text to SRE agent for intelligent response
3. **Response Generation**: Convert agent response back to speech
4. **Terminal Display**: All steps are prominently shown with visual separators

### 2. Text Input → Agent Response → Audio Output
For direct text input:

```
💬 Text Input → 🤖 SRE Agent → 🎵 Audio Response
```

### Key Features
- ✅ **Real-time processing** with WebSocket streaming
- ✅ **Enhanced terminal output** with clear visual feedback
- ✅ **Automatic agent integration** - every recognition triggers agent response
- ✅ **Dual input modes** - speech or text
- ✅ **Comprehensive error handling** with detailed error messages
- ✅ **uv run compatibility** for consistent environment management

## Test Results

### Success Indicators
- ✅ Connection established (WebSocket tests)
- ✅ Audio successfully transcribed
- ✅ Confidence scores provided
- ✅ SRE responses received (WebSocket tests)
- ✅ Response audio generated (WebSocket tests)

### Common Issues & Solutions

#### Server Not Running
```
❌ Server is not running on localhost:8001
💡 Please start the server first:
   uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### Audio File Missing
```
❌ Test audio file not found: ./audio/simplequestion.wav
💡 Please ensure the audio file exists for testing
```

#### Azure Configuration Issues
```
❌ Azure Speech Service health check failed!
💡 Check your .env.local file for correct AZURE_SPEECH_KEY and AZURE_SPEECH_REGION
```

## Audio File Requirements

The test audio file should meet these specifications:
- **Format**: WAV (RIFF format)
- **Sample Rate**: 16kHz (recommended) or 8kHz
- **Bit Depth**: 16-bit
- **Channels**: Mono (single channel)
- **Duration**: 1-30 seconds (for testing)

## Integration with Main Test Suite

These speech tests can be integrated with the main project test suite:

```bash
# Run from backend directory
python -m pytest tests/speech/ -v
```

## Monitoring & Debugging

### Verbose Output
All tests provide detailed console output including:
- Connection status
- Request/response data sizes
- Transcription confidence scores
- Error messages with suggested solutions
- Performance timing information

### Log Files
Check application logs for additional debugging information:
- WebSocket connection logs
- Azure Speech Service API logs
- SRE agent processing logs

## Future Enhancements

- [ ] Add performance benchmarking
- [ ] Add stress testing for concurrent connections
- [ ] Add audio quality validation
- [ ] Add different audio format testing
- [ ] Add multi-language support testing
- [ ] Add error injection testing
