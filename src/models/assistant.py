from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base, generate_id


class Assistant(Base):
    __tablename__ = "ai_assistants"

    assistant_id = Column(String(16), primary_key=True, index=True, default=generate_id)
    name = Column(String(255), index=True)
    description = Column(Text)
    prompt = Column(Text)
    create_time = Column(DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_time = Column(
        DateTime,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    chats = relationship("Chat", back_populates="assistant")
