from aiogram import F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.config.settings import DEFAULT_DURATION, DEFAULT_INTERVAL
from src.core.use_cases import users as use_cases

router = Router()


@router.callback_query(
    F.data == "back", 
    StateFilter(
        states.NewMessageAccount.menu,
        states.NewMessageDuration.menu,
        states.NewMessageInterval.menu,
        states.NewMessageGroup.menu,
        states.NewMessageText.menu,
        states.NewMessageStart.menu,
    ))
async def back(
        call: CallbackQuery,
        state: FSMContext,
        session: di.db_session,
        current_user: di.current_user,
        send_rate_limiter: di.SendRateLimiter
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
        await call.message.edit_text(  # type: ignore
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