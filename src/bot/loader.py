import logging

from src.bot.handlers.routers import base_router
from src.bot.providers.database_session_provider import (
    register_provider as register_database_session_provider,
)
from src.bot.utils.i18n import i18n_middleware
from src.config.settings import env
from src.infrastructure import aiogram_

logger = logging.getLogger(__name__)

# === Step 1: Bot & Dispatcher === #
logger.debug("Initializing Bot and Dispatcher")
bot = aiogram_.create_bot(token=env.BOT_TOKEN)
dp = aiogram_.create_dispatcher()
logger.info(
    "Bot and Dispatcher initialized successfully", 
    extra={"bot_token_set": bool(env.BOT_TOKEN)}
)


async def startup():
    # === Middlewares === #
    logger.debug("Registering i18n middleware")
    dp.update.middleware(i18n_middleware)
    logger.info("i18n middleware registered")

    # === Providers === #
    logger.debug("Registering database session provider")
    register_database_session_provider(dp)
    logger.info("Database session provider registered")

    # === Routers === #
    logger.debug("Including routers into dispatcher")
    dp.include_router(base_router)
    logger.info("Routers included")


async def shutdown():
    pass


dp.startup.register(startup)
dp.shutdown.register(shutdown)
