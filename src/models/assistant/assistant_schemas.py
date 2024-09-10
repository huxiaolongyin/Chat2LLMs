from typing_extensions import Literal
from pydantic import BaseModel, Field
from typing import Any, Optional, List


class AssistantBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt: str


class Assistant(AssistantBase):
    assistant_id: str
    create_time: str
    update_time: str

    class Config:
        from_attributes = True
    

class AssistantResponse(BaseModel):
    status: str = Field(
        "success", pattern="^success$", description="The status of the response."
    )
    data: Assistant

class AssistantListResponse(BaseModel):
    status: str = Field(
        "success", pattern="^success$", description="The status of the response."
    )
    data: List[Assistant]
