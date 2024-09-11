from fastapi import APIRouter, Depends, Query
from schemas import (
    AssistantBaseRequset,
    ErrorResponse,
    AssistantBaseResponse,
    BaseDataResponse,
)
from fastapi.responses import JSONResponse
from core.database import sqlite_connection
from sqlalchemy.orm import Session
from services.assistant import (
    create_assistant,
    get_assistants,
    update_assistant,
    delete_assistant,
)


router = APIRouter()


@router.post(
    "",
    tags=["Assistant"],
    operation_id="create_assistant",
    summary="创建助手",
    response_model=AssistantBaseResponse,
)
async def new_assistant(
    assistant: AssistantBaseRequset, db: Session = Depends(sqlite_connection)
):
    """创建助手"""
    db_assistant = create_assistant(db=db, assistant=assistant)
    if not db_assistant:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                detail="助手名称已存在"
            ).model_dump(),
        )
    return AssistantBaseResponse(assistant=db_assistant)


@router.get(
    "",
    tags=["Assistant"],
    operation_id="assistant_list",
    summary="Get Assistants",
    response_model=AssistantBaseResponse,
)
async def assistants_list(
    skip: int = Query(0, ge=0, description="跳过"),
    limit: int = Query(100, ge=1, le=100, description="返回数量"),
    db: Session = Depends(sqlite_connection),
):
    """获取助手列表"""
    assistants = get_assistants(db, skip=skip, limit=limit)
    return AssistantBaseResponse(assistant=assistants)


@router.put(
    "",
    tags=["Assistant"],
    operation_id="update_assistant",
    summary="Update Assistants",
    response_model=AssistantBaseResponse,
)
async def up_assistant(
    assistant: AssistantBaseRequset,
    assistant_id: str,
    db: Session = Depends(sqlite_connection),
):
    """更新助手"""
    db_assistant = update_assistant(
        db=db, assistant_id=assistant_id, assistant=assistant
    )
    if db_assistant is None:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="未找到该助手"),
        )
    # assistants_list = [assistant for assistant in assistants]
    return AssistantBaseResponse(assistant=db_assistant)


@router.delete(
    "",
    tags=["Assistant"],
    operation_id="delete_assistant",
    summary="Delete Assistants",
    response_model=AssistantBaseResponse,
)
async def del_assistant(assistant_id: str, db: Session = Depends(sqlite_connection)):
    """删除助手"""
    db_assistant = delete_assistant(db=db, assistant_id=assistant_id)
    if db_assistant is None:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="未找到该助手"),
        )
    return AssistantBaseResponse(assistant=db_assistant)
