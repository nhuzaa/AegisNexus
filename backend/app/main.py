from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.sre import router as sre_router
from app.routes.azure_speech_streaming import (
    router as azure_speech_streaming_router
)

app = FastAPI(
    title="AegisNexus SRE Agent API with Azure Speech Streaming",
    description="AI-powered SRE agent with monitoring tools and Azure Speech",
    version="1.0.0"
)

# Add CORS middleware - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {
        "message": (
            "AegisNexus SRE Agent & Azure Speech Streaming API is running"
        ),
        "status": "healthy",
        "version": "1.0.0",
        "documentation": "/docs",
        "services": [
            "SRE Agent",
            "Azure Speech Service",
            "WebSocket Audio Streaming"
        ]
    }

app.include_router(sre_router)
app.include_router(azure_speech_streaming_router)
app.include_router(azure_speech_streaming_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
