from typing import cast

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.filters import users as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.config.settings import DEFAULT_LANGUAGE
from src.core import queries
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


@router.callback_query(states.Language.select, filters.is_language_message)
async def set_user_language(
        call: CallbackQuery, 
        state: FSMContext, 
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        ) -> None:

    await state.clear()

    user_info = await queries.tg_users.get_language_by_chat_id(
        queries.tg_users.p.GetLanguageByChatId(chat_id=call.from_user.id), session=session
    )

    new_language = cast(
        UserLanguages, 
        getattr(UserLanguages, call.data or DEFAULT_LANGUAGE.value, None)
    )
    old_language = user_info.language if user_info is not None else DEFAULT_LANGUAGE

    if new_language == old_language:
        async with send_rate_limiter:
            await call.message.answer(  # type: ignore
                texts.language.old_language_selected(language=old_language.value),
                reply_markup=keyboards.reply.main_menu()
            )

    else:
        await queries.tg_users.update_language(
            queries.tg_users.p.UpdateLanguageDTO(
                chat_id=call.from_user.id, language=new_language
            ), session=session
        )

        await session.commit()

        async with send_rate_limiter:
            await call.message.answer(  # type: ignore
                texts.language.set_new_language(new_language.value, old_language.value),
                reply_markup=keyboards.reply.main_menu()
            )
