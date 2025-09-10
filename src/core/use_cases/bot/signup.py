from sqlalchemy import exc as sa_exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.use_cases import bot as p
from src.core.data_transfer_objects.responses.use_cases import bot as r
from src.core.exceptions.use_cases import bot as exceptions
from src.core.queries import user_auth, users
from src.utils.auth import hash_password


async def execute(data: p.SignUpDTO, *,session: AsyncSession) -> r.SignUpDTO:
    password = hash_password(data.password)

    new_user = await users.create(
        users.p.CreateDTO(), session=session
    )

    try:
        new_user = await user_auth.create(
            user_auth.p.CreateDTO(
                user_id=new_user.id,
                username=data.username, 
                password=password,
            ),
            session=session
        )

    except sa_exc.IntegrityError:
        raise exceptions.UsernameIsTaken() from None
    
    return r.SignUpDTO(
        username=new_user.username,
        password=new_user.password,
        created_at=new_user.created_at
    )
