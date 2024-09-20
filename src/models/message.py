from sqlalchemy import Column, String, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key=True, autoincrement=True, comment="消息ID")
    chat_id = Column(String(16), ForeignKey("chats.chat_id"), comment="对话ID")
    question = Column(Text, nullable=True, comment="问题")
    answer = Column(Text, nullable=True, comment="答案")
    store = Column(String(50), nullable=True, comment="所用知识库")
    context_length = Column(Integer, nullable=True, comment="上下文长度")
    evaluation = Column(String(50), nullable=True, comment="评价")
    create_time = Column(
        DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), comment="创建时间"
    )

    chat = relationship("Chat", back_populates="messages")
