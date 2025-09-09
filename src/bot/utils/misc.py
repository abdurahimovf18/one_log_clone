from aiogram.types import CallbackQuery, InlineQuery, Message, Update


def get_update_text(upd: Update, raise_exc: bool = False) -> str | None:
    
    if isinstance(upd, Message):
        return upd.text
    
    if isinstance(upd, CallbackQuery):
        return upd.data
    
    if isinstance(upd, InlineQuery):
        return upd.query

    if raise_exc:
        raise ValueError(f"Update type not suppored, update={upd}")
    