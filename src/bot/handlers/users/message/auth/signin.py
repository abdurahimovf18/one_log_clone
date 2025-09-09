from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core.use_cases import bot as use_cases

router = Router()


@router.message(states.SignIn.username)
async def accept_username(
        msg: Message, 
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
    await state.set_state(states.SignIn.password)
    await state.update_data(username=msg.text)

    async with send_rate_limiter:
        await msg.answer(
            texts.auth.password_request(),
            reply_markup=keyboards.inline.auth_signup_switch()
        )
    

@router.message(states.SignIn.password,)
async def accept_password(
        msg: Message, 
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,      
        session: di.db_session,
        ) -> None:
    data = await state.get_data()
    username: str | None = data.get("username", None)

    if username is None:
        await state.clear()
        await msg.answer(
            texts.exceptions.unexpected_error()
        )
        return
    
    try:
        await use_cases.signin(
            use_cases.p.SignInDTO(
                username=username,  # type: ignore
                password=msg.text,  # type: ignore
                chat_id=msg.from_user.id  # type: ignore
            ),
            session=session
        )
        await session.commit()
    except (
            use_cases.exceptions.PasswordIncorrect,
            use_cases.exceptions.UsernameNotFound,    
        ):
        async with send_rate_limiter:
            await msg.answer(texts.auth.signin_failed())

        async with send_rate_limiter:
            await msg.answer(
                texts.auth.username_request(),
                reply_markup=keyboards.inline.auth_signup_switch()
            )
    else:
        await state.clear()
        async with send_rate_limiter:
            await msg.answer(
                texts.auth.signin_success(),
                reply_markup=keyboards.reply.main_menu()
            )
