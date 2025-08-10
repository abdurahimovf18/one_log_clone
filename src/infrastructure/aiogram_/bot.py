from aiogram import Bot


def create_bot(
    token: str,
    *args: object,
    **kwargs: object
) -> Bot:

    return Bot(
        *args,
        token=token,
        **kwargs
    )
