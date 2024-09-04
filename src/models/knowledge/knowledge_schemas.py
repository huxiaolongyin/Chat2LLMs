from pydantic import BaseModel
from datetime import datetime
from typing import List


class KnowledgeBase(BaseModel):
    store: str
    content: List[str]


# class Knowledge(KnowledgeBase):
#     chat_id: str
#     create_time: datetime
#     update_time: datetime

#     class Config:
#         orm_mode = True
