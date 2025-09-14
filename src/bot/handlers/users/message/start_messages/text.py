from aiogram import F, Router
from aiogram.types import Message

from src.bot import di
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core import queries

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

    message = queries.messages.get_created_message(
        queries.messages.p.GetCreatedMessageDTO(owner_id=current_user.id), session=session
    )

    print(message)

