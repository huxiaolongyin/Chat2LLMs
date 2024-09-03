from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.sqlite.connection import Base
from utils import generate_id


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(36), ForeignKey("chats.chat_id"))
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    create_time = Column(String, default=func.now())

    chat = relationship("Chat", back_populates="message")
