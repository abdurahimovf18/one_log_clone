from typing import cast

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.bot import di
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.keyboards import users as keyboards
from src.core import queries
from src.core.use_cases import users as use_cases
from src.config.settings import DEFAULT_INTERVAL, DEFAULT_DURATION

router = Router()


@router.message(states.NewMessageText.menu, F.text)
async def set_message_text(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        current_user: di.current_user
        ) -> None:
    
    await state.clear()
    await state.set_state(states.NewMessage.menu)
    
    if current_user is None:
        async with send_rate_limiter:
            await msg.answer(texts.auth.user_not_authenticated())
        return

    await use_cases.update_message_text(
        use_cases.p.UpdateMessageTextDTO(user_id=current_user.id, text=msg.text),  # type: ignore
        session=session
    )

    message_info = await use_cases.get_current_message(
        use_cases.p.GetCurrentMessageDTO(
            user_id=current_user.id  # type: ignore
        ), session=session
    )

    await session.commit()

    async with send_rate_limiter:
        await msg.answer(
            texts.send_message.message_info(),
            reply_markup=keyboards.inline.message_menu(
                allow_start=False,
                accounts_set=False,
                interval_set=message_info.interval != DEFAULT_INTERVAL,
                duration_set=message_info.duration != DEFAULT_DURATION,
                groups_set=False,
                message_set=message_info.text_id is not None,
            )
        )
