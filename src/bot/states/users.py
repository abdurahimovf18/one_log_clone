from aiogram.fsm.state import State, StatesGroup


class TgUserAuth(StatesGroup):
    language_select = State()


class Auth(StatesGroup):
    select_method = State()


class SignIn(StatesGroup):
    username = State()
    password = State()


class SignUp(StatesGroup):
    username = State()
    password = State()
    