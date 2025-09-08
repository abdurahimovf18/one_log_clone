import logging

from src.config.settings import env
from src.infrastructure import aiogram_, redis_

logger = logging.getLogger(__name__)

# ===== REDIS ===== #
logger.debug("Initializing Redis")
redis = redis_.create_instance(
    host=env.REDIS_HOST,
    port=env.REDIS_PORT,
    db=env.REDIS_DB,
    password=env.REDIS_PASSWORD
)
logger.debug(
    "Bot has been initialized successfully...",
    extra={"Password Set": bool(env.REDIS_PASSWORD)}    
)

# ===== BOT ===== #
logger.debug("Initializing Bot")
bot = aiogram_.create_bot(token=env.BOT_TOKEN)
logger.info(
    "Bot has been initialized successfully...",
    extra={"bot_token_set": bool(env.BOT_TOKEN)}
)

# ===== DISPATCHER ===== #
logger.debug("Initializing Dispatcher")
dp = aiogram_.create_dispatcher()
logger.info(
    "Dispatcher has been initialized successfully", 
)
