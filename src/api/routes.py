from fastapi import APIRouter
from api.v1 import (
    assistant_router,
    knowledge_router,
    chat_router,
    message_router,
    manage_router,
    tool_router
)

router = APIRouter()

router.include_router(router=manage_router)  # 管理API
router.include_router(router=knowledge_router, prefix="/knowledge")  # 知识库管理 API
router.include_router(router=assistant_router, prefix="/assistant")  # 助手API
router.include_router(router=chat_router, prefix="/chat")  # 聊天API
router.include_router(router=message_router, prefix="/message")  # 消息API
router.include_router(router=tool_router, prefix="/tool")  # 工具API
