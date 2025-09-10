from src.bot.utils.i18n import gettext as _


def language_select(language: str) -> str:
    return _(
        "Please select your preferred language from " 
        "the list below. Current language is <b>{language}</b>"
    ).format(language=language)
