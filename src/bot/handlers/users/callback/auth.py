from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.filters.state import StateFilter

from src.bot.filters import users as filters
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot import di

router = Router()


@router.callback_query(states.Auth.select_method, filters.is_any_auth_method)
async def select_auth_method(
        call: CallbackQuery,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter
        ) -> None:
    
    auth_method = call.data

    if auth_method == "signin":
        await state.set_state(states.SignIn.username)

        async with send_rate_limiter:
            await call.message.answer(  # type: ignore
                texts.auth.signin_start()
            )

        async with send_rate_limiter:
            await call.message.answer(  # type: ignore
                texts.auth.username_request(),
                reply_markup=keyboards.inline.auth_signup_switch()
            )

    elif auth_method == "signup":
        await state.set_state(states.SignUp.username)

        async with send_rate_limiter:
            await call.message.answer(  # type: ignore
                texts.auth.signup_start()
            )

        async with send_rate_limiter:
            await call.message.answer(  # type: ignore
                texts.auth.username_request(),
                reply_markup=keyboards.inline.auth_signin_switch()
            )
        

@router.callback_query(
    filters.IsAuthMethod("signup"), 
    StateFilter(*states.SignIn.__all_states__)
)
async def switch_auth_method_to_signup(
        call: CallbackQuery,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter
        ) -> None:
    
    await state.clear()
    await state.set_state(states.SignUp.username)

    async with send_rate_limiter:
        await call.message.answer(  # type: ignore
            texts.auth.signup_start()
        )

    async with send_rate_limiter:
        await call.message.answer(  # type: ignore
            texts.auth.username_request(),
            reply_markup=keyboards.inline.auth_signin_switch()
        )
    

@router.callback_query(
    filters.IsAuthMethod("signin"),
    StateFilter(*states.SignUp.__all_states__)
)
async def switch_auth_method_to_signin(
        call: CallbackQuery,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter
        ) -> None:
    
    await state.clear()
    await state.set_state(states.SignIn.username)

    async with send_rate_limiter:
        await call.message.answer(  # type: ignore
            texts.auth.signin_start()
        )

    async with send_rate_limiter:
        await call.message.answer(  # type: ignore
            texts.auth.username_request(),
            reply_markup=keyboards.inline.auth_signin_switch()
        )
    