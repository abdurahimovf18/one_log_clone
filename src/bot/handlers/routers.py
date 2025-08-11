from aiogram import Router

from .users.routers import router as users_router

base_router = Router(name="base_router")
base_router.include_router(users_router)
