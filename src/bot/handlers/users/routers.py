from aiogram import Router

from .message.routers import router as messages_router

router = Router(name="users_router")
router.include_router(messages_router)
