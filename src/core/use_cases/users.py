from sqlalchemy import exc as sa_exc
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.use_cases import users as p
from src.core.data_transfer_objects.responses.use_cases import users as r
from src.core.exceptions.use_cases import users as exceptions
from src.core.queries import feedbacks, messages, texts, tg_users, user_auth, users
from src.models.shared.enums import MessageStatus
from src.utils.auth import hash_password, verify_password


# TODO: implement caching for this function.
async def get_created_message(
        data: p.GetCreatedMessageDTO, *, session: AsyncSession,
    ) -> r.GetCreatedMessageDTO:

    # try to get last message
    last_message_info = await messages.get_last_by_owner_id(
        messages.p.GetLastByOwnerIdDTO(owner_id=data.owner_id), session=session
    )

    # if last message does not exist or it's status is not "CREATED", then try to create 
    # a new message and return new message's data
    if last_message_info is None or last_message_info.status != MessageStatus.CREATED:
        new_message_info = await messages.create(
            messages.p.CreateDTO(owner_id=data.owner_id), session=session
        )
        return r.GetCreatedMessageDTO.model_validate(new_message_info)
    else: # if last message is ok, then return old message's data
        return r.GetCreatedMessageDTO.model_validate(last_message_info)    
        

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


async def update_message_text(data: p.UpdateMessageTextDTO, *, session: AsyncSession) -> None:
    message_info = await get_created_message(
        p.GetCreatedMessageDTO(owner_id=data.user_id), session=session
    )

    if message_info.text_id is None:
        text_info = await texts.create(texts.p.CreateDTO(content=data.text), session=session)

        await messages.update_text_id_by_id(
            messages.p.UpdateTextIdByIdDTO(id=message_info.id, text_id=text_info.id), 
            session=session
        )

    else:
        await texts.update_content_by_id(
            texts.p.UpdateContentByIdDTO(id=message_info.text_id, content=data.text), 
            session=session
        )    
