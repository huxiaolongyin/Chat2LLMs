from pydantic import BaseModel


class ChatData(BaseModel):
    question: str 