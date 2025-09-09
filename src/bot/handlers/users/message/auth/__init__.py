from aiogram import Router

from .signin import router as signin_router
# from .signup import router as signup_router

router = Router(name="commands")

router.include_router(signin_router)
# router.include_router(signup_router)