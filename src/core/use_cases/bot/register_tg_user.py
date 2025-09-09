from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.use_cases.bot import auth as p
from src.core.data_transfer_objects.responses.use_cases.bot import auth as r
from src.core.queries import tg_users


async def execute(data: p.RegisterTgUserDTO, *, session: AsyncSession) -> r.RegisterTgUserDTO:
    tg_user = await tg_users.create(
        tg_users.p.CreateDTO(
            chat_id=data.chat_id,
            language=data.language
        ),
        session=session
    )

    return r.RegisterTgUserDTO.construct_from_dto(tg_user)
    