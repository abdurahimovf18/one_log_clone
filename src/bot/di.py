from aiolimiter import AsyncLimiter
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = [
    "SendRateLimiter",
    "db_session",
]

db_session = FromDishka[AsyncSession]
SendRateLimiter = AsyncLimiter
