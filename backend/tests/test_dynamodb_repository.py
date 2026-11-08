import time

import boto3
import pytest
from moto import mock_aws

from app.core.models import Message
from app.repositories.dynamodb_repository import DynamoSessionRepository

TABLE_NAME = "test-sessions"
REGION = "us-east-1"


@pytest.fixture
def dynamo_repo():
    with mock_aws():
        boto3.client("dynamodb", region_name=REGION).create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "ts", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "ts", "AttributeType": "N"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        yield DynamoSessionRepository(table_name=TABLE_NAME, region=REGION, ttl_days=30)


def test_messages_return_oldest_first(dynamo_repo):
    dynamo_repo.save_message("s1", Message("user", "hi"))
    dynamo_repo.save_message("s1", Message("assistant", "hello"))

    history = dynamo_repo.get_history("s1")

    assert [(m.role, m.content) for m in history] == [("user", "hi"), ("assistant", "hello")]


def test_limit_returns_only_latest_messages(dynamo_repo):
    for i in range(5):
        dynamo_repo.save_message("s1", Message("user", f"m{i}"))

    history = dynamo_repo.get_history("s1", limit=2)

    assert [m.content for m in history] == ["m3", "m4"]


def test_sessions_are_isolated(dynamo_repo):
    dynamo_repo.save_message("s1", Message("user", "for s1"))
    dynamo_repo.save_message("s2", Message("user", "for s2"))

    assert [m.content for m in dynamo_repo.get_history("s1")] == ["for s1"]


def test_unknown_session_returns_empty_list(dynamo_repo):
    assert dynamo_repo.get_history("nope") == []


def test_ttl_expiry_is_about_30_days_ahead(dynamo_repo):
    dynamo_repo.save_message("s1", Message("user", "hi"))

    item = boto3.resource("dynamodb", region_name=REGION).Table(TABLE_NAME).scan()["Items"][0]
    expected = time.time() + 30 * 86_400
    assert abs(int(item["expires_at"]) - expected) < 60