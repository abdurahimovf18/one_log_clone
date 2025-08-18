from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.filters.users.auth import is_authenticated, is_not_langauge_selected
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts.users import auth as auth_texts
from src.bot.texts.users import shared as shared_texts

router = Router(name="command_start")


@router.message(CommandStart(), is_not_langauge_selected)
async def start_language_select(
        msg: Message, 
        state: FSMContext
    ) -> None:

    await state.clear()
    await state.set_state(states.LanguageSelectState.select)

    await msg.answer(shared_texts.greeting())
    await msg.answer(
        text=auth_texts.language_request(), 
        reply_markup=keyboards.inline.language_select()
    )


@router.message(CommandStart(), is_authenticated)
async def start(
        msg: Message,
        state: FSMContext, 
    ) -> None:
    await state.clear()
    await msg.answer(shared_texts.greeting())


@router.message(CommandStart())
async def start_with_authentication(
        msg: Message, 
        state: FSMContext, 
    ) -> None:
    await state.clear()
    await state.set_state(states.Auth.select_method)
    
    await msg.answer(shared_texts.greeting())
    await msg.answer(auth_texts.auth_request())
    await msg.answer(
        auth_texts.auth_method_select(), 
        reply_markup=keyboards.inline.auth_methods_select()
    )
    