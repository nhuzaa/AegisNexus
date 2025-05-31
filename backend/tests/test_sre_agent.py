import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agents.sre_agent import SREAgent

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_sre_agent_ask_question(client, monkeypatch):
    # Mock the SREAgent's ask_question method
    async def mock_ask_question(question: str):
        return {"response": "This is a mock response."}

    monkeypatch.setattr(SREAgent, "ask_question", mock_ask_question)

    response = client.post("/sre/ask", json={"question": "What is SRE?"})
    assert response.status_code == 200
    assert response.json() == {"response": "This is a mock response."}

def test_sre_agent_invalid_question(client):
    response = client.post("/sre/ask", json={"question": ""})
    assert response.status_code == 422  # Unprocessable Entity for invalid input
    assert "detail" in response.json()  # Check for validation error details