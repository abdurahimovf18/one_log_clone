from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import di
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.bot.utils.i18n import gettext_lazy as __

router = Router()


@router.message(F.text == __("🗂 Messages History"))
async def show_settings_menu(
        msg: Message,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
        ) -> None:

    await state.clear()
    await state.set_state(states.Settings.menu)

    async with send_rate_limiter:
        await msg.answer(
            texts.settings.setting_menu()
        )    
