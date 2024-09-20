from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, generate_id


class Assistant(Base):
    __tablename__ = "ai_assistants"

    assistant_id = Column(String, primary_key=True, index=True, default=generate_id)
    name = Column(String, index=True)
    description = Column(Text)
    prompt = Column(Text)
    create_time = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_time = Column(
        String,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    chats = relationship("Chat", back_populates="assistant")
