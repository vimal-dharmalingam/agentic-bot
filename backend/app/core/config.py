from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All app config in one typed class. Values come from env vars or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "agentic-bot"
    environment: str = "local"                 # local | dev | prod

    aws_region: str = "us-east-1"
    sessions_table: str = "agentic-bot-sessions"
    dynamodb_endpoint: str | None = None       # None = real AWS

    llm_provider: str = "fake"                 # fake | bedrock
    bedrock_model_id: str = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
    max_tokens: int = 512
    max_history_messages: int = 10

    cors_origins: list[str] = ["http://localhost:5173"]

    session_store: str = "dynamodb"            # dynamodb | memory
    session_ttl_days: int = 30


@lru_cache
def get_settings() -> Settings:
    """Create Settings once and reuse it (acts like a singleton)."""
    return Settings()