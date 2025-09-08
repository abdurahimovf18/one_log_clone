# import uuid
# from datetime import datetime

# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.core.queries import users

# from src.core.domain_schema.models import User


# @pytest.mark.parametrize(
#     "id, username, created_at, updated_at, result",
#     [
#         (
#             uuid.uuid4(), None, None, None, False
#         ),
#         (
#             None, "jane_doe", None, None, False
#         ),
#         (
#             None, None, datetime(2023, 1, 1), None, False
#         ),
#         (
#             None, None, None, datetime(2023, 1, 1), False
#         ),
#         (
#             None, "jane_doe", datetime(2023, 1, 1), None, False
#         )
#     ]
# )
# async def test_exists(
#         session: AsyncSession,
#         id: uuid.UUID | None,
#         username: str | None,
#         created_at: datetime | None,
#         updated_at: datetime | None,
#         result: bool,
#     ):

#     user_exists = await users.exists(
#         users.p.ExistsDTO(
#             id=id,
#             username=username,
#             created_at=created_at,
#             updated_at=updated_at,
#         ),
#         session=session
#     )
#     assert isinstance(user_exists, bool)
#     assert user_exists == result



# @pytest.mark.parametrize(
#     ""
# )
