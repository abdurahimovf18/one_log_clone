from sqlalchemy.ext.asyncio import AsyncSession

from src.core.data_transfer_objects.common import PageDTO
from src.core.data_transfer_objects.paramters.queries import tg_accounts as p
from src.core.data_transfer_objects.responses.queries import tg_accounts as r
from src.models import TgAccount
from src.utils.pagination import Pagination

model = TgAccount


async def get_page_by_user_id(
        data: p.GetPageByUserIdDTO, *, session: AsyncSession
    ) -> PageDTO[r.GetPageByUserIdDTO]:
    
    pagination = Pagination(
        model=model,
        load_only_fields={model.session_id, model.phone},
        items_per_page=10
    )
    page = pagination.create_page(data.page, session=session, filters={"user_id": data.user_id})

    dict_items = await page.get_items()
    return PageDTO[r.GetPageByUserIdDTO](
        items=[r.GetPageByUserIdDTO.model_validate(item) for item in dict_items],
        page=data.page,
        items_per_page=page.items_per_page,
        is_next=await page.is_next(),
        is_prev=await page.is_prev(),
        items_count=len(dict_items),
        pages_count=await page.get_pages_count()
    )
    