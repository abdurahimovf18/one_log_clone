from aiogram import Router

from .callback.routers import router as callback_router
from .message.routers import router as messages_router

router = Router(name="users_router")

router.include_router(messages_router)
router.include_router(callback_router)
