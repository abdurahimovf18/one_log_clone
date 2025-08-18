

class ExceptionEngine(BaseException):
    msg: str = ""

    def __init__(self, msg: str | None = None, *args: object) -> None:
        super().__init__(msg or self.msg, *args)


class AppException(BaseException): ...
