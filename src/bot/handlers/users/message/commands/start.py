from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dishka.integrations.aiogram import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.filters.users.auth import is_authenticated

router = Router(name="command_start")


@router.message(CommandStart(), is_authenticated)
async def start_authenticated(
        # msg: Message, 
        # state: FSMContext, 
        session: FromDishka[AsyncSession]
    ) -> None:
    print(1)
    print(session)
    # await session.commit()


@router.message(CommandStart())
async def start_not_authenticated(
        msg: Message, 
        state: FSMContext, 
        session: FromDishka[AsyncSession]
    ) -> None:
    print(2)
    print(session)
