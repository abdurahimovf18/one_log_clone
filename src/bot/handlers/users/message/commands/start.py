from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.filters import users as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts

router = Router()


@router.message(CommandStart(), filters.has_user_tg_account, filters.is_authenticated)
async def start_language_select(
        msg: Message, 
        state: FSMContext,
        ) -> None:
    await state.clear()
    await msg.answer(
        texts.auth.greet_old_user(), 
        reply_markup=keyboards.reply.main_menu()
    )


@router.message(CommandStart(), filters.has_user_tg_account)
async def start(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter 
    ) -> None:
    await state.clear()
    await state.set_state(states.Auth.select_method)
    
    async with send_rate_limiter:
        await msg.answer(
            texts.auth.auth_request(),
            reply_markup=keyboards.inline.auth_methods_select()
        )


@router.message(CommandStart())
async def start_new_user(
        msg: Message, 
        state: FSMContext, 
        send_rate_limiter: di.SendRateLimiter
        ) -> None:
    await state.clear()
    await state.set_state(states.TgUserAuth.language_select)

    async with send_rate_limiter:
        await msg.answer(texts.auth.greet_new_user())

    async with send_rate_limiter:
        await msg.answer(
            texts.auth.request_for_language_select(), 
            reply_markup=keyboards.inline.language_select()
        )
