from sqlalchemy.orm import Session
from models import Chat
from schemas import ChatBaseRequest
from datetime import datetime


def create_chat(db: Session, data: ChatBaseRequest):
    db_chat = Chat(**data.model_dump())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    
    return db_chat


def get_chat(db: Session, chat_id: str):
    return db.query(Chat).filter(Chat.chat_id == chat_id).first()


def get_chat_for_assistant(db: Session, assistant_id: str):
    return db.query(Chat).filter(Chat.assistant_id == assistant_id).all()


def update_chat(db: Session, chat_id: str, title: str):
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    setattr(db_chat, "title", title)
    setattr(db_chat, "update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.commit()
    db.refresh(db_chat)
    return db.query(Chat).filter(Chat.chat_id == chat_id).first()


def delete_chat(db: Session, chat_id: str):
    db_chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
    if db_chat:
        db.delete(db_chat)
        db.commit()
    return db_chat


def get_chats_for_assistant(
    db: Session, assistant_id: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(Chat)
        .filter(Chat.assistant_id == assistant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
