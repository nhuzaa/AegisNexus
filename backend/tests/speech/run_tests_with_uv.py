#!/usr/bin/env python3
"""
Test runner using uv run for all speech-to-text tests
"""

import subprocess
import sys
import os

def run_test(test_name, test_file):
    """Run a single test using uv run and return the result"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}")
    print(f"{'='*60}")
    
    try:
        # Change to the backend directory to ensure proper imports
        backend_dir = os.path.join(os.path.dirname(__file__), '..', '..')
        
        result = subprocess.run(
            ["uv", "run", "python", test_file], 
            capture_output=True, 
            text=True, 
            timeout=60,
            cwd=backend_dir
        )
        
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ {test_name} completed successfully")
            return True
        else:
            print(f"❌ {test_name} failed with return code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running {test_name}: {str(e)}")
        return False

def check_server_status():
    """Check if the server is running"""
    try:
        result = subprocess.run(
            ["uv", "run", "python", "-c", 
             "import requests; print('ok' if requests.get('http://localhost:8001/speech-streaming/health', timeout=3).status_code == 200 else 'not_running')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "ok" in result.stdout
    except Exception:
        return False

def check_audio_file():
    """Check if test audio file exists"""
    audio_file_path = "./audio/simplequestion.wav"
    return os.path.exists(audio_file_path)

def main():
    """Main test runner function"""
    print("🧪 AegisNexus Speech-to-Text Test Suite (using uv run)")
    print("=" * 60)
    print("🎯 Testing both Direct API and WebSocket implementations")
    
    # Pre-flight checks
    print("\n🔍 Pre-flight Checks")
    print("-" * 30)
    
    # Check audio file
    if not check_audio_file():
        print("❌ Test audio file not found: ./audio/simplequestion.wav")
        print("💡 Please ensure the audio file exists for testing")
        return
    else:
        print("✅ Test audio file found")
    
    # Check server status for WebSocket tests
    server_running = check_server_status()
    if server_running:
        print("✅ Server is running (WebSocket tests available)")
    else:
        print("⚠️ Server is not running (WebSocket tests will be skipped)")
        print("💡 To run WebSocket tests, start the server:")
        print("   uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload")
    
    # Test files (relative to backend directory)
    tests = [
        ("Direct API Speech-to-Text", "tests/speech/test_direct_speech_to_text.py"),
    ]
    
    if server_running:
        tests.append(("WebSocket Speech-to-Text", "tests/speech/test_websocket_speech_to_text.py"))
        tests.append(("Method Comparison", "tests/speech/compare_methods.py"))
    
    # Run tests
    results = []
    for test_name, test_file in tests:
        success = run_test(test_name, test_file)
        results.append((test_name, success))
    
    # Final Summary
    print("\n" + "=" * 60)
    print("📊 Final Test Results")
    print("=" * 60)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<30} {status}")
    
    # Overall result
    all_passed = all(success for _, success in results)
    if all_passed:
        print("\n🎉 Overall Result: ALL TESTS PASSED")
    else:
        print("\n💥 Overall Result: SOME TESTS FAILED")
    
    print("\n💡 Tips:")
    print("   - For WebSocket tests: Start the server first using 'uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload'")
    print("   - For audio tests: Ensure ./audio/simplequestion.wav exists")
    print("   - Check Azure Speech Service configuration in .env.local")
    print("   - All tests use 'uv run' for consistent environment")

if __name__ == "__main__":
    main()
