from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.sqlite.connection import Base
from utils import generate_id


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(String, primary_key=True, index=True, default=generate_id)
    title = Column(String(255), nullable=False)
    assistant_id = Column(String(8), ForeignKey("ai_assistants.assistant_id"))
    create_time = Column(String, default=func.now())
    update_time = Column(String, default=func.now(), onupdate=func.now())

    assistant = relationship("Assistant", back_populates="chats")
    message = relationship("Message", back_populates="chat")