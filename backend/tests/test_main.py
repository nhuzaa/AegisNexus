import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_sre_ask_route(client):
    response = client.post("/sre/ask", json={"question": "What is SRE?"})
    assert response.status_code == 200
    assert "response" in response.json()  # Adjust based on actual response structure
    assert isinstance(response.json()["response"], str)  # Ensure the response is a string