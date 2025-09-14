from sqlalchemy import exc as sa_exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.use_cases import users as p
from src.core.data_transfer_objects.responses.use_cases import users as r
from src.core.exceptions.use_cases import users as exceptions
from src.core.queries import feedbacks, messages, tg_users, user_auth, users
from src.utils.auth import hash_password, verify_password


# TODO: implement caching for this function.
async def get_current_message(
        data: p.GetCurrentMessageDTO, *, session: AsyncSession,
        ) -> r.GetCurrentMessageDTO:
    
    last_created_message_info = await messages.get_created_message(
        messages.p.GetCreatedMessageDTO(owner_id=data.user_id), session=session
    )

    if last_created_message_info is not None:
        return r.GetCurrentMessageDTO(
            id=last_created_message_info.id,
            text_id=last_created_message_info.text_id,
            owner_id=last_created_message_info.owner_id,
            interval=last_created_message_info.interval,
            duration=last_created_message_info.duration
        )
    
    new_message_info = await messages.create(
        messages.p.CreateDTO(owner_id=data.user_id), session=session
    )
    return r.GetCurrentMessageDTO(
        id=new_message_info.id,
        text_id=new_message_info.text_id,
        owner_id=new_message_info.owner_id,
        interval=new_message_info.interval,
        duration=new_message_info.duration
    )


async def accept_feedback(
        data: p.AcceptFeedbackDTO, *, session: AsyncSession
    ) -> r.AcceptFeedbackDTO:
    
    feedback_info = await feedbacks.create(
        feedbacks.p.CreateDTO(
            chat_id=data.chat_id,
            user_id=data.user_id,
            reply_message_id=data.reply_message_id,
            status=data.status,
            message=data.message,
        ),
        session=session
    )

    return r.AcceptFeedbackDTO(
        id=feedback_info.id,
        status=feedback_info.status
    )


async def register_tg_user(
        data: p.RegisterTgUserDTO, *, session: AsyncSession
    ) -> r.RegisterTgUserDTO:
    tg_user = await tg_users.create(
        tg_users.p.CreateDTO(
            chat_id=data.chat_id,
            language=data.language
        ),
        session=session
    )

    return r.RegisterTgUserDTO.construct_from_dto(tg_user)
    

async def set_user_language():
    pass


async def signin(data: p.SignInDTO, *, session: AsyncSession) -> r.SignInDTO:
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


async def signup(data: p.SignUpDTO, *,session: AsyncSession) -> r.SignUpDTO:
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
