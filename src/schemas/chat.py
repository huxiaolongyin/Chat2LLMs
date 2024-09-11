from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Union, Optional
from .base import BaseResponse


class ChatBase(BaseModel):
    chat_id: Optional[str] = None
    title: Optional[str] = None
    assistant_id: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "properties": {
                "chat_id": {"description": "聊天会话的ID"},
                "title": {"description": "聊天会话的标题"},
                "assistant_id": {"description": "助手的ID"},
                "create_time": {"description": "聊天会话的创建时间"},
                "update_time": {"description": "聊天会话的更新时间"},
            }
        },
    }


class ChatBaseRequest(BaseModel):
    title: str = Field(..., description="聊天会话的标题")
    assistant_id: str = Field(..., description="助手的ID")


class ChatBaseResponse(BaseResponse):
    chat: Union[ChatBase, List[ChatBase]] = Field(..., description="聊天会话信息")
