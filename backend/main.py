"""
AegisNexus Backend Server
Simple script to start the FastAPI server with uvicorn
"""
import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Start the FastAPI server"""
    print("🚀 Starting AegisNexus Backend Server...")
    
    # Add the current directory to Python path to ensure imports work
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    try:
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["app"],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
