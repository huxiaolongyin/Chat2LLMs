from sqlalchemy.orm import Session
from .message_schemas import MessageBase
from .message_model import Message

def create_message(db: Session, message: MessageBase):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, chat_id: str, skip: int = 0, limit: int = 100):
    return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.create_time).offset(skip).limit(limit).all()