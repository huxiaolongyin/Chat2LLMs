from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from core.database import get_db
from schemas import ChatBaseResponse, ErrorResponse, ChatBaseRequest, ChatBaseRequest
from sqlalchemy.orm import Session
from services.chat import (
    create_chat,
    get_chat,
    get_chat_for_assistant,
    update_chat,
    delete_chat,
)
from services.assistant import get_assistant

router = APIRouter()


def check_assistant(db, assistant_id):
    assistant = get_assistant(db, assistant_id=assistant_id)
    if not assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant id is required"),
        )


@router.get(
    "",
    tags=["Chat"],
    operation_id="get_chat",
    summary="获取全部会话",
    response_model=ChatBaseResponse,
)
async def chat_list(assistant_id, db: Session = Depends(get_db)):
    """获取全部会话"""
    check_assistant(db, assistant_id)
    db_chat = get_chat_for_assistant(db=db, assistant_id=assistant_id)
    return ChatBaseResponse(chat=db_chat)


@router.post(
    "",
    tags=["Chat"],
    operation_id="create_chat",
    summary="创建会话",
    response_model=ChatBaseResponse,
)
async def new_chat(data: ChatBaseRequest, db: Session = Depends(get_db)):
    """创建会话"""
    check_assistant(db, data.assistant_id)
    db_chat = create_chat(db=db, data=data)
    return ChatBaseResponse(chat=db_chat)


@router.put(
    "",
    tags=["Chat"],
    operation_id="update_chat",
    summary="更新会话",
    response_model=ChatBaseResponse,
)
async def up_chat(chat_id, title: str, db: Session = Depends(get_db)):
    assistant = get_chat(db, chat_id=chat_id)
    if not assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found").model_dump(),
        )
    db_chat = update_chat(db=db, chat_id=chat_id, title=title)
    return ChatBaseResponse(chat=db_chat)


@router.delete(
    "",
    tags=["Chat"],
    operation_id="delete_chat",
    summary="删除会话",
    response_model=ChatBaseResponse,
)
async def del_chat(chat_id, db: Session = Depends(get_db)):
    """删除会话"""
    chat = get_chat(db, chat_id=chat_id)
    if not chat:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Chat not found").model_dump(),
        )
    db_chat = delete_chat(db=db, chat_id=chat_id)
    return ChatBaseResponse(chat=db_chat)
