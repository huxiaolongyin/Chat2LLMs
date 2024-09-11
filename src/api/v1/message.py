import threading
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.base import BaseDataResponse, ErrorResponse
from fastapi.responses import JSONResponse, StreamingResponse
from core.database import sqlite_connection
from schemas.message import MessageBase, MessageBaseResponse
from services.chat import get_chat
from services.message import create_message, get_messages
from core.chatbot import ChatBot
from services.assistant import get_assistant
from services.chat import get_chat
from haystack.dataclasses import ChatMessage

router = APIRouter()


def _get_history_messages(db, message):
    assistant_id = get_chat(db=db, chat_id=message.chat_id).assistant_id
    prompt = get_assistant(db=db, assistant_id=assistant_id).prompt
    db_messages = get_messages(db=db, chat_id=message.chat_id, skip=0, limit=100)

    history_messages = []
    history_messages.append(ChatMessage.from_system(content=prompt))
    for db_message in db_messages[message.context_length : 0 : -1]:
        if db_message.role == "user":
            history_message = ChatMessage.from_user(db_message.content)
        elif db_message.role == "assistant":
            history_message = ChatMessage.from_assistant(db_message.content)
        history_messages.append(history_message)
    # 添加提示词
    history_messages.append(
        ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
    )
    return history_messages


@router.post(
    "",
    tags=["Message"],
    operation_id="create_message",
    summary="Create Message",
    response_model=BaseDataResponse,
)
async def new_message(
    db: Session = Depends(sqlite_connection), message: MessageBase = None
):
    # 获取对话，如果不存在则返回错误
    chat = get_chat(db, chat_id=message.chat_id)
    if not chat:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Chat not found").model_dump(),
        )
    # 创建ChatBot
    ollama = ChatBot(store=message.store)

    def ollama_start():
        from core.database import SessionLocal

        # 写入问题
        db: Session = SessionLocal()
        create_message(db=db, message=message)
        # 获取历史消息
        history_messages = _get_history_messages(db, message)
        ansewer = ollama.query(
            question=message.content, top_k=5, history_messages=history_messages
        )[0].content
        message.content, message.role = ansewer, "assistant"  # 写入回答
        create_message(db=db, message=message)

    write_thread = threading.Thread(target=ollama_start, args=())
    write_thread.start()

    return StreamingResponse(ollama.get_stream(), media_type="text/event-stream")


@router.get(
    "",
    tags=["Message"],
    operation_id="get_history_message",
    summary="获取历史消息",
    response_model=MessageBaseResponse,
)
async def message_list(
    chat_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(sqlite_connection),
):
    """获取历史消息"""
    db_messages = get_messages(db=db, chat_id=chat_id, skip=skip, limit=limit)
    return MessageBaseResponse(message=db_messages)
