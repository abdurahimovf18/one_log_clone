from aiogram import Router
from .languages import router as languages_router
from .auth import router as auth_router

router = Router(name="user_callback_router")

router.include_routers(
    languages_router,
    auth_router,
)
