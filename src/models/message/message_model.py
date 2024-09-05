from sqlalchemy import Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from database.sqlite.connection import Base
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(36), ForeignKey("chats.chat_id"))
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    create_time = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    store = Column(String(50), nullable=False)
    context_length = Column(Integer)

    chat = relationship("Chat", back_populates="message")
