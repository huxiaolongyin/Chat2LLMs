from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from models.base import BaseDataResponse, ErrorResponse
from fastapi.responses import JSONResponse
from database.sqlite.connection import get_db
from models.message.message_schemas import MessageBase
from models.chat.chat_crud import get_chat
from models.message.message_crud import create_message, get_messages
from core.chat import ChatWithOllama
from models.assistant.assistant_crud import get_assistant
from models.chat.chat_crud import get_chat
from haystack.dataclasses import ChatMessage

router = APIRouter()


@router.post(
    "",
    tags=["Message"],
    operation_id="create_message",
    summary="Create Message",
    response_model=BaseDataResponse,
)
async def new_message(
    message: MessageBase,
    db: Session = Depends(get_db),
):
    chat = get_chat(db, chat_id=message.chat_id)
    if not chat:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Chat not found").dict(),
        )

    assistant_id = get_chat(db=db, chat_id=message.chat_id).assistant_id
    prompt = get_assistant(db=db, assistant_id=assistant_id).prompt
    db_messages = get_messages(db=db, chat_id=message.chat_id, skip=0, limit=100)

    history_messages = []

    for db_message in db_messages[message.context_length :: -1]:
        if db_message.role == "user":
            history_message = ChatMessage.from_user(db_message.content)
        elif db_message.role == "assistant":
            history_message = ChatMessage.from_assistant(db_message.content)
        history_messages.append(history_message)
    # 添加提示词
    history_messages.append(ChatMessage.from_system(content=prompt))
    history_messages.append(
        ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}")
    )
    ollama = ChatWithOllama(store=message.store)
    ansewer = ollama.chat(
        question=message.content, top_k=5, history_messages=history_messages
    )[0].content
    # 写入问题
    create_message(db=db, message=message)
    # 写入回答
    message.content = ansewer
    message.role = "assistant"
    create_message(db=db, message=message)

    return BaseDataResponse(data={"answer": ansewer})


@router.get(
    "",
    tags=["Message"],
    operation_id="get_history_message",
    summary="Get History Message",
    response_model=BaseDataResponse,
)
async def message_list(
    chat_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return BaseDataResponse(
        data=get_messages(db=db, chat_id=chat_id, skip=skip, limit=limit)
    )
