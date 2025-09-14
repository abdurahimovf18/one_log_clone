import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import texts as p
from src.core.data_transfer_objects.responses.queries import texts as r
from src.models import Texts

model = Texts


async def create(data: p.CreateDTO, *, session: AsyncSession) -> r.CreateDTO:
    model_object = model(**data.model_dump())
    session.add(model_object)
    await session.flush([model_object])
    return r.CreateDTO.model_validate(model_object)


async def get_by_id(data: p.GetByIdDTO, *, session: AsyncSession) -> r.GetByIdDTO | None:
    query = sa.select(model).where(model.id == data.id)
    result = await session.execute(query)
    model_result = result.scalar_one_or_none()
    if model_result is not None:
        return r.GetByIdDTO.model_validate(model_result)
    