from aiogram import Router

from .click_settings import router as click_settings_router
from .message_settings import router as message_settings_router

router = Router()

router.include_routers(
    click_settings_router,
    message_settings_router,
)