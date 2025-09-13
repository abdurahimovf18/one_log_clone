from aiolimiter import AsyncLimiter
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession
from src.bot.providers.current_user_provider import CurrentUserDTO


__all__ = [
    "SendRateLimiter",
    "db_session",
    "current_user"
]

db_session = FromDishka[AsyncSession]
SendRateLimiter = AsyncLimiter
current_user = FromDishka[CurrentUserDTO | None]
