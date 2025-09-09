from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.use_cases.bot import auth as p
from src.core.data_transfer_objects.responses.use_cases.bot import auth as r
from src.core.exceptions.use_cases import bot as exceptions
from src.core.queries import tg_users, user_auth
from src.utils.auth import verify_password


async def execute(data: p.SignInDTO, *, session: AsyncSession) -> r.SignInDTO:
    """
    Checks user arguements and logins user, If something gone wrong raises exceptions.

    Raises:
        UsernameNotFound: if User with this username is not found.
        PasswordIncorrect: if password does not match.
        Exception: If not handled exception occures.
    """

    user = await user_auth.get_password_by_username(
        user_auth.p.GetPasswordByUsername(
            username=data.username
        ),
        session=session
    )

    if user is None:
        raise exceptions.UsernameNotFound()
    
    if not verify_password(user.password, data.password):
        raise exceptions.PasswordIncorrect()
    
    await tg_users.set_user_id_by_chat_id(
        tg_users.p.SetUserIdByChatId(
            chat_id=data.chat_id, user_id=user.user_id,
        ),
        session=session
    )

    return r.SignInDTO()
