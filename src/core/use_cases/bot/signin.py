# from sqlalchemy.ext.asyncio import AsyncSession

# # from sqlalchemy import exc as sa_exc
# from src.core.data_transfer_objects.paramters.use_cases.bot import auth as p
# from src.core.data_transfer_objects.prepared.models import UserOptionalDTO
# from src.core.data_transfer_objects.responses.use_cases.bot import auth as r
# from src.core.exceptions import common as common_exceptions
# from src.core.exceptions.use_cases import bot as exceptions
# from src.core.queries import user_auth, users
# from src.utils.auth import verify_password


# async def get_user(
#         username: str, 
#         session: AsyncSession
#     ) -> UserOptionalDTO:
#     """
#     Returns A user object.
#     """
#     user = await users.get_password_by_username(
#         users.p.GetPasswordByUsername(username=username),
#         session=session
#     )

#     if user is None:
#         raise exceptions.UsernameNotFound()
    
#     return UserOptionalDTO.construct_from_dto(user)


# def validate_user_password(
#         user: UserOptionalDTO, 
#         password: str
#     ) -> None:
#     """
#     Validates user password and raises exception if the password is incorrect.

#     raises:
#         PasswordIncorrect: if password does not match.
#     """

#     if user.password is None:
#         raise common_exceptions.Development("user must have a valid field password but got None.")

#     if not verify_password(user.password, password):  # if (password is incorrect)
#         raise exceptions.PasswordIncorrect()
    

async def execute():
    pass
    
# async def execute(data: p.SignInDTO, *, session: AsyncSession) -> r.SignInDTO:
#     """
#     Checks user arguements and logins user, If something gone wrong raises exceptions.

#     Raises:
#         UsernameNotFound: if User with this username is not found.
#         PasswordIncorrect: if password does not match.
#         Exception: If not handled exception occures.
#     """
#     user = await get_user(username=data.username, session=session)

#     validate_user_password(user=user, password=data.password)

#     if user.id is None:
#         raise common_exceptions.Development(f"user.id must not be None, got {user.id=}")

#     auth = await user_auth.create(
#         user_auth.p.CreateDTO(user_id=user.id, chat_id=data.chat_id),
#         session=session
#     )
    
#     return r.SignInDTO(
#         user_id=auth.user_id,
#         chat_id=auth.chat_id,
#     )
