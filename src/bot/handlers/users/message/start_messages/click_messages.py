from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import types as state_types
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __
from src.config.settings import DEFAULT_DURATION, DEFAULT_INTERVAL
from src.core import queries
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

    if current_user is None:
        async with send_rate_limiter:
            await msg.answer(texts.auth.user_not_authenticated())  # type: ignore
        return
    
    await state.clear()
    await state.set_state(states.NewMessage.menu)

    created_message_info = await use_cases.get_created_message(
        use_cases.p.GetCreatedMessageDTO(owner_id=current_user.id), session=session
    )

    current_message_data: state_types.MessageData = {
        "id": created_message_info.id,
        "interval": created_message_info.interval,
        "duration": created_message_info.duration,
        "owner_id": created_message_info.owner_id,
        "created_at": created_message_info.created_at,
        "started_at": created_message_info.started_at,
        "text_id": created_message_info.text_id
    }

    await state.update_data(current_message=current_message_data)

    accounts_set = await queries.tg_accounts.exists_active_by_user_id(
        queries.tg_accounts.p.ExistsActiveByUserIdDTO(user_id=current_user.id), session=session
    )
    groups_set = await queries.tg_groups.exists_active_by_user_id(
        queries.tg_groups.p.ExistsActiveByUserIdDTO(owner_id=current_user.id), session=session
    )
    message_set = created_message_info.text_id is not None
    allow_start = accounts_set and groups_set and message_set

    await session.commit()

    async with send_rate_limiter:
        await msg.answer(  # type: ignore
            texts.send_message.message_info(),
            reply_markup=keyboards.inline.message_menu(
                allow_start=allow_start,
                accounts_set=accounts_set,
                interval_set=created_message_info.interval != DEFAULT_INTERVAL.value,
                duration_set=created_message_info.duration != DEFAULT_DURATION.value,
                groups_set=False,
                message_set=created_message_info.text_id is not None,
            )
        )