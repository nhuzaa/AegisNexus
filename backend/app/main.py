from fastapi import FastAPI
from app.routes.sre import router as sre_router

app = FastAPI(
    title="AegisNexus SRE Agent API",
    description="AI-powered SRE agent with integrated monitoring tools",
    version="1.0.0"
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
