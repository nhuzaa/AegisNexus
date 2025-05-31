import pytest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from app.main import app
from app.agents.sre_agent import SREAgent

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def sre_agent():
    """Fixture for SRE agent"""
    return SREAgent()

def test_sre_agent_ask_question(client, monkeypatch):
    # Mock the SREAgent's ask_question method
    def mock_ask_question(question: str):
        return {
            "langgraph": {"response": "This is a mock langgraph response."},
            "llama": {"response": "This is a mock llama response."},
            "tools_data": {"prometheus_cpu": {"status": "success"}},
            "enhanced_context": True
        }

    monkeypatch.setattr(SREAgent, "ask_question", mock_ask_question)

    response = client.post("/sre/ask", json={"question": "What is SRE?"})
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    assert "langgraph" in result["response"]
    assert "llama" in result["response"]
    assert "tools_data" in result["response"]

def test_sre_agent_invalid_question(client):
    response = client.post("/sre/ask", json={"question": ""})
    assert response.status_code == 422  # Unprocessable Entity for invalid input
    assert "detail" in response.json()  # Check for validation error details

@patch('app.services.llm_service.send_to_langgraph')
@patch('app.services.llm_service.send_to_llama_api')
def test_sre_agent_with_tools_integration(mock_llama, mock_langgraph, sre_agent):
    """Test SRE agent with tools integration"""
    mock_langgraph.return_value = {"response": "Langgraph response"}
    mock_llama.return_value = {"response": "Llama response"}
    
    # Test CPU metrics question
    result = sre_agent.ask_question("What's the current CPU usage?")
    
    assert "langgraph" in result
    assert "llama" in result
    assert "tools_data" in result
    assert "enhanced_context" in result
    assert result["enhanced_context"] is True
    assert "prometheus_cpu" in result["tools_data"]

@patch('app.services.llm_service.send_to_langgraph')
def test_incident_response_endpoint(client, monkeypatch):
    """Test incident response endpoint"""
    def mock_execute_incident_response(alert_name: str, severity: str):
        return {
            "incident_response": {"alerts": [], "metrics": {}},
            "ai_analysis": {"analysis": "Test analysis"},
            "status": "completed"
        }
    
    monkeypatch.setattr(SREAgent, "execute_incident_response", mock_execute_incident_response)
    
    response = client.post("/sre/incident-response", json={
        "alert_name": "HighCPU",
        "severity": "critical"
    })
    
    assert response.status_code == 200
    result = response.json()
    assert result["response"]["status"] == "completed"

def test_health_endpoint(client, monkeypatch):
    """Test health endpoint"""
    def mock_get_system_health():
        return {
            "health_data": {"tools_health": {"prometheus": "healthy"}},
            "ai_assessment": {"assessment": "System healthy"},
            "timestamp": "2024-01-01T00:00:00Z"
        }
    
    monkeypatch.setattr(SREAgent, "get_system_health", mock_get_system_health)
    
    response = client.get("/sre/health")
    assert response.status_code == 200
    result = response.json()
    assert "health_data" in result["response"]

def test_tools_health_endpoint(client):
    """Test tools health endpoint"""
    response = client.get("/sre/tools/health")
    assert response.status_code == 200
    result = response.json()
    assert "tools_health" in result
    # Should have all 8 tools
    expected_tools = [
        "prometheus", "grafana", "loki", "alertmanager",
        "github", "slack", "teams", "opentelemetry"
    ]
    for tool in expected_tools:
        assert tool in result["tools_health"]
        assert result["tools_health"][tool] == "healthy"

def test_tools_demo_endpoint(client):
    """Test tools demo endpoint"""
    response = client.get("/sre/tools/demo")
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "successfully" in result["message"]