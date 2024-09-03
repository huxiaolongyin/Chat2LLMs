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
# def get_chat(db: Session, chat_id: str):
#     return db.query(chat_model.Chat).filter(chat_model.Chat.chat_id == chat_id).first()

# def get_chats_for_assistant(db: Session, assistant_id: str, skip: int = 0, limit: int = 100):
#     return db.query(chat_model.Chat).filter(chat_model.Chat.assistant_id == assistant_id).offset(skip).limit(limit).all()