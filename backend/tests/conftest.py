import pytest

from app.providers.fake_provider import FakeLLMProvider
from app.repositories.in_memory_repository import InMemorySessionRepository
from app.services.chat_service import ChatService


@pytest.fixture(autouse=True)
def aws_test_env(monkeypatch):
    """Runs before EVERY test: fake credentials so nothing can hit real AWS."""
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture
def repository():
    return InMemorySessionRepository()


@pytest.fixture
def chat_service(repository):
    return ChatService(llm=FakeLLMProvider(), repository=repository, max_history=10)