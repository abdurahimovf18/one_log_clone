from src.bot.utils.i18n import gettext as _


def greet_new_user() -> str:
    return _("Hi there!, Welcome to the bot.")


def greet_old_user() -> str:
    return _("Hi there!, What we gonna start with today?")


def request_for_language_select() -> str:
    return """
🇺🇿 Quyidagi roʻyxatdan oʻzingizga yoqqan tilni tanlang.
🇺🇸 Please select your preferred language from the list below.
🇷🇺 Пожалуйста, выберите предпочитаемый вами язык из списка ниже.
"""
    




# def auth_request() -> str:
#     return _(
#         "Before using the bot, Please <b>Sign In</b> or "
#         "<b>Sign Up</b> first."
#     )


# def language_request() -> str:
#     return _(
#         "Please, Select the language, which you're "
#         "comfortable with from options below..."
#     )


# def auth_method_select() -> str:
#     return _(
#         "Please choose <b>Sign In</b> if you already have an account, "
#         "or <b>Sign Up</b> to create one."
#     )


# def signin_request() -> str:
#     return _(
#         "Please provide your account details to continue with <b>Sign In</b>."
#     )


# def signup_request() -> str:
#     return _(
#         "Please provide a new account info to continue with <b>Sign Up</b>."
#     )


# def username_request() -> str:
#     return _(
#         "Please, enter your account <b>username</b>."
#     )


# def password_request() -> str:
#     return _(
#         "Please, enter your account <b>password</b>."
#     )

# def signin_failed() -> str:
#     return _(
#         "<b>Sign In</b> failed, invalid username or password. "
#         "Please check your credentials and try again."
#     )
