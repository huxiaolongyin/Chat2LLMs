from fastapi import APIRouter
from models.base import BaseDataResponse
from core.retrieval import HTWDocument
from models.knowledge.knowledge_schemas import KnowledgeBase

router = APIRouter()


@router.get(
    "/list",
    tags=["Knowledge"],
    operation_id="knowledge_catalogue",
    summary="Get Knowledge Catalogue",
    response_model=BaseDataResponse,
)
async def knowledge_catalogue():
    return BaseDataResponse(data=HTWDocument().store_list())


@router.post(
    "/create",
    tags=["Knowledge"],
    operation_id="create_knowledge",
    summary="Create Knowledge",
    response_model=BaseDataResponse,
)
async def knowledge_create(documents: KnowledgeBase):
    return BaseDataResponse(
        data={
            "write_to_store": documents.store,
            "respose": HTWDocument(documents.store).write_docs(documents.content),
        }
    )
