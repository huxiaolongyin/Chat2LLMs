from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class Suggestion(Base):
    __tablename__ = "suggestions"

    suggestion_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=True)
    create_time = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
