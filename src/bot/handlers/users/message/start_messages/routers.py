from aiogram import Router

from .click_messages import router as click_messages_router
from .text import router as text_router

router = Router()

router.include_routers(
    click_messages_router,
    text_router,
)
