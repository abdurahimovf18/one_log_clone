from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import types as state_types
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __

router = Router()


@router.message(F.text == __("💬 Message Settings"), states.Settings.menu)
async def show_message_settings(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:
    
    data: state_types.SettingsStateData = {"page": {"items": []}}
    await state.set_data(data)
    
    await state.set_state(states.MessageSettings.menu)
    
    async with send_rate_limiter:
        await msg.answer(
            texts.settings.message_settings_info(),
            reply_markup=keyboards.inline.message_settings()
        )