from fastapi import APIRouter
from api.v1 import (
    assistant_router,
    knowledge_router,
    chat_router,
    message_router,
    manage_router,
)
# from models.assistant import Base
# from core.database import sqlite_connection


# # 创建数据库
# assistant.Base.metadata.create_all(bind=sqlite_connection.engine)

router = APIRouter()

router.include_router(router=manage_router)  # 管理API
router.include_router(router=knowledge_router, prefix="/knowledge")  # 知识库管理 API
router.include_router(router=assistant_router, prefix="/assistant")  # 助手API
router.include_router(router=chat_router, prefix="/chat")  # 聊天API
router.include_router(router=message_router, prefix="/message")  # 消息API
