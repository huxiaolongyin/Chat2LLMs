from fastapi import APIRouter, Query, Path
from models.base import BaseDataResponse, ErrorResponse
from core.retrieval import HTWDocument
from models.knowledge.knowledge_schemas import KnowledgeBase
from fastapi.responses import JSONResponse
from typing import List, Union

router = APIRouter()


@router.get(
    "/store",
    tags=["Knowledge"],
    operation_id="knowledge_catalogue",
    summary="知识库目录",
    response_model=BaseDataResponse,
)
async def knowledge_catalogue():
    return BaseDataResponse(data=HTWDocument().store_list())


@router.get(
    "/{store}",
    tags=["Knowledge"],
    operation_id="knowledge_content",
    summary="知识库内容",
    response_model=BaseDataResponse,
)
async def knowledges(store: str = Path(..., description="知识库名称")):
    if store not in HTWDocument().store_list():
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="Store not found").model_dump(),
        )
    return BaseDataResponse(data=HTWDocument(store).get_docs())


@router.post(
    "",
    tags=["Knowledge"],
    operation_id="create_knowledge",
    summary="创建知识(若没有知识库，则新建)",
    response_model=BaseDataResponse,
)
async def new_knowledge(documents: KnowledgeBase):
    return BaseDataResponse(
        data={
            "write_to_store": documents.store,
            "respose": HTWDocument(documents.store).write_docs(documents.content),
        }
    )


@router.delete(
    "",
    tags=["Knowledge"],
    operation_id="delete_knowledge",
    summary="删除知识",
    response_model=BaseDataResponse,
)
async def del_knowledge(store: str, document_id: Union[list, str]):
    if isinstance(document_id, str):
        document_id = [document_id]
    return BaseDataResponse(data=HTWDocument(store).del_docs(document_id))


@router.delete(
    "/{store}",
    tags=["Knowledge"],
    operation_id="delete_knowledge_store",
    summary="删除知识库",
    response_model=BaseDataResponse,
)
async def del_knowledge_store(store: str):
    """todo"""
    pass
