from aiogram import Router

# from .common import router as common_router
from .message_settings import router as message_settings_router

router = Router()


router.include_routers(
    message_settings_router,
)