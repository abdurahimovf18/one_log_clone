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
    

class Feedback(StatesGroup):
    accept = State()


class Language(StatesGroup):
    select = State()


class SendMessage(StatesGroup):
    menu = State()
    