from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode


def create_bot(
    token: str,
    default: DefaultBotProperties | None = None,
    *args: object,
    **kwargs: object
) -> Bot:
    """
    Create a infrastructure object with internal defaults.

    Defaults:
        default: aiogram.client.default.DefaultBotProperties

    Returns:
        aiogram.Bot  
    """

    default = default or DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        disable_notification=False,
    )

    return Bot(
        *args,
        token=token,
        default=default,
        **kwargs
    )
