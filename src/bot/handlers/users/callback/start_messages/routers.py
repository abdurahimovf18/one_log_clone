from aiogram import Router

from .accounts import router as accounts_router
from .common import router as common_router
from .duration import router as duration_router
from .groups import router as groups_router
from .interval import router as interval_router
from .text import router as text_router

router = Router()

router.include_routers(
    common_router,
    accounts_router,
    text_router,
    groups_router,
    interval_router,
    duration_router,
)

