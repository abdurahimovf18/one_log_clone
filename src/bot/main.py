import asyncio
import logging
import logging.config

import uvloop

import src.bot.loader  # type: ignore  # noqa: F401
from src.bot.infrastructure import bot, dp
from src.config.settings import LOGGING_CONFIG


async def main():
    await dp.start_polling(bot)  # type: ignore


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    logging.config.dictConfig(LOGGING_CONFIG)
    asyncio.run(main())

