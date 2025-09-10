from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __

router = Router()


@router.message(F.text == __("♻️ Send Message"))
async def start_messages(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
    
    await state.set_state(states.SendMessage.menu)
    
    async with send_rate_limiter:
        await msg.answer(
            texts.send_message.message_info(),
            reply_markup=keyboards.inline.message_menu(
                allow_start=True,
                accounts_set=True
            )
        )