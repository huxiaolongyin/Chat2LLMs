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
ollama = ChatWithOllama()


@router.post(
    "",
    tags=["Message"],
    operation_id="create_message",
    summary="Create Message",
    response_model=BaseDataResponse,
)
async def new_message(message: MessageBase, db: Session = Depends(get_db)):
    chat = get_chat(db, chat_id=message.chat_id)
    if not chat:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Chat not found").dict(),
        )
    # 写入数据
    create_message(db=db, message=message)

    assistant_id = get_chat(db=db, chat_id=message.chat_id).assistant_id
    prompt = get_assistant(db=db, assistant_id=assistant_id).prompt
    db_messages = get_messages(db=db, chat_id=message.chat_id, skip=0, limit=100)

    history_messages = []
    # 添加提示词
    history_messages.append(ChatMessage.from_system(content=prompt))
    for db_message in db_messages[-8:]:
        if db_message.role == "user":
            history_message = ChatMessage.from_user(db_message.content)
        elif db_message.role == "assistant":
            history_message = ChatMessage.from_assistant(db_message.content)
        history_messages.append(history_message)
    history_messages.append(ChatMessage.from_user("问题：{{question}}，参考内容：{{content}}"))
    ansewer = ollama.chat(message.content,top_k=5, history_messages=history_messages)[0].content
    message.content = ansewer
    message.role = "assistant"

    create_message(db=db, message=message)
    return BaseDataResponse(
        data={"answer": ansewer}
    )
