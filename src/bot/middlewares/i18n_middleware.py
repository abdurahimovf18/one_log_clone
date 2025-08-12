"""
This file declares I18n middleware to use according to aiogram 3.x I18n
docs: https://docs.aiogram.dev/en/latest/utils/i18n.html#aiogram.utils.i18n.middleware.I18nMiddleware.setup
"""

from collections.abc import Awaitable, Callable

from aiogram import BaseMiddleware, Router
from aiogram.types import TelegramObject, Update
from aiogram.utils.i18n.core import I18n

from src.config.settings import DEFAULT_LANGUAGE
from src.core.queries import user_languages
from src.infrastructure.database import session_factory


class I18nMiddleware(BaseMiddleware):
    """
    Abstract I18n middleware.
    """
    def __init__(
        self,
        i18n: I18n,
        i18n_key: str | None = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        """
        Create an instance of middleware

        :param i18n: instance of I18n
        :param i18n_key: context key for I18n instance
        :param middleware_key: context key for this middleware
        """
        self.i18n = i18n
        self.i18n_key = i18n_key
        self.middleware_key = middleware_key

    async def get_locale(self, event: Update, data: dict[str, object]) -> str:  # noqa: ARG002
        if event.callback_query:
            chat_id = event.callback_query.from_user.id
        elif event.message:
            chat_id = event.message.from_user.id  # type: ignore
        else:
            raise ValueError(f"Unsupported event detected on {type(self).__name__}")

        async with session_factory() as session:
            user_language = await user_languages.get_by_chat_id(
                user_languages.p.GetByChatIdDTO(chat_id=chat_id), session=session
            )

            if user_language is None:
                return DEFAULT_LANGUAGE.value
            
            return user_language.language.value
    
    def setup(
        self: BaseMiddleware, router: Router, exclude: set[str] | None = None
    ) -> BaseMiddleware:
        """
        Register middleware for all events in the Router

        :param router:
        :param exclude:
        :return:
        """
        if exclude is None:
            exclude = set()
        exclude_events = {"update", *exclude}
        for event_name, observer in router.observers.items():
            if event_name in exclude_events:
                continue
            observer.outer_middleware(self)
        return self
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]],
        event: TelegramObject,
        data: dict[str, object],
    ) -> object:
        
        current_locale = await self.get_locale(event=event, data=data) or self.i18n.default_locale  # type: ignore

        if self.i18n_key:
            data[self.i18n_key] = self.i18n
        if self.middleware_key:
            data[self.middleware_key] = self

        with self.i18n.context(), self.i18n.use_locale(current_locale):
            return await handler(event, data)
        