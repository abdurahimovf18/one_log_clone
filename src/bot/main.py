import asyncio
import logging
import logging.config

import uvloop

from src.config.settings import LOGGING_CONFIG

from .loader import bot, dp

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def main():
    await dp.start_polling(bot)  # type: ignore


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    asyncio.run(main())

