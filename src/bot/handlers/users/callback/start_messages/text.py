from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core import queries
from src.core.use_cases import users as use_cases


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

    message_info = await use_cases.get_current_message(
        use_cases.p.GetCurrentMessageDTO(user_id=current_user.id), session=session
    )
    
    # check if text_id does not exist
    if message_info.text_id is None:
        async with send_rate_limiter:
            await call.message.edit_text(  # type: ignore
                texts.send_message.message_content_request(None),
                reply_markup=keyboards.inline.back()
            )

    else:  # do logic if text_id exists
        text_info = await queries.texts.get_by_id(
            queries.texts.p.GetByIdDTO(id=message_info.text_id), session=session
        )

        old_text = text_info.content if text_info else None
        async with send_rate_limiter:
            await call.message.edit_text(  # type: ignore
                texts.send_message.message_content_request(old_text),
                reply_markup=keyboards.inline.back()
            )


