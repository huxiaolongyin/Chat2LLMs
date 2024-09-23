from sqlalchemy import Column, String, Text, DateTime
from .base import Base
from datetime import datetime


class Issue(Base):
    __tablename__ = "issues"

    issue_id = Column(String(100), primary_key=True)
    issue = Column(Text, nullable=True)
    status = Column(String(100), nullable=True)
    priority = Column(String(100), nullable=True)
    create_time = Column(DateTime, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    response_time = Column(DateTime, nullable=True)
    complete_time = Column(DateTime, nullable=True)
