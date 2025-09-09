from typing import cast

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.filters import users as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core.domain_schema.settings import UserLanguages
from src.core.use_cases import bot as use_cases

router = Router()


@router.callback_query(states.TgUserAuth.language_select, filters.is_language_message)
async def register_tg_user_language(
        call: CallbackQuery, 
        state: FSMContext, 
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        ) -> None:

    lang_text = cast(str, call.data)
    current_language: UserLanguages = getattr(UserLanguages, lang_text)

    registered_user_info = await use_cases.register_tg_user(
        use_cases.p.RegisterTgUserDTO(
            chat_id=call.from_user.id,
            language=current_language
        ),
        session=session,
    )

    await state.clear()
    await state.set_state(states.Auth.select_method)

    async with send_rate_limiter:
        await call.answer(texts.auth.language_setup_complete(registered_user_info.language.value))
    
    async with send_rate_limiter:
        await call.message.answer(  # type: ignore
            texts.auth.auth_request(),
            reply_markup=keyboards.inline.auth_methods_select()
        )

    await session.commit()

