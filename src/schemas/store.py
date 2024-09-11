from pydantic import BaseModel, Field
from typing import List, Union, Optional
from .base import BaseResponse


class StoreBase(BaseModel):
    store_name: Optional[str] = None
    status: Optional[str] = None
    document_count: Optional[int] = None
    embedding_size: Optional[int] = None
    distance: Optional[str] = None
    model_config = {
        "json_schema_extra": {
            "properties": {
                "store_name": {"description": "知识库名称"},
                "status": {"description": "知识库状态"},
                "document_count": {"description": "知识库文档数量"},
                "embedding_size": {"description": "知识库嵌入大小"},
                "distance": {"description": "知识库用的距离算法"},
            }
        }
    }


class StoreBaseRequest(BaseModel):
    store_name: str
    model_config = StoreBase.model_config


class StoreBaseResponse(BaseResponse):
    store_info: Union[StoreBase, List[StoreBase]] = Field(..., description="知识库信息")