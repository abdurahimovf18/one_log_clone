from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core import queries

router = Router()


@router.callback_query(F.data == "message", states.NewMessage.menu)
async def set_message(
        call: CallbackQuery, 
        state: FSMContext, 
        send_rate_limiter: di.SendRateLimiter,
        current_user: di.current_user,
        session: di.db_session
    ) -> None:
    
    await state.set_state(states.NewMessageText.menu)

    if current_user is None:
        async with send_rate_limiter:
            await call.answer(texts.auth.user_not_authenticated(), show_alert=True)
        return

    message = queries.messages.get_created_message(
        queries.messages.p.GetCreatedMessageDTO(owner_id=current_user.id), session=session
    )

    print(message)

    async with send_rate_limiter:
        await call.message.edit_text(  # type: ignore
            texts.send_message.message_content_request(),
            reply_markup=keyboards.inline.back()
        )
