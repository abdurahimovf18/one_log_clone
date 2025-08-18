from aiogram.types import InlineKeyboardButton

from src.bot.utils.i18n import gettext as _


def back_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text=_("⬅️ Back"), callback_data="back")
