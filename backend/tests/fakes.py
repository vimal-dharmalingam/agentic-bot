from app.core.exceptions import LLMProviderError
from app.core.models import Message
from app.providers.base import LLMProvider


class RecordingLLMProvider(LLMProvider):
    """Remembers what it was sent, so tests can inspect it."""

    def __init__(self, reply: str = "ok"):
        self.reply = reply
        self.calls: list[list[Message]] = []

    def generate(self, messages: list[Message], system_prompt: str | None = None) -> str:
        self.calls.append(list(messages))
        return self.reply


class FailingLLMProvider(LLMProvider):
    """Always fails, to test error handling."""

    def generate(self, messages: list[Message], system_prompt: str | None = None) -> str:
        raise LLMProviderError("simulated failure")