from pydantic import BaseModel, Field
from typing import Any, Optional


class BaseEmptyResponse(BaseModel):
    status: str = Field(
        "success", Literal="success", description="The status of the response."
    )


class BaseDataResponse(BaseModel):
    status: str = Field(
        "success", Literal="success", description="The status of the response."
    )
    data: Any = Field(...)
