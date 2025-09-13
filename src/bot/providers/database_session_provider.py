from collections.abc import AsyncGenerator
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import session_factory


class DatabaseSessionProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession, object]:
        """
        A generator that yields database session
        """
        async with session_factory() as session:
            yield session
