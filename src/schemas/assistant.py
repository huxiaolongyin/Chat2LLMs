from pydantic import BaseModel, Field
from typing import Optional, List, Union
from .base import BaseResponse
from models import Assistant


class AssistantBase(BaseModel):
    """助手模型"""

    assistant_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    prompt: Optional[str] = None
    create_time: Optional[str] = None
    update_time: Optional[str] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "properties": {
                "assistant_id": {"description": "助手ID"},
                "name": {"description": "助手名称"},
                "description": {"description": "助手描述"},
                "prompt": {"description": "助手提示词"},
                "create_time": {"description": "创建时间"},
                "update_time": {"description": "更新时间"},
            }
        },
    }


class AssistantBaseRequset(BaseModel):
    """助手请求模型"""

    name: str = Field(..., description="助手名称")
    description: Optional[str] = Field(None, description="助手描述")
    prompt: str = Field(..., description="助手提示词")


class AssistantBaseResponse(BaseResponse):
    """助手响应模型"""

    assistant: Union[AssistantBase, List[AssistantBase]] = Field(
        ..., description="助手信息"
    )
