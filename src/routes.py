from fastapi import APIRouter
from assistant import assistant_router
from manage import manage_router
from models.assistant import assistant_model
from database.sqlite.connection import engine

# 创建数据库
assistant_model.Base.metadata.create_all(bind=engine)
router = APIRouter()

router.include_router(router=manage_router, prefix="/manange")  # 管理API
router.include_router(router=assistant_router, prefix="/assistant")  # 助手API
