from aiogram import Router

from .feedback import router as feedback_router
from .language import router as language_router
from .start import router as start_router

router = Router(name="commands")
router.include_routers(
    start_router,
    feedback_router,
    language_router,
)
