from typing import cast

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message, Update
from dishka.integrations.aiogram import FromDishka, inject
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.enums import UserLanguages
from src.core.queries import user_auth, user_languages


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


class isNotLanguageSelected(Filter):
    """
    Checks if user have selected the language.
    """

    @inject
    async def __call__(self, update: Update, session: FromDishka[AsyncSession]) -> bool:
        if isinstance(update, CallbackQuery):
            chat_id = update.from_user.id
        elif isinstance(update, Message):
            chat_id = update.from_user.id  # type: ignore        
        else:
            raise ValueError("Unhandled message action detected")
        
        return not await user_languages.exists(
            user_languages.p.ExistsDTO(chat_id=chat_id),
            session=session
        )


is_authenticated = IsAuthenticated()
is_language_message = IsLanguageMessage()
is_not_langauge_selected = isNotLanguageSelected()
