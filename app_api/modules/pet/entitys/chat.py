from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


@dataclass(frozen=True)
class Message(BaseModel):
    user_id: str
    message: str
    date_create: datetime
    register_status: bool


@dataclass(frozen=True)
class Chat(BaseModel):
    chat_id: Optional[str]
    from_user_id: str
    to_user_id: str
    pet_id: str
    messages: List[Message]
    date_create: datetime
    register_status: bool
