from pydantic import BaseModel
from datetime import datetime


class ChatBase(BaseModel):
    title: str
    assistant_id: str
    store: str = "Document"
    context_length: int=8


class Chat(ChatBase):
    chat_id: str
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
