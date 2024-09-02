from pydantic import BaseModel


class ChatData(BaseModel):
    assistant_id: str
    chat_id: str
    question: str 