from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


@dataclass(frozen=True)
class Notification(BaseModel):
    title: str
    body: str
    asset: str


@dataclass(frozen=True)
class Push(BaseModel):
    push_id: Optional[str]
    notification: Notification
    group: int
    from_user_id: str
    to_user_id: str
    data: datetime
    token: str
    date_create: datetime
    date_process: datetime
    register_status: bool


class ChatGroup(Enum):
    CHAT: int = 1
    CANDIDATE: int = 2
    ACCEPT_PENDING: int = 3
    ACCEPT_FALSE: int = 4
    ACCEPT_TRUE: int = 5
    ADOPT: int = 6
