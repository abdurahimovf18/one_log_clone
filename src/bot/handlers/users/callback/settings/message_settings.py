from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot import di
from src.bot.keyboards import users as keyboards
from src.bot.states import types as state_types
from src.bot.states import users as states
from src.bot.texts import users as texts
from src.core import queries

router = Router()


@router.callback_query(states.MessageSettings.menu, F.data == "groups")
async def show_message_settings_pagination(
        call: CallbackQuery,
        state: FSMContext,
        send_rate_limiter: di.SendRateLimiter,
		current_user: di.current_user,
		session: di.db_session,
        ) -> None:

	if current_user is None:
		async with send_rate_limiter:
			await call.answer(texts.auth.user_not_authenticated())
		return

	data = cast(state_types.SettingsStateData, await state.get_data())
	await state.set_state(states.MessageGroupSettings.menu)

	page = await queries.tg_groups.get_page_by_user_id(
		queries.tg_groups.p.GetPageByUserIdDTO(
			owner_id=current_user.id, page=1
		), session=session
	)

	data["page"]["items"] = [
		{"is_selected": False, "callback": item.username, "label": item.username}
		for item in page.items
	]
	await state.set_data(data)

	items = {item.username: item.username for item in page.items}
	selected_items = {item["callback"] for item in data["page"]["items"] if item["is_selected"]}

	async with send_rate_limiter:
		await call.message.edit_text(  # type: ignore
			texts.settings.message_group_settings_info(),
			reply_markup=keyboards.inline.settings_pagination(
				page=page.page, pages_count=page.pages_count, 
				items=items, selected_items=selected_items
			)
		)


