from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiolimiter import AsyncLimiter

from src.bot.filters.users.auth import has_user_tg_account, is_authenticated
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts.users import auth as auth_texts

router = Router(name="command_start")


@router.message(CommandStart(), has_user_tg_account, is_authenticated)
async def start_language_select(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(auth_texts.greet_old_user(), reply_markup=keyboards.reply.main_menu())


@router.message(CommandStart(), has_user_tg_account)
async def start(
        state: FSMContext, 
    ) -> None:
    await state.clear()


@router.message(CommandStart())
async def start_new_user(msg: Message, state: FSMContext, msg_limiter: AsyncLimiter) -> None:
    await state.clear()
    await state.set_state(states.LanguageSelectState.select)

    async with msg_limiter:
        await msg.answer(auth_texts.greet_new_user())

    async with msg_limiter:
        await msg.answer(
            auth_texts.request_for_language_select(), 
            reply_markup=keyboards.inline.language_select()
        )
