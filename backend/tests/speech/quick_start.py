#!/usr/bin/env python3
"""
Quick Start Script for Enhanced Speech Recognition

This script provides a simple way to test the enhanced speech recognition
system using uv run. It automatically checks prerequisites and guides
the user through the testing process.
"""

import subprocess
import sys
import os
import time

def run_command(command, description, check_output=False):
    """Run a command and return the result"""
    print(f"\n🔄 {description}")
    print(f"💻 Command: {command}")
    
    try:
        if check_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(command, shell=True, timeout=30)
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False, "", "Timeout"
    except Exception as e:
        print(f"❌ Error running command: {str(e)}")
        return False, "", str(e)

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking Prerequisites")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Not in the correct directory. Please run from the backend folder.")
        return False
    print("✅ Correct directory confirmed")
    
    # Check if uv is installed
    success, stdout, stderr = run_command("uv --version", "Checking uv installation", check_output=True)
    if not success:
        print("❌ uv is not installed. Please install uv first.")
        print("💡 Install with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    print(f"✅ uv is installed: {stdout.strip()}")
    
    # Check if audio file exists
    if not os.path.exists("audio/simplequestion.wav"):
        print("❌ Test audio file not found: audio/simplequestion.wav")
        print("💡 Please ensure the audio file exists for testing")
        return False
    print("✅ Test audio file found")
    
    return True

def start_server():
    """Start the server using uv run"""
    print("\n🚀 Starting Server")
    print("=" * 50)
    print("💡 This will start the server with enhanced terminal output")
    print("👀 Watch for enhanced speech recognition output in this terminal!")
    print("\n🔄 Starting server with uv run...")
    
    # Start the server
    command = "uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"
    print(f"💻 Command: {command}")
    print("\n📋 Server will show enhanced output for:")
    print("   • Speech recognition results")
    print("   • SRE agent processing")
    print("   • Response generation")
    print("\n🛑 Press Ctrl+C to stop the server when done testing")
    print("=" * 50)
    
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")

def run_tests():
    """Run tests using uv run"""
    print("\n🧪 Running Tests with uv run")
    print("=" * 50)
    
    tests = [
        ("Direct API Test", "uv run python tests/speech/test_direct_speech_to_text.py"),
        ("Enhanced Demo", "uv run python tests/speech/enhanced_speech_demo.py"),
        ("All Tests", "uv run python tests/speech/run_tests_with_uv.py")
    ]
    
    for test_name, command in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        success, stdout, stderr = run_command(command, f"Running {test_name}")
        
        if success:
            print(f"✅ {test_name} completed successfully")
        else:
            print(f"❌ {test_name} failed")
            if stderr:
                print(f"Error: {stderr}")

def show_menu():
    """Show the main menu"""
    print("\n🎤 Enhanced Speech Recognition Quick Start")
    print("=" * 50)
    print("What would you like to do?")
    print("1. 🚀 Start Server (with enhanced terminal output)")
    print("2. 🧪 Run Tests (requires server to be running separately)")
    print("3. 🔍 Check Prerequisites Only")
    print("4. 📖 Show Usage Examples")
    print("5. 🚪 Exit")
    print("=" * 50)

def show_usage_examples():
    """Show usage examples"""
    print("\n📖 Usage Examples")
    print("=" * 50)
    
    examples = [
        ("Start server with enhanced output", "uv run uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload"),
        ("Run direct API test", "uv run python tests/speech/test_direct_speech_to_text.py"),
        ("Run WebSocket test", "uv run python tests/speech/test_websocket_speech_to_text.py"),
        ("Run enhanced demo", "uv run python tests/speech/enhanced_speech_demo.py"),
        ("Run all tests", "uv run python tests/speech/run_tests_with_uv.py"),
        ("Compare methods", "uv run python tests/speech/compare_methods.py")
    ]
    
    for description, command in examples:
        print(f"\n📌 {description}:")
        print(f"   {command}")
    
    print("\n💡 Tips:")
    print("   • Always use 'uv run' for consistent environment")
    print("   • Start server first for WebSocket tests")
    print("   • Watch server terminal for enhanced output")
    print("   • Keep both client and server terminals visible")

def main():
    """Main function"""
    print("🎤 Enhanced Speech Recognition Quick Start")
    print("=" * 70)
    print("🎯 This script helps you get started with the enhanced speech system")
    print("✨ Features: Enhanced terminal output, SRE agent integration, uv run support")
    print("=" * 70)
    
    while True:
        show_menu()
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                if check_prerequisites():
                    start_server()
                else:
                    print("❌ Prerequisites not met. Please resolve issues first.")
            
            elif choice == "2":
                if check_prerequisites():
                    print("\n⚠️ Make sure the server is running in another terminal!")
                    input("Press Enter when ready to run tests...")
                    run_tests()
                else:
                    print("❌ Prerequisites not met. Please resolve issues first.")
            
            elif choice == "3":
                check_prerequisites()
            
            elif choice == "4":
                show_usage_examples()
            
            elif choice == "5":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
