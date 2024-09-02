from fastapi import APIRouter
from api.models import KnowledgeData
from embedding import Knowledge

router = APIRouter()


@router.post("add_knowledge")
def add_knowledge(KnowledgeData: KnowledgeData):
    Knowledge.write([KnowledgeData.data])

    return {"status": "OK"}


def embed_query(query: str = None):
    response = Knowledge.get(query)
