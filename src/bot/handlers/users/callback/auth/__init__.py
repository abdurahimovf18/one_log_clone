from aiogram import Router

# from .authentication import router as auth_router
from .language import router as language_router

router = Router(name="user_auth")

# router.include_router(auth_router)
router.include_router(language_router)
