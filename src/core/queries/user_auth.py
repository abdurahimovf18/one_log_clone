import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import user_auth as p
from src.core.data_transfer_objects.responses.queries import user_auth as r
from src.models import UserAuth

model = UserAuth


async def create(data: p.CreateDTO, *, session: AsyncSession) -> r.CreateDTO:
    model_object = model(**data.model_dump())
    session.add(model_object)
    await session.flush([model_object])
    return r.CreateDTO.model_validate(model_object)


async def get_password_by_username(
        data: p.GetPasswordByUsername, *, session: AsyncSession
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
    