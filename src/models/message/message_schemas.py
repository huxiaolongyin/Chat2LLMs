from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class MessageBase(BaseModel):
    chat_id: str
    role: Literal['user', 'assistant', 'system']
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    message_id: str
    create_time: datetime

    class Config:
        orm_mode = True
