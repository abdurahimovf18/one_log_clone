from collections.abc import Iterable
from datetime import timedelta

from aiogram.types import CallbackQuery, InlineQuery, Message, Update

from src.core.domain_schema.settings import TimeDelta


def get_update_text(upd: Update, raise_exc: bool = False) -> str | None:
    
    if isinstance(upd, Message):
        return upd.text
    
    if isinstance(upd, CallbackQuery):
        return upd.data
    
    if isinstance(upd, InlineQuery):
        return upd.query

    if raise_exc:
        raise ValueError(f"Update type not suppored, update={upd}")
    

def get_update_user_id(upd: Update, raise_exc: bool = False) -> int | None:
    
    if isinstance(upd, Message):
        return upd.from_user.id  # type: ignore
    
    elif isinstance(upd, CallbackQuery):
        return upd.from_user.id
    
    elif isinstance(upd, InlineQuery):
        return upd.from_user.id

    else:
        if raise_exc:
            raise ValueError(f"Update type not suppored, update={upd}")
    

def get_timedelta(timedelta: timedelta, lookup_values: Iterable[TimeDelta]) -> TimeDelta | None:

    for interval in lookup_values:
        if interval.value == timedelta:
            return interval