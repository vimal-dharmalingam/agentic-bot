from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from app.core.exceptions import LLMProviderError
from app.core.models import Message
from app.providers.bedrock_provider import BedrockProvider


def _make_provider(client) -> BedrockProvider:
    return BedrockProvider(model_id="test-model", region="us-east-1", max_tokens=100, client=client)


def test_returns_text_and_builds_correct_request():
    client = MagicMock()
    client.converse.return_value = {"output": {"message": {"content": [{"text": "hi there"}]}}}

    reply = _make_provider(client).generate([Message("user", "hello")], system_prompt="be nice")

    assert reply == "hi there"
    sent = client.converse.call_args.kwargs
    assert sent["modelId"] == "test-model"
    assert sent["messages"] == [{"role": "user", "content": [{"text": "hello"}]}]
    assert sent["system"] == [{"text": "be nice"}]
    assert sent["inferenceConfig"]["maxTokens"] == 100


def test_aws_error_is_wrapped_in_our_exception():
    client = MagicMock()
    client.converse.side_effect = ClientError(
        {"Error": {"Code": "ThrottlingException", "Message": "slow down"}}, "Converse"
    )

    with pytest.raises(LLMProviderError):
        _make_provider(client).generate([Message("user", "hello")])