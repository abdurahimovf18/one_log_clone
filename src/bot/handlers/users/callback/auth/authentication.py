from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts

router = Router(name="user_auth")


@router.callback_query(
    F.data == "signin", 
    states.Auth.select_method
)    
async def select_auth_method_signup(
    call: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(states.SignIn.username)
    await call.message.edit_text(  # type: ignore
        texts.auth.signin_request(),
    )
    await call.message.answer(  # type: ignore
        texts.auth.username_request(),
        reply_markup=keyboards.inline.auth_signup_switch()
    )


@router.callback_query(
    F.data == "signup", 
    states.Auth.select_method
)
async def select_auth_method_signin(
    call: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(states.SignUp.username)
    await call.message.edit_text(  # type: ignore
        texts.auth.signup_request(),
    )
    await call.message.answer(  # type: ignore
        texts.auth.username_request(),
        reply_markup=keyboards.inline.auth_signin_switch()
    )


@router.callback_query(
    F.data == "signin",
    StateFilter(
        states.SignIn.username,
        states.SignIn.password
    )
)
async def switch_to_signup(    
    call: CallbackQuery,
    state: FSMContext,
) -> None:
    await state.clear()
    await state.set_state(states.SignUp.username)

    await call.message.edit_text(  # type: ignore
        texts.auth.signup_request()
    )
    await call.message.answer(  # type: ignore
        texts.auth.username_request(),
        reply_markup=keyboards.inline.auth_signin_switch()
    )


