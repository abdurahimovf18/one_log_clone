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


class NewMessage(StatesGroup):
    menu = State()
    

class NewMessageAccount(StatesGroup):
    menu = State()


class NewMessageGroup(StatesGroup):
    menu = State()


class NewMessageInterval(StatesGroup):
    menu = State()


class NewMessageDuration(StatesGroup):
    menu = State()


class NewMessageText(StatesGroup):
    menu = State()


class NewMessageStart(StatesGroup):
    menu = State()
    

class Settings(StatesGroup):
    menu = State()


class MessageSettings(StatesGroup):
    menu = State()


class MessageAccountSettings(StatesGroup):
    menu = State()


class MessageGroupSettings(StatesGroup):
    menu = State()


