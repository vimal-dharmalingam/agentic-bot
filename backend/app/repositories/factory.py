from app.core.config import Settings
from app.repositories.base import SessionRepository
from app.repositories.dynamodb_repository import DynamoSessionRepository
from app.repositories.in_memory_repository import InMemorySessionRepository


def build_session_repository(settings: Settings) -> SessionRepository:
    """Factory: pick the storage backend from config."""
    if settings.session_store == "memory":
        return InMemorySessionRepository()
    if settings.session_store == "dynamodb":
        return DynamoSessionRepository(
            table_name=settings.sessions_table,
            region=settings.aws_region,
            ttl_days=settings.session_ttl_days,
            endpoint_url=settings.dynamodb_endpoint,
        )
    raise ValueError(f"Unknown session store: {settings.session_store}")