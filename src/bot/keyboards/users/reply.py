from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from src.bot.utils.i18n import gettext as _


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("♻️ Send Message")),
                KeyboardButton(text=_("🗂 Messages History")),
            ],
            [
                KeyboardButton(text=_("✍️ Leave Feedback")),
                KeyboardButton(text=_("⚙️ Settings"))
            ]
        ]
    )


def back() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=_("⬅️ Back"))]
        ]
    )


def settings() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=_("💬 Message Settings")),
                KeyboardButton(text=_("👤 Manage Account"))
            ],
            [KeyboardButton(text=_("⬅️ Back"))]
        ]
    )
