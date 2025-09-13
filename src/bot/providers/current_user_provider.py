from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession
from src.core.data_transfer_objects.base import BaseDTO
from src.core.domain_schema.models import TgUser

from aiogram.types import TelegramObject
from dishka import Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData, AiogramProvider

from src.core import queries
from src.bot.utils.misc import get_update_user_id

from src.infrastructure.database import session_factory


class CurrentUserDTO(BaseDTO):
    id: TgUser.user_id


class CurrentUserProvider(AiogramProvider):

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self, event: TelegramObject, session: AsyncSession
        ) -> CurrentUserDTO | None:
        """
        A function that returns current user
        """
        
        user_id = cast(int, get_update_user_id(event, raise_exc=True))  # type: ignore            
        user_info = await queries.tg_users.get_user_id_by_chat_id(
            queries.tg_users.p.GetUserIdByChatIdDTO(chat_id=user_id), session=session
        )
        if user_info is None or user_info.user_id is None:
            return None
        return CurrentUserDTO(id=user_info.user_id)

