from fastapi import APIRouter, HTTPException
from app.agents.sre_agent import SREAgent
from app.models.request_models import SRERequest

router = APIRouter()
sre_agent = SREAgent()

@router.post("/sre/ask")
async def ask_sre_question(request: SRERequest):
    try:
        response = sre_agent.ask_question(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))