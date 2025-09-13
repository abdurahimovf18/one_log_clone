from src.core.exceptions.common import Forbidden, NoAction, ObjectNotFound


class UsernameNotFound(ObjectNotFound): 
    msg = "User at this username not found."


class PasswordIncorrect(Forbidden): 
    msg = "Username is found, but password verification failed."


class UserAlreadyLoggined(NoAction):
    msg = "User is already logged in."


class UsernameIsTaken(Forbidden):
    msg = "This username is already in use."
    