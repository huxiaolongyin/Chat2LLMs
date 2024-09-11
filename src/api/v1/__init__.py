from .assistant import router as assistant_router
from .document import router as knowledge_router
from .chat import router as chat_router
from .message import router as message_router
from .manage import router as manage_router

__all__ = [
    "assistant_router",
    "knowledge_router",
    "chat_router",
    "message_router",
    "manage_router",
]
