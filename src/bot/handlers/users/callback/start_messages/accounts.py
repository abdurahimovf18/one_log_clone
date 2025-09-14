from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core import queries

router = Router()


@router.callback_query(F.data == "accounts", states.NewMessage.menu)
async def handle_accounts(
        call: CallbackQuery,
        state: FSMContext,
        session: di.db_session,
        current_user: di.current_user,
        send_rate_limiter: di.SendRateLimiter
        ) -> None:
    
    current_page = 1

    if current_user is None:
        async with send_rate_limiter:
            await call.answer(texts.auth.user_not_authenticated(), show_alert=True)
        return

    await state.set_state(states.NewMessageAccount.menu)
    await state.update_data({"page": current_page})

    page = await queries.tg_accounts.get_page_by_user_id(
        queries.tg_accounts.p.GetPageByUserIdDTO(
            user_id=current_user.id, page=current_page
        ), session=session
    )

    if page.items_count == 0:
        async with send_rate_limiter:
            await call.message.edit_text(  # type: ignore
                texts.send_message.accounts_not_found(),
                reply_markup=keyboards.inline.info_not_found(show_add_btn=True)
            )
    else:
        items = {str(item.phone): str(item.session_id) for item in page.items}
        async with send_rate_limiter: 
            await call.message.edit_text(  # type: ignore
                texts.send_message.accounts_info(),
                reply_markup=keyboards.inline.pagination(
                    page=page.page, pages_count=page.pages_count, items=items
                )
            )


@router.callback_query(F.data == "add", states.NewMessageAccount.menu)
async def add(call: CallbackQuery, send_rate_limiter: di.SendRateLimiter) -> None:
    async with send_rate_limiter:
        await call.answer(texts.common.not_built())


@router.callback_query(states.NewMessageAccount.menu, F.data.is_digit())
async def paginate(
        call: CallbackQuery,
        state: FSMContext,
        session: di.db_session,
        current_user: di.current_user,
        send_rate_limiter: di.SendRateLimiter
        ) -> None:
    
    current_page = int(call.data)  # type: ignore

    if current_user is None:
        async with send_rate_limiter:
            await call.answer(texts.auth.user_not_authenticated(), show_alert=True)
        return

    await state.set_state(states.NewMessageAccount.menu)
    await state.update_data({"page": current_page})

    page = await queries.tg_accounts.get_page_by_user_id(
        queries.tg_accounts.p.GetPageByUserIdDTO(
            user_id=current_user.id, page=current_page
        ), session=session
    )

    if page.items_count == 0:
        async with send_rate_limiter:
            await call.message.edit_text(  # type: ignore
                texts.send_message.accounts_not_found(),
                reply_markup=keyboards.inline.info_not_found(show_add_btn=True)
            )
    else:
        items = {str(item.phone): str(item.session_id) for item in page.items}
        async with send_rate_limiter: 
            await call.message.edit_text(  # type: ignore
                texts.send_message.accounts_info(),
                reply_markup=keyboards.inline.pagination(
                    page=page.page, pages_count=page.pages_count, items=items
                )
            )
