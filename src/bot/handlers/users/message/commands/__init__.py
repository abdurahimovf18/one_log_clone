from aiogram import Router

from .start import router as start_router

router = Router(name="commands")
router.include_router(start_router)
