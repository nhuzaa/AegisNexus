from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.sre import router as sre_router

app = FastAPI(
    title="AegisNexus SRE Agent API",
    description="AI-powered SRE agent with integrated monitoring tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default port
        "http://localhost:8080",  # Vue default port
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint for API health check"""
    return {
        "message": "AegisNexus SRE Agent API is running",
        "status": "healthy",
        "version": "1.0.0",
        "documentation": "/docs"
    }

app.include_router(sre_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
