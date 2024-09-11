from pydantic import BaseModel, Field
from typing import List, Union, Optional
from .base import BaseResponse


class DocumentBase(BaseModel):
    id: Optional[str] = None
    content: Optional[str] = None
    # dataframe: str
    # blob: int
    # meta: str
    # score: str
    # sparse_embedding: str

    model_config = {
        "json_schema_extra": {
            "properties": {
                "id": {"description": "文档ID"},
                "content": {"description": "文档内容"},
                # "dataframe": {"description": "文档数据"},
                # "blob": {"description": "文档blob"},
                # "meta": {"description": "文档元数据"},
                # "score": {"description": "文档分数"},
                # "sparse_embedding": {"description": "文档稀疏嵌入"},
            }
        }
    }


class DocumentBaseRequest(BaseModel):
    store_name: str = Field(..., description="知识库名称")
    content: str = Field(..., description="文档内容")


class DocumentBaseResponse(BaseResponse):
    store_name: str = Field(..., description="知识库名称")
    document: Union[DocumentBase, List[DocumentBase]] = Field(
        ..., description="文档信息"
    )


# class KnowledgeRequest(KnowledgeBase):
#     pass

# class Knowledge(KnowledgeBase):
#     chat_id: str
#     create_time: datetime
#     update_time: datetime

#     class Config:
#         from_attributes = True
