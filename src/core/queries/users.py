import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import users as p

# from src.core.data_transfer_objects.responses.queries import users as r
from src.models import User

model = User


async def exists(data: p.ExistsDTO, session: AsyncSession) -> bool:
    """
    Checks if a User matching the given criteria exists in the database.
    Returns True if exists, False otherwise.
    """
    valid_keys = {c.key for c in model.__table__.columns}
    exists_fields = {
        key: val for key, val in data.model_dump().items()
        if val is not None and key in valid_keys
    }

    conditions = [getattr(model, k) == v for k, v in exists_fields.items()]
    exists_condition = sa.exists(model).where(sa.and_(*conditions))

    query = sa.select(exists_condition)
    result = await session.execute(query)
    return result.scalar_one()
