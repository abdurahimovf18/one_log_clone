from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage


def create_dispatcher(
    *args: object,
    storage: BaseStorage | None = None,
    **kwargs: object,
) -> Dispatcher:
    """
    Create a infrastructure object with internal defaults.

    Defaults:
        storage: aiogram.fsm.storage.memory.MemoryStorage

    Returns:
        aiogram.Dispatcher  
    """
    storage = storage or MemoryStorage()

    return Dispatcher(
        *args,
        storage=storage,
        **kwargs
    )
