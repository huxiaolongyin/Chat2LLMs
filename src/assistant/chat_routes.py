from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from database.sqlite.connection import get_db
from models.base import BaseDataResponse, ErrorResponse
from models.chat.chat_schemas import ChatCreate
from models.chat.chat_crud import *
from models.assistant.assistant_crud import *
from .message_routes import router as message_router

router = APIRouter()


@router.post(
    "/create",
    tags=["Chat"],
    operation_id="create_chat",
    summary="Create chat",
    response_model=BaseDataResponse,
)
async def new_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    assistant = get_assistant(db, assistant_id=chat.assistant_id)
    if not assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found").dict(),
        )
    db_chat = create_chat(db=db, chat=chat)
    return BaseDataResponse(data=db_chat)


router.include_router(message_router, prefix="/message")
