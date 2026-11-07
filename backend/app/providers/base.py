from abc import ABC, abstractmethod

from app.core.models import Message


class LLMProvider(ABC):
    """Contract every LLM provider must follow."""

    @abstractmethod
    def generate(self, messages: list[Message], system_prompt: str | None = None) -> str:
        """Take the conversation, return the assistant reply text."""
        raise NotImplementedError