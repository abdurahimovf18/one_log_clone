from aiogram import Router

from .auth import router as auth_router
from .commands import router as commands_router
from .feedbacks import router as feedbacks_router
from .start_messages.routers import router as start_messages_routers

router = Router(name="user_message")

router.include_routers(
    commands_router,
    auth_router,
    feedbacks_router,
    start_messages_routers,
)
