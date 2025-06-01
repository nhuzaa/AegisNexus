#!/usr/bin/env python3
"""
Comprehensive WebSocket Test Suite
Tests WebSocket functionality including message handling and error cases.
"""

import asyncio
import websockets
import json
import requests
import sys
import time
from typing import Dict, Any, List


class WebSocketTester:
    """Comprehensive WebSocket testing class."""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://")
        self.test_results: List[Dict[str, Any]] = []
    
    def log_result(self, test_name: str, status: str, message: str, details: Dict = None):
        """Log test result."""
        self.test_results.append({
            "test": test_name,
            "status": status,
            "message": message,
            "details": details or {},
            "timestamp": time.time()
        })
        
        status_icon = "✅" if status == "pass" else "❌" if status == "fail" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
    
    async def test_server_health(self) -> bool:
        """Test if the server is running and healthy."""
        endpoints = [
            "/health",
            "/speech-streaming/health",
            "/speech-streaming/stream-test"
        ]
        
        server_healthy = False
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                if response.status_code == 200:
                    self.log_result(
                        f"HTTP {endpoint}",
                        "pass",
                        f"Status: {response.status_code}",
                        {"status_code": response.status_code, "response_size": len(response.content)}
                    )
                    server_healthy = True
                else:
                    self.log_result(
                        f"HTTP {endpoint}",
                        "warn",
                        f"Status: {response.status_code}",
                        {"status_code": response.status_code}
                    )
            except Exception as e:
                self.log_result(
                    f"HTTP {endpoint}",
                    "fail",
                    f"Error: {str(e)}",
                    {"error": str(e)}
                )
        
        return server_healthy
    
    async def test_websocket_connection(self) -> bool:
        """Test basic WebSocket connection."""
        uri = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(uri, timeout=10) as websocket:
                self.log_result(
                    "WebSocket Connection",
                    "pass",
                    "Successfully connected",
                    {"uri": uri}
                )
                return True
                
        except websockets.exceptions.InvalidStatusCode as e:
            self.log_result(
                "WebSocket Connection",
                "fail",
                f"HTTP {e.status_code}",
                {"status_code": e.status_code, "uri": uri}
            )
            return False
        except Exception as e:
            self.log_result(
                "WebSocket Connection",
                "fail",
                str(e),
                {"error": str(e), "uri": uri}
            )
            return False
    
    async def test_text_message(self) -> bool:
        """Test sending text message to WebSocket."""
        uri = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(uri, timeout=10) as websocket:
                # Send text message
                test_message = {
                    "type": "text",
                    "data": "test message",
                    "metadata": {"with_audio": False}
                }
                
                await websocket.send(json.dumps(test_message))
                
                # Wait for response
                response = await asyncio.wait_for(websocket.recv(), timeout=15)
                response_data = json.loads(response)
                
                if response_data.get("type") == "sre_response":
                    self.log_result(
                        "Text Message Test",
                        "pass",
                        "Received SRE response",
                        {
                            "sent": test_message,
                            "received_type": response_data.get("type"),
                            "response_length": len(response_data.get("data", ""))
                        }
                    )
                    return True
                else:
                    self.log_result(
                        "Text Message Test",
                        "warn",
                        f"Unexpected response type: {response_data.get('type')}",
                        {"response": response_data}
                    )
                    return False
                    
        except asyncio.TimeoutError:
            self.log_result(
                "Text Message Test",
                "fail",
                "Response timeout",
                {"timeout": 15}
            )
            return False
        except Exception as e:
            self.log_result(
                "Text Message Test",
                "fail",
                str(e),
                {"error": str(e)}
            )
            return False
    
    async def test_invalid_message(self) -> bool:
        """Test sending invalid message format."""
        uri = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(uri, timeout=10) as websocket:
                # Send invalid JSON
                await websocket.send("invalid json")
                
                # Wait for error response
                response = await asyncio.wait_for(websocket.recv(), timeout=10)
                response_data = json.loads(response)
                
                if response_data.get("type") == "error":
                    self.log_result(
                        "Invalid Message Test",
                        "pass",
                        "Error handling works correctly",
                        {"error_type": response_data.get("metadata", {}).get("error_code")}
                    )
                    return True
                else:
                    self.log_result(
                        "Invalid Message Test",
                        "fail",
                        "Did not receive error response",
                        {"response": response_data}
                    )
                    return False
                    
        except Exception as e:
            self.log_result(
                "Invalid Message Test",
                "fail",
                str(e),
                {"error": str(e)}
            )
            return False
    
    async def test_unknown_message_type(self) -> bool:
        """Test sending unknown message type."""
        uri = f"{self.ws_url}/speech-streaming/stream"
        
        try:
            async with websockets.connect(uri, timeout=10) as websocket:
                # Send unknown message type
                test_message = {
                    "type": "unknown_type",
                    "data": "test",
                    "metadata": {}
                }
                
                await websocket.send(json.dumps(test_message))
                
                # Wait for error response
                response = await asyncio.wait_for(websocket.recv(), timeout=10)
                response_data = json.loads(response)
                
                if response_data.get("type") == "error":
                    self.log_result(
                        "Unknown Message Type Test",
                        "pass",
                        "Error handling for unknown types works",
                        {"error_code": response_data.get("metadata", {}).get("error_code")}
                    )
                    return True
                else:
                    self.log_result(
                        "Unknown Message Type Test",
                        "fail",
                        "Did not receive error for unknown type",
                        {"response": response_data}
                    )
                    return False
                    
        except Exception as e:
            self.log_result(
                "Unknown Message Type Test",
                "fail",
                str(e),
                {"error": str(e)}
            )
            return False
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all WebSocket tests."""
        print("🚀 Starting Comprehensive WebSocket Tests")
        print("=" * 60)
        
        # Test server health
        print("\n📡 Testing Server Health...")
        server_healthy = await self.test_server_health()
        
        if not server_healthy:
            print("\n❌ Server is not healthy - stopping tests")
            return self.get_summary()
        
        # Test WebSocket functionality
        print("\n🔌 Testing WebSocket Functionality...")
        
        # Basic connection test
        connection_ok = await self.test_websocket_connection()
        
        if connection_ok:
            # Message handling tests
            await self.test_text_message()
            await self.test_invalid_message()
            await self.test_unknown_message_type()
        
        return self.get_summary()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary."""
        total_tests = len(self.test_results)
        passed = len([r for r in self.test_results if r["status"] == "pass"])
        failed = len([r for r in self.test_results if r["status"] == "fail"])
        warnings = len([r for r in self.test_results if r["status"] == "warn"])
        
        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "success_rate": (passed / total_tests * 100) if total_tests > 0 else 0,
            "results": self.test_results
        }
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        print(f"\n📈 Results:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   ✅ Passed: {summary['passed']}")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   ⚠️  Warnings: {summary['warnings']}")
        print(f"   📊 Success Rate: {summary['success_rate']:.1f}%")
        
        if summary['failed'] > 0:
            print(f"\n❌ Failed Tests:")
            for result in summary['results']:
                if result['status'] == 'fail':
                    print(f"   • {result['test']}: {result['message']}")
        
        if summary['success_rate'] >= 80:
            print(f"\n🎉 WebSocket tests mostly successful!")
        elif summary['success_rate'] >= 50:
            print(f"\n⚠️ WebSocket has some issues but basic functionality works")
        else:
            print(f"\n❌ WebSocket tests failed")
            print(f"\n💡 Troubleshooting:")
            print(f"   1. Start the server: uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            print(f"   2. Check server logs for errors")
            print(f"   3. Verify imports and route registration")


async def main():
    """Main test runner."""
    tester = WebSocketTester()
    summary = await tester.run_all_tests()
    tester.print_summary(summary)
    
    # Exit with appropriate code
    success = summary['success_rate'] >= 80
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
