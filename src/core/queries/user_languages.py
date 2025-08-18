import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import user_languages as p
from src.core.data_transfer_objects.responses.queries import user_languages as r
from src.models import UserLanguage

model = UserLanguage



async def exists(
    data: p.ExistsDTO,
    session: AsyncSession
    ) -> bool:
    """
    Checks if a UserLanguage matching the given criteria exists in the database.
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


async def get_by_chat_id(
        data: p.GetByChatIdDTO, 
        session: AsyncSession
    ) -> r.GetByChatIdDTO | None:
    """
    Finds and returns `UserLanguage` ORM object if it exists.
    Loads only `language` field.
    """

    query = (
        sa.select(model)
        .where(model.chat_id == data.chat_id)
        .options(
            sa_orm.load_only(model.language)
        )
    )
    result = await session.execute(query)
    model_result = result.scalar_one_or_none()
    if model_result is not None:
        return r.GetByChatIdDTO.model_validate(model_result)


async def create(
    data: p.CreateDTO,
    *,
    session: AsyncSession
    ) -> r.CreateDTO:
    model_object = model(**data.model_dump())
    session.add(model_object)
    await session.flush([model_object])
    return r.CreateDTO.model_validate(model_object)


async def update(
    data: p.UpdateDTO,
    *,
    session: AsyncSession,
    ) -> r.UpdateDTO | None:
    """
    Updates model language filtering by chat_id.
    """

    stmt = (
        sa.update(model)
        .where(model.chat_id == data.chat_id)
        .values(language=data.language)
        .returning(model)
    )
    result = await session.execute(stmt)
    result_model = result.scalar_one_or_none()
    if result_model is not None:
        return r.UpdateDTO.model_validate(result_model)
    