"""
Internationalization (i18n) utilities for the bot.

This module sets up the aiogram-i18n system, providing:
- A preconfigured `I18n` instance.
- Shorthand translation functions for immediate (`gettext`) and lazy (`gettext_lazy`) translations.
- An `I18nMiddleware` instance for dynamic language switching.

Exposed constants and objects:
- I18N_DOMAIN: Default translation domain ("messages").
- i18n: Configured `I18n` instance.
- gettext: Immediate translation function.
- gettext_lazy: Lazy translation function.
- i18n_middleware: Middleware for managing user language preferences.
"""

from aiogram.utils.i18n import I18n

from src.bot.middlewares.i18n_middleware import I18nMiddleware
from src.config.settings import LOCALE_DIR

__all__ = [
    "gettext",
    "gettext_lazy",
    "i18n"
]

# Default translation domain
I18N_DOMAIN = "messages"

# Initialize the I18n instance with the locale directory and default locale
i18n = I18n(path=LOCALE_DIR, default_locale="en", domain=I18N_DOMAIN)

# Shorthand functions for text translation
gettext = i18n.gettext  # Immediate translation
gettext_lazy = i18n.lazy_gettext  # Lazy translation (evaluated later)

# Middleware for handling dynamic translation switching
i18n_middleware = I18nMiddleware(i18n)
