from aiolimiter import AsyncLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from dishka.integrations.aiogram import FromDishka


__all__ = [
    "db_session",
    "SendRateLimiter",
]

db_session = FromDishka[AsyncSession]
SendRateLimiter = AsyncLimiter
