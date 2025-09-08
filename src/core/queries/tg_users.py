import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import tg_users as p
from src.core.data_transfer_objects.responses.queries import tg_users as r
from src.models import TgUser

model = TgUser


async def exists_by_chat_id(data: p.ExistsByChatIdDTO, *, session: AsyncSession) -> bool:
    """
    Looks for <table>.chat_id and returns True if finds at least one match, else False 
    """
    query = sa.select(sa.exists(model).where(model.chat_id == data.chat_id))
    result = await session.execute(query)
    return result.scalar_one()


async def get_user_id_by_chat_id(
        data: p.GetUserIdByChatIdDTO, *, session: AsyncSession
    ) -> r.GetUserIdByChatIdDTO | None:
    query = (
        sa.select(model)
        .where(model.chat_id == data.chat_id)
        .options(sa_orm.load_only(model.user_id))
    )
    result = await session.execute(query)
    model_result = result.scalar_one_or_none()
    if model_result is not None:
        return r.GetUserIdByChatIdDTO.model_validate(model_result)


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
    