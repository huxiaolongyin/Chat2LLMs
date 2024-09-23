from sqlalchemy import Column, String, Text, Integer, DateTime
from .base import Base
from datetime import datetime


class Tool(Base):
    __tablename__ = "tools"

    tool_id = Column(Integer, primary_key=True, autoincrement=True, comment="工具id")
    link = Column(Text, nullable=True, comment="工具链接")
    method = Column(String(50), nullable=True, comment="工具方法")
    name = Column(String(50), nullable=True, comment="工具名称")
    english_name = Column(String(50), nullable=True, comment="工具英文名称")
    description = Column(Text, nullable=True, comment="工具描述")
    parameters = Column(Text, nullable=True, comment="函数参数")
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
