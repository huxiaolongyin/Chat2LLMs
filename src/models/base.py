from pydantic import BaseModel, Field
from typing import Any, Optional


__all__ = ["BaseEmptyResponse", "BaseDataResponse", "ErrorResponse"]


class BaseEmptyResponse(BaseModel):
    status: str = Field(
        "success", Literal="success", description="The status of the response."
    )


class BaseDataResponse(BaseModel):
    status: str = Field(
        "success", Literal="success", description="The status of the response."
    )
    data: Any = Field(...)


class ErrorResponse(BaseModel):
    status: str = Field("error", const=True, description="The status of the response.")
    detail: str


