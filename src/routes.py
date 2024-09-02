import json
from config import CONFIG
from fastapi import APIRouter
from assistant import ChatWithOllama
from fastapi.responses import StreamingResponse
from models import BaseEmptyResponse, ChatData, KnowledgeData, BaseDataResponse

router = APIRouter()

ollama = ChatWithOllama()


@router.get("/assistants", tags=["Assistant"], summary="Get Assistants")
async def get_assistants():
    """获取助手列表"""
    pass


@router.post("/chat", tags=["Assistant"], summary="Chat with Ollama", response_model=BaseDataResponse)
async def get_chat(chatdata: ChatData):
    answer, _ = ollama.chat(chatdata.question)
    return StreamingResponse({json.dumps({"answer": answer}, ensure_ascii=False)})


@router.get("/knowledge", tags=["Knowledge"], summary="Get knowledge")
async def get_knowledge():
    """获取知识内容"""
    return {"knowledge": ollama.knowledge_list()}


@router.post("/add_knowledge", tags=["Knowledge"], summary="Add knowledge")
async def add_knowledge(Data: KnowledgeData):
    """添加知识内容"""
    ollama.add_knowledge(Data.data)
    return {"status": "OK"}


@router.get(
    "/health_check",
    tags=["Manage"],
    operation_id="health_check",
    summary="Health check",
    response_model=BaseEmptyResponse,
)
async def api_health_check():
    return {"status": "OK"}


@router.get(
    "/version",
    tags=["Manage"],
    operation_id="get_version",
    summary="Get application version",
    response_model=BaseDataResponse,
)
async def api_version():
    return BaseDataResponse(data={"version": CONFIG.VERSION})


# add_manage_routes(CONFIG.WEB_ROUTE_PREFIX)
# add_assistant_routes(CONFIG.WEB_ROUTE_PREFIX)
