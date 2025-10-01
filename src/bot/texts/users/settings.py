from src.bot.utils.i18n import gettext as _


def settings_info() -> str:
    return _(
        "⚙️ Settings — manage your bot account data, message " 
        "preferences, Telegram accounts, and groups here."
    )


def message_settings_info() -> str:
    return _(
        "💬 Message Settings — manage how messages are sent from your accounts."
    )


def message_group_settings_info() -> str:
    return _(
        "👥 Manage your groups attached to your account by selecting its username " 
        "and choosing the action."
    )
