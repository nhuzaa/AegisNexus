from fastapi import FastAPI
from app.routes.sre import router as sre_router

app = FastAPI()

app.include_router(sre_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)