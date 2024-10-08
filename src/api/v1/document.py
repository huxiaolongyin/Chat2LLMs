from fastapi import APIRouter, Query, Path
from core.embedding import HTWDocument
from schemas import (
    StoreBaseResponse,
    DocumentBaseResponse,
    ErrorResponse,
    DocumentBaseRequest,
    BaseDataResponse,
)
from fastapi.responses import JSONResponse
from typing import Union

router = APIRouter()


@router.get(
    "/store",
    tags=["Knowledge"],
    operation_id="knowledge_catalogue",
    summary="知识库目录",
    response_model=StoreBaseResponse,
)
async def get_all_store():
    """获取知识库的信息"""
    store_info = HTWDocument().get_all_knowledge_store_details()
    return StoreBaseResponse(store_info=store_info)


@router.get(
    "/{store}",
    tags=["Knowledge"],
    operation_id="knowledge_content",
    summary="知识库内容",
    response_model=DocumentBaseResponse,
)
async def knowledges(store: str = Path(..., description="知识库名称")):
    """获取知识库所有内容"""
    store_info = HTWDocument().get_all_knowledge_store_details()
    store_name_list = [store.store_name for store in store_info]
    # 判断知识库是否存在
    if store not in store_name_list:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(detail="知识库不存在").model_dump(),
        )
    document = HTWDocument(store).get_knowledge_content_or_all()
    return DocumentBaseResponse(store_name=store, document=document)


@router.post(
    "",
    tags=["Knowledge"],
    operation_id="create_knowledge",
    summary="创建知识(若没有知识库，则新建)",
    response_model=BaseDataResponse,
)
async def new_knowledge(data: DocumentBaseRequest):
    """创建知识内容"""
    result = HTWDocument(data.store_name).save_knowledge_content(data.content)
    return BaseDataResponse(data=result)


@router.delete(
    "",
    tags=["Knowledge"],
    operation_id="delete_knowledge",
    summary="删除知识",
    response_model=BaseDataResponse,
)
async def del_knowledge(store: str, document_id: Union[list, str]):
    """删除知识"""
    if isinstance(document_id, str):
        document_id = [document_id]
    return BaseDataResponse(
        data=HTWDocument(store).delete_knowledge_content(document_id)
    )


@router.delete(
    "/{store}",
    tags=["Knowledge"],
    operation_id="delete_knowledge_store",
    summary="删除知识库",
    response_model=BaseDataResponse,
)
async def del_knowledge_store(store_name: str):
    """删除知识库"""
    data = HTWDocument().delete_knowledge_store(store_name)
    return BaseDataResponse(data=data)
