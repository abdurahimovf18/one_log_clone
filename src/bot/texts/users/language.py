from src.bot.utils.i18n import gettext as _


def language_select(language: str) -> str:
    return _(
        "Please select your preferred language from " 
        "the list below. Current language is <b>{language}</b>"
    ).format(language=language)


def old_language_selected(language: str) -> str:
    return _(
        "⬅️ Returning to the main menu. " 
        "No changes were made — your current " 
        "language is still <b>{language}</b>."
    ).format(language=language)


def set_new_language(new_language: str, old_language: str) -> str:
    return _(
        "⬅️ Returning to the main menu. "
        "Language updated: <b><s>{old_language}</s></b> → <b>{new_language}</b>."
    ).format(old_language=old_language, new_language=new_language)
