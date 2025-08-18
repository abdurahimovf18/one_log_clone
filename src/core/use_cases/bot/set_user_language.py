from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy import exc as sa_exc
from src.core.data_transfer_objects.paramters.use_cases.bot import auth as p
from src.core.data_transfer_objects.responses.use_cases.bot import auth as r
from src.core.queries import user_languages


async def execute(
        data: p.SetUserLanguageDTO, 
        session: AsyncSession
    ) -> r.SetUserLanguageDTO:

    user_language = await user_languages.update(
        user_languages.p.UpdateDTO(**data.model_dump()),
        session=session
    )

    if user_language is None:
        user_language = await user_languages.create(
            user_languages.p.CreateDTO.model_construct(**data.model_dump()),
            session=session
        )

    return r.SetUserLanguageDTO.model_construct(**user_language.model_dump())
