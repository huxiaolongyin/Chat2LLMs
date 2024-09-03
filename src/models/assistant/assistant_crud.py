from sqlalchemy.orm import Session
from models.assistant.assistant_model import Assistant
from models.assistant.assistant_schemas import AssistantCreate


def get_assistant_by_name(db: Session, name: str):
    return db.query(Assistant).filter(Assistant.name == name).first()


def create_assistant(db: Session, assistant: AssistantCreate):
    """创建助手"""
    existing_assistant = get_assistant_by_name(db, assistant.name)
    if existing_assistant:
        return None
    db_assistant = Assistant(**assistant.dict())
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


def get_assistant(db: Session, assistant_id: str):
    return db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()


def get_assistants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Assistant).offset(skip).limit(limit).all()


def update_assistant(
    db: Session, assistant_id: str, assistant: AssistantCreate
):
    db_assistant = (
        db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()
    )
    if db_assistant:
        for key, value in assistant.dict().items():
            setattr(db_assistant, key, value)
        db.commit()
        db.refresh(db_assistant)
    return db_assistant


def delete_assistant(db: Session, assistant_id: str):
    db_assistant = (
        db.query(Assistant).filter(Assistant.assistant_id == assistant_id).first()
    )
    if db_assistant:
        db.delete(db_assistant)
        db.commit()
    return db_assistant
