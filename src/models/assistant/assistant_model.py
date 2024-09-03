from sqlalchemy import Column, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.sqlite.connection import Base
from utils import generate_id


class Assistant(Base):
    __tablename__ = "ai_assistants"

    assistant_id = Column(String, primary_key=True, index=True, default=generate_id)
    name = Column(String, index=True)
    description = Column(Text)
    prompt = Column(Text)
    create_time = Column(String, default=func.now())
    update_time = Column(String, default=func.now(), onupdate=func.now())

    chats = relationship("Chat", back_populates="assistant")
