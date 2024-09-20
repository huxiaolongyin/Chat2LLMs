from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, generate_id

from datetime import datetime


class Chat(Base):
    __tablename__ = "chats"

    chat_id = Column(String, primary_key=True, index=True, default=generate_id)
    title = Column(String(255), nullable=False)
    assistant_id = Column(String(8), ForeignKey("ai_assistants.assistant_id"))
    create_time = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_time = Column(
        String,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    assistant = relationship("Assistant", back_populates="chats")
    # chat有多个message
    messages = relationship("Message", back_populates="chat")
