from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.utils.i18n import gettext as _
from src.config.settings import LANGUAGES
from src.core.domain_schema.settings import UserLanguage


def language_select(languages: tuple[UserLanguage, ...] = LANGUAGES) -> InlineKeyboardMarkup:    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{language.flag} {language.code.value}", 
                    callback_data=language.code.value
                )
                for language in languages
            ]
        ]
    )


def auth_methods_select() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("SignIn"), callback_data="signin"),
                InlineKeyboardButton(text=_("SignUp"), callback_data="signup"),
            ],
        ]
    )


def auth_signin_switch() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("I have an account: SignIn"), 
                    callback_data="signin"
                )
            ]
        ]
    )


def auth_signup_switch() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_("I don't have an account: SignUp"), 
                    callback_data="signup"
                )
            ]
        ]
    )
