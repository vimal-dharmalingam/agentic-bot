from abc import ABC, abstractmethod

from app.core.models import Message


class SessionRepository(ABC):
    """Contract for storing and loading chat history."""

    @abstractmethod
    def save_message(self, session_id: str, message: Message) -> None:
        """Append one message to a session."""
        raise NotImplementedError

    @abstractmethod
    def get_history(self, session_id: str, limit: int = 10) -> list[Message]:
        """Return the last `limit` messages, oldest first."""
        raise NotImplementedError