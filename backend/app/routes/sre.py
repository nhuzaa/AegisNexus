from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agents.sre_agent import SREAgent
from app.models.request_models import SRERequest

router = APIRouter()
sre_agent = SREAgent()

class IncidentRequest(BaseModel):
    alert_name: str
    severity: str

@router.post("/sre/ask")
async def ask_sre_question(request: SRERequest):
    try:
        response = sre_agent.ask_question(request.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sre/incident-response")
async def trigger_incident_response(request: IncidentRequest):
    """Trigger a complete incident response workflow"""
    try:
        response = sre_agent.execute_incident_response(request.alert_name, request.severity)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sre/health")
async def get_system_health():
    """Get comprehensive system health report"""
    try:
        response = sre_agent.get_system_health()
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sre/tools/demo")
async def demo_sre_tools():
    """Demonstrate SRE tools functionality"""
    try:
        from app.tools.sre_tools import demo_sre_tools
        # In a real scenario, you'd capture the output, but for demo purposes:
        demo_sre_tools()
        return {"message": "SRE tools demo executed successfully. Check console output."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sre/tools/health")
async def check_tools_health():
    """Check the health status of all SRE tools"""
    try:
        health_status = sre_agent.tools.health_check()
        return {"tools_health": health_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))