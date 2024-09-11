from pydantic import BaseModel, Field
from typing import Literal, List, Union, Optional
from .base import BaseResponse


class MessageBase(BaseModel):
    message_id: Optional[int] = None
    chat_id: Optional[str] = None
    role: Optional[str] = None
    content: Optional[str] = None
    create_time: Optional[str] = None
    store: Optional[str] = None
    context_length: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "properties": {
                "message_id": {"description": "消息ID"},
                "chat_id": {"description": "聊天ID"},
                "role": {"description": "角色"},
                "content": {"description": "消息内容"},
                "create_time": {"description": "创建时间"},
                "store": {"description": "存储类型"},
                "context_length": {"description": "上下文长度"},
            },
            "examples": [
                {
                    "message_id": 1,
                    "chat_id": "AVG7zkTGtG1nv7cw",
                    "role": "user",
                    "content": "Hello, how are you?",
                    "create_time": "2023-05-01 12:00:00",
                    "store": "Document",
                    "context_length": 8,
                }
            ],
        },
    }


class MessageBaseRequest(BaseModel):
    chat_id: str = Field("AVG7zkTGtG1nv7cw", description="聊天ID")
    role: Literal["user", "assistant", "system"]
    content: Union[str, None]
    store: Union[str, None] = "Document"
    context_length: Union[int, None] = 8

    model_config = MessageBase.model_config


class MessageBaseResponse(BaseResponse):
    message: Union[MessageBase, List[MessageBase]]
