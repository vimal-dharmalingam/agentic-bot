from functools import lru_cache

from app.core.config import get_settings
from app.providers.factory import build_llm_provider
from app.repositories.factory import build_session_repository
from app.services.chat_service import ChatService


@lru_cache
def get_chat_service() -> ChatService:
    """Built once per process. In Lambda: once per warm container, reused across requests."""
    settings = get_settings()
    return ChatService(
        llm=build_llm_provider(settings),
        repository=build_session_repository(settings),
        max_history=settings.max_history_messages,
    )