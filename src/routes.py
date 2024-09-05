from fastapi import APIRouter
from assistant import assistant_router
from manage import manage_router
from models.assistant import assistant_model
from database.sqlite.connection import engine
from chat.routes import router as chat_router
from knowledge.routes import router as knowledge_router
from message.routes import router as message_router


# 创建数据库
assistant_model.Base.metadata.create_all(bind=engine)

router = APIRouter()

router.include_router(router=manage_router)  # 管理API
router.include_router(knowledge_router, prefix="/knowledge")  # 知识库管理 API
router.include_router(router=assistant_router, prefix="/assistant")  # 助手API
router.include_router(router=chat_router, prefix="/chat")  # 聊天API
router.include_router(router=message_router, prefix="/message")  # 消息API
