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
    

def language_setup_complete(language: str) -> str:
    return _(
        "Bot language has been changed to: {language}"
    )


def auth_request() -> str:
    return _(
        "Please choose <b>Sign In</b> if you already have an account, "
        "or <b>Sign Up</b> to create one."
    )


def signin_start() -> str:
    return _(
        "Ok, To <b>SignIn</b> your account, please provide " \
        "some credentials of your account..."
    )


def signup_start() -> str:
    return _(
        "Ok, To <b>SignUp</b> your account, please provide " \
        "some credentials of your account..."
    )


def username_request() -> str:
    return _(
        "Please, enter your account <b>username</b>."
    )


def password_request() -> str:
    return _(
        "Please, enter your account <b>password</b>."
    )

# def signin_failed() -> str:
#     return _(
#         "<b>Sign In</b> failed, invalid username or password. "
#         "Please check your credentials and try again."
#     )
