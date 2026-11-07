from app.core.models import Message
from app.repositories.base import SessionRepository


class InMemorySessionRepository(SessionRepository):
    """Dict-based store for unit tests. Data is lost when the process stops."""

    def __init__(self) -> None:
        self._store: dict[str, list[Message]] = {}

    def save_message(self, session_id: str, message: Message) -> None:
        self._store.setdefault(session_id, []).append(message)

    def get_history(self, session_id: str, limit: int = 10) -> list[Message]:
        return self._store.get(session_id, [])[-limit:]