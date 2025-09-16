
from aiogram import F, Router
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core.use_cases import users as use_cases

router = Router()


@router.message(states.NewMessageText.menu, F.text)
async def set_message_text(
        msg: Message,
        send_rate_limiter: di.SendRateLimiter,
        session: di.db_session,
        current_user: di.current_user
        ) -> None:
    
    if current_user is None:
        async with send_rate_limiter:
            await msg.answer(texts.auth.user_not_authenticated())
        return

    await use_cases.update_message_text(
        use_cases.p.UpdateMessageTextDTO(user_id=current_user.id, text=msg.text),  # type: ignore
        session=session
    )

    await session.commit()

    async with send_rate_limiter:
        await msg.answer(texts.send_message.message_updated())
    
    async with send_rate_limiter:
        await msg.answer(
            texts.send_message.message_content_request(msg.text),
            reply_markup=keyboards.inline.back()
        )

