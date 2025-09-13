from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __
from src.core import queries
from src.core.use_cases import users as use_cases

router = Router()


@router.message(F.text == __("♻️ Send Message"))
async def start_messages(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        ) -> None:
    
    await state.set_state(states.SendMessage.menu)
    
    user_info = await queries.tg_users.get_user_id_by_chat_id(
        queries.tg_users.p.GetUserIdByChatIdDTO(
            chat_id=msg.from_user.id  # type: ignore
        ), session=session
    )

    if user_info is None:
        return 

    message_info = await use_cases.get_current_message(
        use_cases.p.GetCurrentMessageDTO(
            user_id=user_info.id
        )
    )


    async with send_rate_limiter:
        await msg.answer(
            texts.send_message.message_info(),
            reply_markup=keyboards.inline.message_menu(
                allow_start=True,
                accounts_set=True
            )
        )