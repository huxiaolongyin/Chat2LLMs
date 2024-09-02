from pydantic import BaseModel


class KnowledgeData(BaseModel):
    data: str
