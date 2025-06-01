#!/usr/bin/env python3
"""
Quick WebSocket Connection Test

Simple script to quickly check if the WebSocket is accessible.
"""

import asyncio
import websockets
import requests
import sys


async def quick_websocket_test():
    """Quick test to check WebSocket connectivity."""
    print("🔍 Quick WebSocket Test")
    print("-" * 30)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        print(f"✅ Server status: {response.status_code}")
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return False
    
    # Test WebSocket connection
    try:
        async with websockets.connect("ws://localhost:8000/speech-streaming/stream") as websocket:
            print("✅ WebSocket connection: SUCCESS")
            return True
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"❌ WebSocket connection failed: HTTP {e.status_code}")
        return False
    except websockets.InvalidStatusCode as e:
        print(f"❌ WebSocket connection failed: HTTP {e.status_code}")
        return False
    except Exception as e:
        print(f"❌ WebSocket connection failed: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(quick_websocket_test())
    if not result:
        print("\n💡 Tips:")
        print("1. Make sure the server is running:")
        print("   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("2. Check that the route is registered in app/main.py")
        print("3. Verify there are no import errors")
        sys.exit(1)
    else:
        print("\n🎉 WebSocket is working correctly!")
