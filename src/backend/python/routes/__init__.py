from .session import router as session_router
from .chat import router as chat_router

routes = [
    session_router,
    chat_router
]