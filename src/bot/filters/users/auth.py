from typing import cast

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message, Update
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain_schema.settings import UserLanguages
from src.core.queries import tg_users


class HasUserTgAccount(Filter):
    """
    Checks if the user has already used this bot before
    """

    @inject
    async def __call__(self, update: Update, session: FromDishka[AsyncSession]) -> bool:
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
        if isinstance(update, CallbackQuery):
            text = cast(str, update.data)
        elif isinstance(update, Message):
            text = cast(str, update.text)         
        else:
            raise ValueError("Unhandled message action detected")
        
        return getattr(UserLanguages, text, None) is not None


# class isNotLanguageSelected(Filter):
#     """
#     Checks if user have selected the language.
#     """

#     @inject
#     async def __call__(self, update: Update, session: FromDishka[AsyncSession]) -> bool:
#         if isinstance(update, CallbackQuery):
#             chat_id = update.from_user.id
#         elif isinstance(update, Message):
#             chat_id = update.from_user.id  # type: ignore        
#         else:
#             raise ValueError("Unhandled message action detected")
        
#         return not await tg_users.exists(
#             tg_users.p.ExistsDTO(chat_id=chat_id),
#             session=session
#         )


is_language_message = IsLanguageMessage()
# is_not_langauge_selected = isNotLanguageSelected()
is_authenticated = IsAuthenticated()
has_user_tg_account = HasUserTgAccount()
