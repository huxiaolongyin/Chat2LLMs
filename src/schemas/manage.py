from pydantic import Field
from .base import BaseResponse


class SytemStatusResponse(BaseResponse):
    health: dict = Field(..., description="系统健康情况")
