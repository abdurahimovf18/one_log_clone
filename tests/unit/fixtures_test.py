from sqlalchemy.ext.asyncio import AsyncSession


async def test_session_fixture(session: AsyncSession):
    assert session, (
        f"Session fixture must return sqlalchemy.ext.asyncio."
        f"AsyncSession object, but got {session=}"
    )