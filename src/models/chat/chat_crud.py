from sqlalchemy.orm import Session
from . import chat_model, chat_schemas

def create_chat(db: Session, chat: chat_schemas.ChatCreate):
    db_chat = chat_model.Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat(db: Session, chat_id: str):
    return db.query(chat_model.Chat).filter(chat_model.Chat.chat_id == chat_id).first()

def get_chats_for_assistant(db: Session, assistant_id: str, skip: int = 0, limit: int = 100):
    return db.query(chat_model.Chat).filter(chat_model.Chat.assistant_id == assistant_id).offset(skip).limit(limit).all()