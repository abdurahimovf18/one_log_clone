from aiogram import Router

from .commands import router as commands_router

router = Router(name="user_message")
router.include_router(commands_router)
