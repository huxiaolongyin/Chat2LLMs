from pydantic import BaseModel, Field
from typing import Literal, List, Union, Optional
from .base import BaseResponse


class MessageBase(BaseModel):
    message_id: Optional[int] = None
    chat_id: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    store: Optional[str] = None
    context_length: Optional[int] = None
    evaluation: Optional[str] = None
    create_time: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_sche"
        "json_schema_extra": {
            "properties": {
                "message_id": {"description": "消息ID"},
                "chat_id": {"description": "聊天ID"},
                "question": {"description": "问题"},
                "answer": {"description": "答案"},
                "store": {"description": "存储类型"},
                "context_length": {"description": "上下文长度"},
                "evaluation": {"description": "评价"},
                "create_time": {"description": "创建时间"},
            },
            "examples": [
                {
                    "message_id": 1,
                    "chat_id": "AVG7zkTGtG1nv7cw",
                    "question": "How are you?",
                    "answer": "I am good.",
                    "store": "Document",
                    "context_length": 8,
                    "evaluation": "1",
                    "create_time": "2023-05-01 12:00:00",
                }
            ],
        },
    }


class MessageBaseRequest(BaseModel):
    chat_id: str = Field("AVG7zkTGtG1nv7cw", description="聊天ID")
    question: Union[str, None] = Field("你叫什么名字", description="问题")
    store: Union[str, None] = Field("Document", description="所使用的知识库")
    context_length: Union[int, None] = Field(8, description="上下文长度")


class MessageBaseResponse(BaseResponse):
    message: Union[MessageBase, List[MessageBase]]
