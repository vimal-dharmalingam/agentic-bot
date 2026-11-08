from app.core.models import Message
from app.providers.base import LLMProvider


class FakeLLMProvider(LLMProvider):
    """Free, offline provider for local dev and unit tests."""

    def generate(self, messages: list[Message], system_prompt: str | None = None) -> str:
        last_message = messages[-1].content if messages else ""
        return f"[fake] You said: {last_message}"