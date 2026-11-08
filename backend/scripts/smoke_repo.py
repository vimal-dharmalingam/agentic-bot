import uuid

from app.core.config import get_settings
from app.core.models import Message
from app.repositories.factory import build_session_repository


def main() -> None:
    repo = build_session_repository(get_settings())
    session_id = f"smoke-{uuid.uuid4()}"

    repo.save_message(session_id, Message("user", "hi"))
    repo.save_message(session_id, Message("assistant", "Hello! How can I help?"))
    repo.save_message(session_id, Message("user", "what is DynamoDB?"))

    print(type(repo).__name__, "| session:", session_id)
    for msg in repo.get_history(session_id, limit=10):
        print(f"  {msg.role:9} -> {msg.content}")


if __name__ == "__main__":
    main()