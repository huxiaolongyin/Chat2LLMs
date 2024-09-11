from sqlalchemy.orm import Session
from datetime import datetime
from models import Assistant
from schemas import AssistantBase, AssistantBaseRequset
from typing import List


def get_assistant_by_name(db: Session, name: str):
    return db.query(Assistant).filter(Assistant.name == name).first()


def create_assistant(db: Session, assistant: AssistantBase):
    """创建助手"""
    existing_assistant = get_assistant_by_name(db, assistant.name)
    if existing_assistant:
        return None
    db_assistant = Assistant(**assistant.model_dump())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


def get_assistant(db: Session, assistant_id: str):
    return db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()


def get_assistants(db: Session, skip: int = 0, limit: int = 100):
    """获取助手列表"""

    return db.query(Assistant).offset(skip).limit(limit).all()


def update_assistant(
    db: Session, assistant_id: str, assistant: AssistantBaseRequset
) -> AssistantBase:
    """更新助手"""
    db_assistant = (
        db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()
    )
    if db_assistant:
        for key, value in assistant.model_dump().items():
            setattr(db_assistant, key, value)
        setattr(
            db_assistant, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.commit()
        db.refresh(db_assistant)
    db_assistant = (
        db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()
    )
    return db_assistant


def delete_assistant(db: Session, assistant_id: str):
    db_assistant = (
        db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()
    )
    if db_assistant:
        db.delete(db_assistant)
        db.commit()
    return db_assistant
