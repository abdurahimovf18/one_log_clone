from typing import Literal, cast

from aiogram.filters import Filter
from aiogram.types import Update
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot import di
from src.bot.utils.misc import get_update_text
from src.core.domain_schema.settings import UserLanguages
from src.core.queries import tg_users


class HasUserTgAccount(Filter):
    """
    Checks if the user has already used this bot before
    """

    @inject
    async def __call__(self, update: Update, session: di.db_session) -> bool:
        user_id = cast(int, update.from_user.id)  # type: ignore

        return await tg_users.exists_by_chat_id(
            tg_users.p.ExistsByChatIdDTO(chat_id=user_id), session=session
        )


class IsAuthenticated(Filter):
    """
    Checks if the user is authenticated.
    """

    @inject
    async def __call__(self, update: Update, session: FromDishka[AsyncSession]) -> bool:
        chat_id = cast(int, update.from_user.id)  # type: ignore

        response = await tg_users.get_user_id_by_chat_id(
            tg_users.p.GetUserIdByChatIdDTO(chat_id=chat_id), session=session
        )
        if response is None or response.user_id is None:
            return False
        return True


class IsLanguageMessage(Filter):
    """
    Checks if the callback_query.data/message.text is in the list of language code, 
    which the application supports
    """

    async def __call__(self, update: Update) -> bool:
        text = cast(str, get_update_text(update, raise_exc=True))
        language = getattr(UserLanguages, text, None)
        return language is not None
    

class IsAuthMethod(Filter):
    def __init__(self, method: Literal["all", "signin", "signup"]) -> None:
        self.method = method
        self.lookup_methods = {
            "all": {"signin", "signup"},
            "signin": {"signin", },
            "signup": {"signup", },
        }

    async def __call__(self, update: Update) -> bool:
        text = cast(str, get_update_text(update, raise_exc=True))
        return text in self.lookup_methods[self.method]
    

is_any_auth_method = IsAuthMethod(method="all")
is_language_message = IsLanguageMessage()
is_authenticated = IsAuthenticated()
has_user_tg_account = HasUserTgAccount()
