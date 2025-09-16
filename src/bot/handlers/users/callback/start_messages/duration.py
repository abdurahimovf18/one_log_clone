
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.filters import users as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import types as state_types
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext as _
from src.bot.utils.misc import get_timedelta
from src.config.settings import DEFAULT_DURATION, DURATIONS
from src.core import queries
from src.core.domain_schema.settings import TimeDelta

router = Router()


@router.callback_query(F.data == "duration", states.NewMessage.menu)
async def show_awaible_durations(
        call: CallbackQuery,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        current_user: di.current_user,
        ) -> None:
    
    if current_user is None:
        async with send_rate_limiter:
            await call.answer(texts.auth.user_not_authenticated(), show_alert=True)
        return
    
    await state.set_state(states.NewMessageDuration.menu)

    data = await state.get_data()
    message_info: state_types.MessageData | None = data.get("current_message")

    if message_info is None:
        async with send_rate_limiter:
            await call.message.edit_text(texts.exceptions.unexpected_error())  # type: ignore
        return

    message_duration = message_info["duration"]
    current_timedelta: TimeDelta = get_timedelta(message_duration, DURATIONS) or DEFAULT_DURATION

    keyboard_choices: dict[str, str] = {}
    for duration in DURATIONS:
        keyboard_choices[_(str(duration.label))] = duration.callback_value

    async with send_rate_limiter:
        await call.message.edit_text(  # type: ignore
            texts.send_message.duration_info(),
            reply_markup=keyboards.inline.time_choice(
                keyboard_choices, current_timedelta.callback_value
            )
        )


@router.callback_query(
    states.NewMessageDuration.menu, 
    filters.Contains({time_value.callback_value for time_value in DURATIONS})
)
async def set_new_duration(
        call: CallbackQuery,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        current_user: di.current_user,
        session: di.db_session,
        ) -> None:

    if current_user is None:
        async with send_rate_limiter:
            await call.answer(texts.auth.user_not_authenticated(), show_alert=True)
        return
    
    data = await state.get_data()
    message_info: state_types.MessageData | None = data.get("current_message")

    if message_info is None:
        async with send_rate_limiter:
            await call.message.edit_text(texts.exceptions.unexpected_error())  # type: ignore
        return

    message_duration = message_info["duration"]
    old_timedelta: TimeDelta = get_timedelta(message_duration, DURATIONS) or DEFAULT_DURATION
    new_timedelta: TimeDelta = DEFAULT_DURATION

    for duration in DURATIONS:
        if duration.callback_value == call.data: 
            new_timedelta = duration
            break

    if new_timedelta == old_timedelta:
        return
    
    await queries.messages.update_duration_by_id(
        queries.messages.p.UpdateDurationByIdDTO(
            id=message_info["id"], duration=new_timedelta.value
        ), session=session
    )

    await session.commit()

    keyboard_choices: dict[str, str] = {}
    for duration in DURATIONS:
        keyboard_choices[_(str(duration.label))] = duration.callback_value

    async with send_rate_limiter:
        await call.message.edit_text(  # type: ignore
            texts.send_message.duration_info(),
            reply_markup=keyboards.inline.time_choice(
                keyboard_choices, new_timedelta.callback_value
            )
        )