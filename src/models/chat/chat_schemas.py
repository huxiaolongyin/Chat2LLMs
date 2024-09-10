from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ChatBase(BaseModel):
    title: str = Field(..., description="聊天会话的标题")
    assistant_id: str = Field(..., description="助手的ID")


class Chat(ChatBase):
    chat_id: str
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    status: str = Field(
        "success", pattern="^success$", description="The status of the response."
    )
    data: Chat


class ChatListResponse(BaseModel):
    status: str = Field(
        "success", pattern="^success$", description="The status of the response."
    )
    data: List[Chat]
