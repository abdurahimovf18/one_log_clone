import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core.use_cases import bot as use_cases

logger = logging.getLogger(__name__)


router = Router(name="user_auth_signin")


@router.message(
    states.SignIn.username,
)
async def signin_username(
    msg: Message,
    state: FSMContext
) -> None:
    await state.set_state(states.SignIn.password)
    await state.update_data(username=msg.text)
    await msg.answer(
        texts.auth.password_request(),
        reply_markup=keyboards.inline.auth_signup_switch()
    )
    

@router.message(
    states.SignIn.password,
)
async def signin_password(    
    msg: Message,
    state: FSMContext,
    session: FromDishka[AsyncSession],
) -> None:
    data = await state.get_data()
    username: str | None = data.get("username", None)

    if username is None:
        await state.clear()
        await msg.answer(
            texts.exceptions.unexpected_error()
        )
    
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
        await msg.answer(texts.auth.signin_failed())
        await msg.answer(
            texts.auth.username_request(),
            reply_markup=keyboards.inline.auth_signup_switch()
        )
    except Exception:
        logger.exception("Unhandled exception")
