import sqlalchemy as sa
from sqlalchemy import orm as sa_orm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.queries import user_languages as p
from src.core.data_transfer_objects.responses.queries import user_languages as r
from src.models import UserLanguage

model = UserLanguage


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
