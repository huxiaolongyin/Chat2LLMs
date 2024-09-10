from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from database.sqlite.connection import get_db
from models.base import BaseDataResponse, ErrorResponse
from models.chat.chat_schemas import ChatBase, ChatListResponse, ChatResponse
from models.chat.chat_crud import (
    create_chat,
    get_chat,
    get_chat_for_assistant,
    update_chat,delete_chat,
    Session,
)
from models.assistant.assistant_crud import get_assistant

router = APIRouter()


@router.get(
    "",
    tags=["Chat"],
    operation_id="get_chat",
    summary="Get chat",
    response_model=BaseDataResponse,
)
async def chat_list(assistant_id, db: Session = Depends(get_db)):
    assistant = get_assistant(db, assistant_id=assistant_id)
    if not assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found"),
        )
    db_chat = get_chat_for_assistant(db=db, assistant_id=assistant_id)
    return ChatListResponse(data=db_chat)


@router.post(
    "",
    tags=["Chat"],
    operation_id="create_chat",
    summary="Create chat",
    response_model=ChatResponse,
)
async def new_chat(chat: ChatBase, db: Session = Depends(get_db)):
    assistant = get_assistant(db, assistant_id=chat.assistant_id)
    if not assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found"),
        )
    db_chat = create_chat(db=db, chat=chat)
    return ChatResponse(data=db_chat)


@router.put(
    "",
    tags=["Chat"],
    operation_id="update_chat",
    summary="Update chat",
    response_model=ChatResponse,
)
async def up_chat(chat_id, title: str, db: Session = Depends(get_db)):
    assistant = get_chat(db, chat_id=chat_id)
    if not assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found").dict(),
        )
    db_chat = update_chat(db=db, chat_id=chat_id, title=title)    
    return ChatResponse(data=db_chat)


@router.delete(
    "",
    tags=["Chat"],
    operation_id="delete_chat",
    summary="Delete chat",
    response_model=ChatResponse,
)
async def del_chat(chat_id, db: Session = Depends(get_db)):
    chat = get_chat(db, chat_id=chat_id)
    if not chat:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Chat not found").dict(),
        )
    db_chat = delete_chat(db=db, chat_id=chat_id)    
    return ChatResponse(data=db_chat)