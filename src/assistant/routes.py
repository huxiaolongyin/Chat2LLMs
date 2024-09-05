from fastapi import APIRouter, Depends, Query
from models.base import BaseDataResponse, ErrorResponse
from fastapi.responses import JSONResponse
from database.sqlite.connection import get_db
from sqlalchemy.orm import Session

from models.assistant.assistant_schemas import AssistantBase, AssistantList
from models.assistant.assistant_crud import *
from .chat_routes import router as chat_router


router = APIRouter()


@router.post(
    "",
    tags=["Assistant"],
    operation_id="create_assistant",
    summary="Create Assistants",
    response_model=BaseDataResponse,
)
async def new_assistant(assistant: AssistantBase, db: Session = Depends(get_db)):
    """创建助手"""
    db_assistant = create_assistant(db=db, assistant=assistant)
    if not db_assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                detail="Assistant with this name already exists"
            ).dict(),
        )
    return BaseDataResponse(status="success", data=db_assistant)


@router.get(
    "",
    tags=["Assistant"],
    operation_id="assistant_list",
    summary="Get Assistants",
    response_model=AssistantList,
)
async def assistants_list(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    db: Session = Depends(get_db),
):
    """获取助手列表"""
    assistants = get_assistants(db, skip=skip, limit=limit)
    return AssistantList(data=assistants)


@router.put(
    "",
    tags=["Assistant"],
    operation_id="update_assistant",
    summary="Update Assistants",
    response_model=BaseDataResponse,
)
async def up_assistant(
    assistant: AssistantBase,
    assistant_id: str,
    db: Session = Depends(get_db),
):
    """更新助手"""
    db_assistant = update_assistant(
        db=db, assistant_id=assistant_id, assistant=assistant
    )
    if db_assistant is None:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found").dict(),
        )
    return BaseDataResponse(data=db_assistant)


@router.delete(
    "",
    tags=["Assistant"],
    operation_id="delete_assistant",
    summary="Delete Assistants",
    response_model=BaseDataResponse,
)
async def del_assistant(assistant_id: str, db: Session = Depends(get_db)):
    """删除助手"""
    db_assistant = delete_assistant(db=db, assistant_id=assistant_id)
    if db_assistant is None:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Assistant not found").dict(),
        )
    return BaseDataResponse(data=db_assistant)


router.include_router(chat_router, prefix="/chat")
