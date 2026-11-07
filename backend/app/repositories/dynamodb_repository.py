import time

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import BotoCoreError, ClientError

from app.core.exceptions import RepositoryError
from app.core.models import Message
from app.repositories.base import SessionRepository

SECONDS_PER_DAY = 86_400


class DynamoSessionRepository(SessionRepository):
    """One DynamoDB item per message. PK = session_id, SK = ts (nanoseconds)."""

    def __init__(
        self,
        table_name: str,
        region: str,
        ttl_days: int = 30,
        endpoint_url: str | None = None,
        table=None,
    ):
        self._ttl_seconds = ttl_days * SECONDS_PER_DAY
        if table is None:
            dynamodb = boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url)
            table = dynamodb.Table(table_name)
        self._table = table

    def save_message(self, session_id: str, message: Message) -> None:
        item = {
            "session_id": session_id,
            "ts": time.time_ns(),                       # unique + sortable
            "role": message.role,
            "content": message.content,
            "expires_at": int(time.time()) + self._ttl_seconds,   # TTL in epoch seconds
        }
        try:
            self._table.put_item(Item=item)
        except (ClientError, BotoCoreError) as exc:
            raise RepositoryError(f"Failed to save message: {exc}") from exc

    def get_history(self, session_id: str, limit: int = 10) -> list[Message]:
        try:
            response = self._table.query(
                KeyConditionExpression=Key("session_id").eq(session_id),
                ScanIndexForward=False,     # newest first
                Limit=limit,                # only the last N
            )
        except (ClientError, BotoCoreError) as exc:
            raise RepositoryError(f"Failed to load history: {exc}") from exc

        items = reversed(response.get("Items", []))    # back to oldest first
        return [Message(role=item["role"], content=item["content"]) for item in items]