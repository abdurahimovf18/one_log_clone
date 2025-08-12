from typing import cast

from aiogram.filters import Filter
from aiogram.types import Update
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.queries import user_auth


class IsAuthenticated(Filter):
    """
    Checks if the user is authenticated, using relationships of UserAuth.
    """

    @inject
    async def __call__(self, update: Update, session: FromDishka[AsyncSession]) -> bool:
        chat_id = cast(int, update.from_user.id)  # type: ignore

        return await user_auth.exists(
            user_auth.p.ExistsDTO(chat_id=chat_id), session=session
        )


is_authenticated = IsAuthenticated()
