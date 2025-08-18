from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import session_factory


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
