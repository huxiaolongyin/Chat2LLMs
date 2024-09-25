from sqlalchemy import Column, String, Text, Integer, DateTime
from .base import Base
from datetime import datetime


class Tool(Base):
    __tablename__ = "tools"

    tool_id = Column(Integer, primary_key=True, autoincrement=True, comment="工具id")
    json = Column(Text, nullable=True, comment="工具json")
    enabled = Column(Integer, nullable=True, comment="是否启用")
    create_time = Column(
        DateTime,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        comment="创建时间",
    )
    update_time = Column(
        DateTime,
        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        comment="更新时间",
    )
