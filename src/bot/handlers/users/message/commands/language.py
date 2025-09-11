from aiogram import Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.config.settings import DEFAULT_LANGUAGE
from src.core import queries

router = Router()


@router.message(Command("language"))
async def authenticated_user_feedback(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        ) -> None:
    
    await state.clear()
    await state.set_state(states.Language.select)

    user_info = await queries.tg_users.get_language_by_chat_id(
        queries.tg_users.p.GetLanguageByChatId(
            chat_id=msg.from_user.id  # type: ignore
        ),
        session=session
    )

    if user_info is None:
        current_language = DEFAULT_LANGUAGE.value
    else:
        current_language = user_info.language.value

    async with send_rate_limiter:
        await msg.answer(
            texts.language.language_select(current_language),
            reply_markup=keyboards.inline.language_select()
        )
        