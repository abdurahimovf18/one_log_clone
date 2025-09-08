from collections.abc import Awaitable, Callable
from typing import cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from aiolimiter import AsyncLimiter
from redis.asyncio import Redis

from src.bot.utils.i18n import gettext as _


class ThrottlingObject:
    def __init__(self, redis: Redis, key: str,) -> None:
        self.redis = redis
        self.key = key

    async def get_value(self) -> int:
        result = await self.redis.get(self.name)
        if result is None:
            return 0
        return int.from_bytes(result, byteorder="big")
    
    async def set_value(self, new_value: int, ex: int) -> None:
        await self.redis.set(self.name, value=new_value, ex=ex)

    @property
    def name(self) -> str:
        return f"throttling_object[{self.key}]"


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, rate: int = 3, time_period: int = 1) -> None:
        """
        A middleware that limits RPS of the users.

        Params:
            rate (int): this value is how much requests in the 
                        x time period users can send to the bot
            time_period (float): this is the time period in seconds.       
            redis: (redis.asyncio.Redis): A Redis instance 
        """
        self.rate = rate
        self.time_period = time_period
        self.redis = redis

    async def __call__(
            self, 
            handler: Callable[[TelegramObject, dict[str, object]], Awaitable[object]], 
            event: TelegramObject, 
            data: dict[str, object]
            ) -> object:
        
        throttling_obj = ThrottlingObject(
            redis=self.redis,
            key=self._generate_key_by_event(event=event)  # type: ignore
        )

        value = await throttling_obj.get_value()
        await throttling_obj.set_value(value + 1, ex=self.time_period)

        if value + 1 > self.rate:
            await self.reject_handler(event, data)  # type: ignore
        else:
            await handler(event, data)

    def _generate_key_by_event(self, event: Update) -> str:
        if src := event.callback_query or event.message or event.inline_query:
            return str(src.from_user.id)  # type: ignore
        else:
            raise ValueError(f"Event Type is unsupported, {event=}")
        
    def _get_message_limiter_by_data(self, data: dict[str, object]) -> AsyncLimiter:
        limiter = cast(AsyncLimiter | None, data.get("send_rate_limiter"))
        if limiter is None:
            raise RuntimeError(
                "send_rate_limiter should be registered to the dispatcher as a context manager."
            )
        return limiter
    
    async def reject_handler(self, event: Update, data: dict[str, object]) -> None:
        limiter = self._get_message_limiter_by_data(data=data)
        text = _("Too much requests sent, Please slow down...")

        async with limiter:
            if msg := event.message or event.callback_query:
                await msg.answer(text=text)
            elif event.inline_query: 
                await event.inline_query.answer(
                    [], 
                    switch_pm_text=text, 
                    switch_pm_parameter="rate_limit"
                )
            else:
                raise ValueError(f"Event Type is unsupported, {event=}")
   