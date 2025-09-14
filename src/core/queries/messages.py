import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import messages as p
from src.core.data_transfer_objects.responses.queries import messages as r
from src.models import Message
from src.models.shared.enums import MessageStatus

model = Message


async def create(data: p.CreateDTO, *, session: AsyncSession) -> r.CreateDTO:
    model_object = model(**data.model_dump())
    session.add(model_object)
    await session.flush([model_object])
    return r.CreateDTO.model_validate(model_object)


async def get_created_message(
        data: p.GetCreatedMessageDTO,
        *,
        session: AsyncSession
    ) -> r.GetCreatedMessageDTO | None: 

    query = (
        sa.select(model)
        .where(
            sa.and_(
                model.owner_id == data.owner_id,
                model.status == MessageStatus.CREATED
            ) 
        )
        .limit(1)
        .order_by(
            sa.desc(model.created_at)
        )
        .options(
            sa_orm.load_only(
                model.owner_id,
                model.interval,
                model.duration,
                model.text_id,
            )
        )
    )
    result = await session.execute(query)
    model_result = result.scalar_one_or_none()
    if model_result is not None:
        return r.GetCreatedMessageDTO.model_validate(model_result)
    