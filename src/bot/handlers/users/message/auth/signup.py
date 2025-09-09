from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core import queries
from src.core.use_cases import bot as use_cases

router = Router()


@router.message(states.SignUp.username)
async def accept_username(
        msg: Message, 
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session
        ) -> None:
    
    if msg.text is None:
        await state.clear()
        async with send_rate_limiter:
            await msg.answer(texts.exceptions.unexpected_error())
        return

    is_username_taken = await queries.user_auth.exists_by_username(
        queries.user_auth.p.ExistsByUsernameDTO(
            username=msg.text  # type: ignore
        ),
        session=session
    )

    if is_username_taken:
        async with send_rate_limiter:
            await msg.answer(
                texts.auth.username_is_taken(username=msg.text),
                reply_markup=keyboards.inline.auth_signin_switch()
            )
    else:
        await state.set_state(states.SignUp.password)
        await state.update_data(username=msg.text)
        
        async with send_rate_limiter:
            await msg.answer(
                texts.auth.password_request(),
                reply_markup=keyboards.inline.auth_signin_switch()
            )
    

@router.message(states.SignUp.password)
async def accept_password(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session
        ) -> None:
    data = await state.get_data()
    await state.clear()
    username: str | None = data.get("username", None)

    if username is None or msg.text is None:
        async with send_rate_limiter:
            await msg.answer(texts.exceptions.unexpected_error())
        return

    try:
        await use_cases.signup(
            use_cases.p.SignUpDTO(
                username=username,
                password=msg.text,
            ),
            session=session
        )
        await session.commit()
    except use_cases.exceptions.UsernameIsTaken:
        await state.set_state(states.SignUp.username)

        async with send_rate_limiter:
            await msg.answer(
                texts.auth.username_is_taken(username),
                reply_markup=keyboards.inline.auth_signin_switch()
            )

    else:
        await state.set_state(states.SignIn.username)

        async with send_rate_limiter:
            await msg.answer(texts.auth.signup_success())
        
        async with send_rate_limiter:
            await msg.answer(
                texts.auth.username_request(),
                reply_markup=keyboards.inline.auth_signup_switch()
            )
