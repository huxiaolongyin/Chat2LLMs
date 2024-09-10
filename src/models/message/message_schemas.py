from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, List, Union


class MessageBase(BaseModel):
    chat_id: str = "AVG7zkTGtG1nv7cw"
    role: Literal["user", "assistant", "system"]
    content: Union[str, None]
    store: Union[str, None] = "Document"
    context_length: Union[int, None] = 8


class Message(MessageBase):
    message_id: Union[int, None]
    create_time: datetime

    class Config:
        from_attributes = True

class MessageListResponse(BaseModel):
    status: str = Field(
        "success", pattern="^success$", description="The status of the response."
    )
    data: List[Message]