from aiogram import Router

from .click_messages import router as click_messages_router

router = Router()

router.include_routers(
    click_messages_router,
)
