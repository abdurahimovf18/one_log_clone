from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.users import auth as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core.use_cases import bot as use_cases

router = Router(name="user_auth_language")


@router.callback_query(
    states.LanguageSelectState.select,
    filters.is_language_message,
)
async def register_user_language(
    call: CallbackQuery,
    state: FSMContext,
    session: FromDishka[AsyncSession]
) -> None:
    await state.set_state(states.Auth.select_method)
    await use_cases.set_user_language(
        use_cases.p.SetUserLanguageDTO(
            chat_id=call.from_user.id, 
            language=call.data,  # type: ignore
        ),
        session=session,
    )
    await call.message.answer(  # type: ignore
        texts.auth.auth_method_select(), 
        reply_markup=keyboards.inline.auth_methods_select()
    )

    await session.commit()

