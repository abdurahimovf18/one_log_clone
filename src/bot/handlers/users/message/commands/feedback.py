from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.filters import users as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts

router = Router()


@router.message(Command("feedback"), filters.is_authenticated)
async def authenticated_user_feedback(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
    
    await state.clear()
    await state.set_state(states.Feedback.accept)

    async with send_rate_limiter:
        await msg.answer(
            texts.feedbacks.start_feedback(),
            reply_markup=keyboards.reply.back()
        )


@router.message(Command("feedback"))
async def anonim_user_feedback(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
        
    await state.clear()

    async with send_rate_limiter:
        await msg.answer(
            texts.feedbacks.not_authenticated()
        )
        