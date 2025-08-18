import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import users as p
from src.core.data_transfer_objects.responses.queries import users as r
from src.models import User

model = User


async def exists(
    data: p.ExistsDTO, 
    *,
    session: AsyncSession
    ) -> bool:
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


async def get_password_by_username(
    data: p.GetPasswordByUsername,
    *,
    session: AsyncSession
    ) -> r.GetPasswordByUsername | None:
    """
    Looks for user by username and loads only password.
    """
    query = (
        sa.select(model)
        .where(model.username == data.username)
        .options(
            sa_orm.load_only(model.password)
        )
    )
    result = await session.execute(query)
    result_model = result.scalar_one_or_none()
    if result_model is not None:
        return r.GetPasswordByUsername.model_validate(result_model)
    