from pydantic import BaseModel, Field
from typing import Optional, List


class AssistantBase(BaseModel):
    name: str
    description: Optional[str] = None
    prompt: str


class Assistant(AssistantBase):
    assistant_id: str
    create_time: str
    update_time: str

    class Config:
        orm_mode = True


class AssistantList(BaseModel):
    status: str = Field(
        "success", pattern="^success$", description="The status of the response."
    )
    data: List[Assistant]
