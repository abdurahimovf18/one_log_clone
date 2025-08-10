from src.config.settings import env
from src.infrastructure import aiogram_

bot = aiogram_.create_bot(token=env.BOT_TOKEN)
dp = aiogram_.create_dispatcher()

