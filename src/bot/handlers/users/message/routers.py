from aiogram import Router

from .auth import router as auth_router
from .commands import router as commands_router

router = Router(name="user_message")

router.include_router(commands_router)
router.include_router(auth_router)
