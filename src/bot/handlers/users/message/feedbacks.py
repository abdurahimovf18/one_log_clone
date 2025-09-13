from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __
from src.core.use_cases import users as use_cases

router = Router()


@router.message(F.text == __("✍️ Leave Feedback"))
async def start_feedback(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
    
    await state.set_state(states.Feedback.accept)

    async with send_rate_limiter:
        await msg.answer(
            texts.feedbacks.start_feedback(),
            reply_markup=keyboards.reply.back()
        )

@router.message(states.Feedback.accept, F.text == __("⬅️ Back"))
async def cencel_feedback(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
    
    await state.clear()
    async with send_rate_limiter:
        await msg.answer(
            texts.feedbacks.cencel_feedback(),
            reply_markup=keyboards.reply.main_menu()
        )


@router.message(states.Feedback.accept)
async def accept_user_feedback(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        ) -> None:
    
    await state.clear()

    await use_cases.accept_feedback(
        use_cases.p.AcceptFeedbackDTO(
            chat_id=msg.chat.id,
            user_id=msg.from_user.id,  # type: ignore
            reply_message_id=msg.message_id,
            message=msg.text  # type: ignore
        ),
        session=session
    )

    await session.commit()

    async with send_rate_limiter:
        await msg.answer(
            texts.feedbacks.feedback_accepted(),
            reply_markup=keyboards.reply.main_menu()
        )
