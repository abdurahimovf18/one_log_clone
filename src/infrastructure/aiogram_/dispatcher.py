from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage


def create_dispatcher(
    storage: BaseStorage,
    *args: object,
    **kwargs: object,
) -> Dispatcher:
    
    return Dispatcher(
        *args,
        storage=storage,
        **kwargs
    )
