from pydantic import BaseModel


class KnowledgeModel(BaseModel):
    data: str
