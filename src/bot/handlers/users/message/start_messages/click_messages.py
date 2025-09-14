from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __
from src.config.settings import DEFAULT_DURATION, DEFAULT_INTERVAL
from src.core.use_cases import users as use_cases

router = Router()


@router.message(F.text == __("♻️ Send Message"))
async def start_messages(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        current_user: di.current_user
        ) -> None:

    await state.clear()
    await state.set_state(states.NewMessage.menu)

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