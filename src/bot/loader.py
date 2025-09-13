import logging

from aiolimiter import AsyncLimiter

from src.bot.handlers.routers import base_router
from src.bot.infrastructure import bot, dp, redis
from src.bot.middlewares.throttling_middleware import ThrottlingMiddleware
from src.bot.providers import register_providers
from src.bot.utils.bot import setup_bot_commands
from src.bot.utils.i18n import i18n_middleware
from src.config.settings import BOT_COMMANDS, BOT_THROTTLING_PER_SECOND, MESSAGE_RATE_PER_SECOND

logger = logging.getLogger(__name__)


async def startup():
    # === Bot Commands === #
    await setup_bot_commands(bot=bot, commands=BOT_COMMANDS)

    # === Middlewares === #
    logger.debug("Registering i18n middleware")
    dp.update.middleware(i18n_middleware)
    logger.info("i18n middleware registered")

    logger.debug("Registering i18n middleware")
    dp.update.middleware(ThrottlingMiddleware(
        redis=redis, 
        rate=BOT_THROTTLING_PER_SECOND, 
        time_period=1
    ))
    logger.info("i18n middleware registered")

    # === Providers === #
    logger.debug("Registering providers from dishka")
    register_providers(dp)
    logger.info("Providers are registered")

    # === Dependencies === #
    logger.debug("Registering AsyncLimiter as Dependency")
    dp["send_rate_limiter"] = AsyncLimiter(max_rate=MESSAGE_RATE_PER_SECOND, time_period=1)
    logger.info("AioLimiter has been registered")

    # === Routers === #
    logger.debug("Including routers into dispatcher")
    dp.include_router(base_router)
    logger.info("Routers included")


async def shutdown():
    pass


dp.startup.register(startup)
dp.shutdown.register(shutdown)
