from dataclasses import dataclass
from typing import Literal

Role = Literal["user", "assistant"]


@dataclass(frozen=True)
class Message:
    """One chat message. frozen=True makes it immutable."""

    role: Role
    content: str