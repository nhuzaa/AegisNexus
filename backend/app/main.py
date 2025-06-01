from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.sre import router as sre_router

app = FastAPI(
    title="AegisNexus SRE Agent API",
    description="AI-powered SRE agent with monitoring tools",
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
            "AegisNexus SRE Agent API is running"
        ),
        "status": "healthy",
        "version": "1.0.0",
        "documentation": "/docs",
        "services": [
            "SRE Agent"
        ]
    }

app.include_router(sre_router)
