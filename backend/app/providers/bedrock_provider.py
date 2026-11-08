import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.core.exceptions import LLMProviderError
from app.core.models import Message
from app.providers.base import LLMProvider


class BedrockProvider(LLMProvider):
    """Calls Amazon Bedrock using the Converse API."""

    def __init__(self, model_id: str, region: str, max_tokens: int = 512, client=None):
        self._model_id = model_id
        self._max_tokens = max_tokens
        self._client = client or boto3.client("bedrock-runtime", region_name=region)

    def generate(self, messages: list[Message], system_prompt: str | None = None) -> str:
        request = {
            "modelId": self._model_id,
            "messages": [
                {"role": m.role, "content": [{"text": m.content}]} for m in messages
            ],
            "inferenceConfig": {"maxTokens": self._max_tokens, "temperature": 0.3},
        }
        if system_prompt:
            request["system"] = [{"text": system_prompt}]

        try:
            response = self._client.converse(**request)
        except (ClientError, BotoCoreError) as exc:
            raise LLMProviderError(f"Bedrock call failed: {exc}") from exc

        return response["output"]["message"]["content"][0]["text"]