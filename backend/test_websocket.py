#!/usr/bin/env python3
"""
WebSocket Connection Test for Azure Speech Streaming

This script tests the WebSocket connection and basic functionality
of the speech streaming service.
"""

import asyncio
import websockets
import json
import requests
import time
import sys
from typing import Dict, Any


class WebSocketTester:
    def __init__(self, base_url: str = "localhost:8001"):
        self.base_url = base_url
        self.http_url = f"http://{base_url}"
        self.ws_url = f"ws://{base_url}"
        
    async def test_server_health(self) -> bool:
        """Test if the server is running and healthy."""
        print("🏥 Testing server health...")
        
        try:
            # Test speech streaming health endpoint (main one)
            response = requests.get(f"{self.http_url}/speech-streaming/health", timeout=5)
            if response.status_code == 200:
                print("✅ Speech streaming health check passed")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Speech streaming health check failed: {response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Server is not running or not accessible")
            return False
        except requests.exceptions.Timeout:
            print("❌ Server health check timed out")
            return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    async def test_websocket_connection(self) -> bool:
        """Test basic WebSocket connection."""
        print("\n🔗 Testing WebSocket connection...")
        
        ws_endpoint = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(ws_endpoint, timeout=10) as websocket:
                print("✅ WebSocket connection established successfully")
                print(f"   Connected to: {ws_endpoint}")
                return True
                
        except websockets.exceptions.InvalidStatusCode as e:
            print(f"❌ WebSocket connection failed with status: {e.status_code}")
            if e.status_code == 404:
                print("   This usually means the route is not registered or server is not running")
            return False
        except websockets.exceptions.ConnectionClosed:
            print("❌ WebSocket connection was closed unexpectedly")
            return False
        except Exception as e:
            print(f"❌ WebSocket connection error: {e}")
            return False
    
    async def test_websocket_text_message(self) -> bool:
        """Test sending a text message through WebSocket."""
        print("\n💬 Testing WebSocket text messaging...")
        
        ws_endpoint = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(ws_endpoint, timeout=10) as websocket:
                # Send a test text message
                test_message = {
                    "type": "text",
                    "data": "Hello, this is a test message",
                    "metadata": {"with_audio": False}
                }
                
                print(f"📤 Sending test message: {test_message}")
                await websocket.send(json.dumps(test_message))
                
                # Wait for response with timeout
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15)
                    response_data = json.loads(response)
                    print(f"📥 Received response: {response_data}")
                    
                    if response_data.get("type") == "sre_response":
                        print("✅ WebSocket text messaging test passed")
                        return True
                    else:
                        print(f"❌ Unexpected response type: {response_data.get('type')}")
                        return False
                        
                except asyncio.TimeoutError:
                    print("❌ WebSocket response timed out")
                    return False
                    
        except Exception as e:
            print(f"❌ WebSocket text messaging error: {e}")
            return False
    
    async def test_websocket_error_handling(self) -> bool:
        """Test WebSocket error handling with invalid messages."""
        print("\n⚠️  Testing WebSocket error handling...")
        
        ws_endpoint = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(ws_endpoint, timeout=10) as websocket:
                # Send invalid JSON
                print("📤 Sending invalid JSON...")
                await websocket.send("invalid json")
                
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                response_data = json.loads(response)
                
                if (response_data.get("type") == "error" and 
                    "invalid_json" in response_data.get("metadata", {}).get("error_code", "")):
                    print("✅ WebSocket error handling test passed")
                    print(f"   Error response: {response_data}")
                    return True
                else:
                    print(f"❌ Unexpected error response: {response_data}")
                    return False
                    
        except Exception as e:
            print(f"❌ WebSocket error handling test failed: {e}")
            return False
    
    async def test_stream_info_endpoint(self) -> bool:
        """Test the stream info endpoint."""
        print("\n📋 Testing stream info endpoint...")
        
        try:
            response = requests.get(f"{self.http_url}/speech-streaming/stream-test", timeout=5)
            if response.status_code == 200:
                info = response.json()
                print("✅ Stream info endpoint test passed")
                print(f"   WebSocket URL: {info.get('websocket_url')}")
                print(f"   Supported message types: {len(info.get('supported_message_types', []))}")
                return True
            else:
                print(f"❌ Stream info endpoint failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Stream info endpoint error: {e}")
            return False
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all WebSocket tests."""
        print("🚀 Starting WebSocket tests...\n")
        
        results = {}
        
        # Test server health first
        results["server_health"] = await self.test_server_health()
        
        if not results["server_health"]:
            print("\n❌ Server is not healthy. Skipping WebSocket tests.")
            return results
        
        # Test WebSocket connection
        results["websocket_connection"] = await self.test_websocket_connection()
        
        if not results["websocket_connection"]:
            print("\n❌ WebSocket connection failed. Skipping message tests.")
            return results
        
        # Test WebSocket messaging
        results["websocket_messaging"] = await self.test_websocket_text_message()
        
        # Test error handling
        results["error_handling"] = await self.test_websocket_error_handling()
        
        # Test stream info endpoint
        results["stream_info"] = await self.test_stream_info_endpoint()
        
        return results
    
    def print_test_summary(self, results: Dict[str, bool]) -> None:
        """Print a summary of test results."""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
        
        print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All tests passed! WebSocket service is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")


async def main():
    """Main test function."""
    print("WebSocket Service Test Suite")
    print("="*50)
    
    # Parse command line arguments for custom URL
    base_url = "localhost:8001"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Testing server at: {base_url}")
    
    tester = WebSocketTester(base_url)
    results = await tester.run_all_tests()
    tester.print_test_summary(results)
    
    # Exit with error code if any tests failed
    if not all(results.values()):
        sys.exit(1)


def check_server_startup():
    """Check if the server needs to be started."""
    print("🔍 Checking if server is running...")
    
    try:
        response = requests.get("http://localhost:8001/speech-streaming/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is already running")
            return True
    except Exception:
        pass
    
    print("❌ Server is not running")
    print("\n🚀 To start the server, run:")
    print("   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001")
    print("\nOr if you want to test against a different server:")
    print("   python test_websocket.py <host:port>")
    return False


if __name__ == "__main__":
    # Check if server is running first
    if not check_server_startup():
        print("\n⏳ Waiting for server to start (you can start it in another terminal)...")
        print("Press Ctrl+C to cancel\n")
        
        # Wait for server to start (with timeout)
        start_time = time.time()
        timeout = 30  # 30 seconds timeout
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(
                    "http://localhost:8001/speech-streaming/health", 
                    timeout=1
                )
                if response.status_code == 200:
                    print("✅ Server detected! Starting tests...\n")
                    break
            except Exception:
                pass
            time.sleep(1)
        else:
            print("❌ Timeout waiting for server to start")
            sys.exit(1)
    
    # Run the tests
    asyncio.run(main())
