from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class KnowledgeBase(BaseModel):
    store: str = Field(..., description="知识库名称，若没有则新建一个知识库")
    content: List[str] = Field(..., description="输入的知识内容")

    model_config = {
        "json_schema_extra": {
            "example": {
                "store": "test",
                "content": ["小明家在东北，他有两个哥哥", "小青住在福建"],
            }
        }
    }


# class Knowledge(KnowledgeBase):
#     chat_id: str
#     create_time: datetime
#     update_time: datetime

#     class Config:
#         from_attributes = True
