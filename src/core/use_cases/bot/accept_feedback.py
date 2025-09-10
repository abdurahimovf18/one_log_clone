from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.paramters.use_cases import bot as p
from src.core.data_transfer_objects.responses.use_cases import bot as r
from src.core.queries import feedbacks


async def execute(data: p.AcceptFeedbackDTO, *, session: AsyncSession) -> r.AcceptFeedbackDTO:
    
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