from aiogram import Router

from .accounts import router as accounts_router
from .common import router as common_router
from .text import router as text_router

router = Router()

router.include_routers(
    common_router,
    accounts_router,
    text_router,
)

