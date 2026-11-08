from app.core.config import Settings
from app.providers.base import LLMProvider
from app.providers.bedrock_provider import BedrockProvider
from app.providers.fake_provider import FakeLLMProvider


def build_llm_provider(settings: Settings) -> LLMProvider:
    """Factory: pick the provider from config; caller never knows which one."""
    if settings.llm_provider == "fake":
        return FakeLLMProvider()
    if settings.llm_provider == "bedrock":
        return BedrockProvider(
            model_id=settings.bedrock_model_id,
            region=settings.aws_region,
            max_tokens=settings.max_tokens,
        )
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")