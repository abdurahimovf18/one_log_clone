from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.keyboards.shared import back_button
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
            True: _("✔️ Interval Set"), False: _("Set Interval ↗️"),
        },
        "duration": {
            True: _("✔️ Duration Set"), False: _("Set Duration ↗️"),
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


def pagination(page: int, pages_count: int, items: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    keyboard.append(
        [InlineKeyboardButton(text=key, callback_data=value) for key, value in items.items()]
    )

    if page > 1 or page < pages_count:
        prev_text = "◀️" if page > 1 else "🚫"
        next_text = "▶️" if page < pages_count else "🚫"
        page_text = f"{page}/{pages_count}"

        keyboard.append([
            InlineKeyboardButton(text=prev_text, callback_data=f"{page - 1}"),
            InlineKeyboardButton(text=page_text, callback_data="current_page"),
            InlineKeyboardButton(text=next_text, callback_data=f"{page + 1}")
        ])

    keyboard.append([back_button()])

    return InlineKeyboardMarkup(
        inline_keyboard=[*keyboard]
    )


def info_not_found(show_add_btn: bool = False) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    if show_add_btn:
        keyboard.append([InlineKeyboardButton(text=_("Add One ↗️"), callback_data="add")])

    return InlineKeyboardMarkup(
        inline_keyboard=[
            *keyboard,
            [back_button()]
        ]
    )


def back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[back_button()]])


def time_choice(choices: dict[str, str], chosen: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            *[
                [InlineKeyboardButton(
                    text=f"✔️ {key}" if value == chosen else key, callback_data=value
                )]
                for key, value in choices.items()
            ],
            [back_button()]
        ]
    )


def message_settings() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("📞 Accounts"), callback_data="accounts")],
            [InlineKeyboardButton(text=_("👥 Groups"), callback_data="groups")],
            [back_button()]
        ]
    )


def settings_pagination(
        page: int, 
        pages_count: int, 
        items: dict[str, str],
        selected_items: set[str],
) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    is_page_selected = True

    for label, callback in items.items():
        if callback in selected_items:
            label = f"✅ {label}"
        else:
            is_page_selected = False

        keyboard.append([InlineKeyboardButton(text=label, callback_data=callback)])  
        
    if page > 1 or page < pages_count:
        prev_text = "◀️" if page > 1 else "🚫"
        next_text = "▶️" if page < pages_count else "🚫"
        page_text = f"{page}/{pages_count}"

        keyboard.append([
            InlineKeyboardButton(text=prev_text, callback_data=f"{page - 1}"),
            InlineKeyboardButton(text=page_text, callback_data="current_page"),
            InlineKeyboardButton(text=next_text, callback_data=f"{page + 1}")
        ])

    select_text = _("✅ Select Page") if is_page_selected else _("✔️ Select Page")

    keyboard.append([
        InlineKeyboardButton(text=select_text, callback_data="select",),
        InlineKeyboardButton(text=_("🔽 Action"), callback_data="action")
    ])

    keyboard.append([
        InlineKeyboardButton(text=_("➕ Add new"), callback_data="add"),  # noqa: RUF001
    ])

    keyboard.append([back_button()])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def settings_actions() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("✅ Activate All"), callback_data="activate_items"),
                InlineKeyboardButton(text=_("✔️ Deactivate All"), callback_data="deactivate_items"),
                InlineKeyboardButton(text=_("🗑 Delete All"), callback_data="delete_items"),
            ],
            [back_button()]
        ]
    )


def delete_confirm() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Yes, Delete all")),
            ],
            [
                InlineKeyboardButton(text=_("⬅️ No, Go Back")),
            ]
        ]
    )


def delete_confirm_final() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("❌ Yes, I'm 100% sure.")),
            ],
            [back_button()]
        ]
    )
