from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class MessageBase(BaseModel):
    chat_id: str = "AVG7zkTGtG1nv7cw"
    role: Literal["user", "assistant", "system"]
    content: str
    store: str = "Document"
    context_length: int = 8


class Message(MessageBase):
    message_id: str
    create_time: datetime

    class Config:
        orm_mode = True
