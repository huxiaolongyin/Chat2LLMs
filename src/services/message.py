from sqlalchemy.orm import Session
from schemas import MessageBase
from models import Message
from sqlalchemy import desc
from typing import List


def create_message(db: Session, message: MessageBase):
    db_message = Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_messages(
    db: Session, chat_id: str, skip: int = 0, limit: int = 100
) -> List[MessageBase]:

    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(desc(Message.message_id))
        .offset(skip)
        .limit(limit)
        .all()
    )