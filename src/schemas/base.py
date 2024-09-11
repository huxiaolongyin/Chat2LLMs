from typing import Any
from pydantic import BaseModel, Field
from core.config import CONFIG
from datetime import datetime

class BaseResponse(BaseModel):
    """基础响应模型"""

    version: str = Field(CONFIG.VERSION, description="系统版本")
    status: str = Field("SUCCESS", Literal="SUCCESS", description="API状态")
    create_time: str = Field(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="创建时间")

class BaseDataResponse(BaseResponse):
    """基础数据响应模型"""

    data: Any = Field(..., description="响应数据(列表)")


class ErrorResponse(BaseResponse):
    """基础错误响应模型"""

    status: str = Field("error", description="API状态")
    detail: str = Field(..., description="错误详情")


# class BaseRequest(BaseModel):
#     """基础请求模型"""

#     pass
