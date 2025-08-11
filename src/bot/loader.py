from src.bot.handlers.routers import base_router
from src.bot.providers.database_session_provider import (
    register_provider as register_database_session_provider,
)
from src.config.settings import env
from src.infrastructure import aiogram_

bot = aiogram_.create_bot(token=env.BOT_TOKEN)
dp = aiogram_.create_dispatcher()

# === Including Routers === #
dp.include_router(base_router)

# === Register Providers === #
register_database_session_provider(dp)

# === Registering Middlewares === #

