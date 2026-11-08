import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_chat_service
from app.main import app
from app.providers.fake_provider import FakeLLMProvider
from app.repositories.in_memory_repository import InMemorySessionRepository
from app.services.chat_service import ChatService
from tests.fakes import FailingLLMProvider


def _client_with(service: ChatService) -> TestClient:
    app.dependency_overrides[get_chat_service] = lambda: service
    return TestClient(app)


@pytest.fixture
def client():
    yield _client_with(ChatService(FakeLLMProvider(), InMemorySessionRepository()))
    app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_reply_and_session_id(client):
    response = client.post("/api/chat", json={"message": "hello"})

    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "[fake] You said: hello"
    assert body["session_id"]


def test_history_round_trip(client):
    session_id = client.post("/api/chat", json={"message": "hello"}).json()["session_id"]

    response = client.get(f"/api/sessions/{session_id}/messages")

    assert [m["role"] for m in response.json()["messages"]] == ["user", "assistant"]


@pytest.mark.parametrize("payload", [{}, {"message": ""}, {"message": 123}])
def test_invalid_input_returns_422(client, payload):
    assert client.post("/api/chat", json=payload).status_code == 422


def test_llm_failure_returns_502():
    client = _client_with(ChatService(FailingLLMProvider(), InMemorySessionRepository()))
    try:
        response = client.post("/api/chat", json={"message": "hi"})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json() == {"detail": "AI service unavailable"}