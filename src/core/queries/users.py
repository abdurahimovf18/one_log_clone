from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import users as p
from src.core.data_transfer_objects.responses.queries import users as r
from src.models import User

model = User


async def create(data: p.CreateDTO, *, session: AsyncSession) -> r.CreateDTO:
    model_object = model(**data.model_dump())
    session.add(model_object)
    await session.flush([model_object])
    return r.CreateDTO.model_validate(model_object)
