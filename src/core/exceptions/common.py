from src.core.exceptions.base import AppException

__all__ = [
    "Forbidden",
    "ObjectNotFound",
    "ValidationError",
]


# An exception raised when some object is not found
class ObjectNotFound(AppException): ...


# An exception for validation exception 
class ValidationError(AppException): ...


# An exception responsible for forbidding access
class Forbidden(AppException): ...


# An exception for cases when No Action is needed, e.g. UserAlreadyAuthenticated
class NoAction(AppException): ...


# An exception when an exception is related to developers typo or tests rather than business logic
class Development(AppException): ...
