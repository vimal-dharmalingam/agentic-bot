import uuid
from dataclasses import dataclass

from app.core.models import Message
from app.providers.base import LLMProvider
from app.repositories.base import SessionRepository


@dataclass(frozen=True)
class ChatResult:
    session_id: str
    reply: str


class ChatService:
    """Business logic: load history, call the LLM, save both messages."""

    SYSTEM_PROMPT = "You are a helpful, concise assistant."

    def __init__(self, llm: LLMProvider, repository: SessionRepository, max_history: int = 10):
        self._llm = llm
        self._repository = repository
        self._max_history = max_history

    def chat(self, user_message: str, session_id: str | None = None) -> ChatResult:
        session_id = session_id or str(uuid.uuid4())

        history = self._repository.get_history(session_id, limit=self._max_history)
        history = self._start_with_user(history)

        user_msg = Message(role="user", content=user_message)
        reply = self._llm.generate([*history, user_msg], system_prompt=self.SYSTEM_PROMPT)

        # save only after the LLM succeeds -> no half-saved conversations
        self._repository.save_message(session_id, user_msg)
        self._repository.save_message(session_id, Message(role="assistant", content=reply))

        return ChatResult(session_id=session_id, reply=reply)

    def get_history(self, session_id: str) -> list[Message]:
        return self._repository.get_history(session_id, limit=100)

    @staticmethod
    def _start_with_user(history: list[Message]) -> list[Message]:
        """Bedrock requires the conversation to start with a user message."""
        while history and history[0].role != "user":
            history = history[1:]
        return history