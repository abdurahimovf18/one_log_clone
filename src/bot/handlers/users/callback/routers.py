from aiogram import Router

from .auth import router as auth_router

router = Router(name="user_callback_router")

router.include_router(auth_router)
