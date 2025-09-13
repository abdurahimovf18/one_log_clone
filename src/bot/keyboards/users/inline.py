from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.utils.i18n import gettext as _
from src.config.settings import LANGUAGES
from src.core.domain_schema.settings import UserLanguage
from src.bot.keyboards.shared import back_button


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


def message_menu(
        accounts_set: bool = False,
        message_set: bool = False,
        groups_set: bool = False,
        interval_set: bool = False,
        duration_set: bool = False,
        allow_start: bool = False,
) -> InlineKeyboardMarkup:
    
    status_text = {
        "accounts": {
            True: _("✔️ Accounts Set"), False: _("Set Accounts ↗️")
        },
        "message": {
            True: _("✔️ Message Set"), False: _("Set Message ↗️"),
        },
        "groups": {
            True: _("✔️ Groups Set"), False: _("Set Groups ↗️"),  
        },
        "interval": {
            True: _("✔️ Interval Set"), False: _("Set Message ↗️"),
        },
        "duration": {
            True: _("✔️ Duration Set"), False: _("Set Message ↗️"),
        },
        "start": {
            True: _("✔️ Start Mailing"), False: _("🚫 Start Mailing"),
        }
    }

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=status_text["accounts"][accounts_set], callback_data="accounts"
            )],
            [InlineKeyboardButton(
                text=status_text["message"][message_set], callback_data="message"
            )],
            [InlineKeyboardButton(
                text=status_text["groups"][groups_set], callback_data="groups"    
            )],
            [InlineKeyboardButton(
                text=status_text["interval"][interval_set], callback_data="interval"    
            )],
            [InlineKeyboardButton(
                text=status_text["duration"][duration_set], callback_data="duration"    
            )],
            [InlineKeyboardButton(
                text=status_text["start"][allow_start], callback_data="start"    
            )],
            [back_button()]
        ]
    )
