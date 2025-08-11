from collections.abc import AsyncGenerator

from aiogram import Dispatcher
from dishka import Provider, Scope, make_async_container, provide  # type: ignore
from dishka.integrations.aiogram import AiogramProvider, setup_dishka
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import session_factory


class DatabaseSessionProvider(Provider):
    """
    Dishka provider responsible for creating a fresh SQLAlchemy AsyncSession
    for each incoming update in the aiogram bot.

    This provider uses Scope.REQUEST, meaning:
        - A new session is created for each update (message, callback, etc.)
        - The same session instance is shared across all injections in that update
        - The session is automatically closed after the update is processed

    Benefits:
        - Prevents session reuse between updates (avoiding stale connections)
        - Automatically cleans up resources
        - Works in both handlers and filters via dependency injection
    """

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncGenerator[AsyncSession, object]:
        """
        Creates and yields a fresh AsyncSession for the current request (update).

        This method:
            - Opens a new database session using the application's session_factory
            - Yields it for use inside handlers and filters
            - Ensures proper cleanup/closing of the session after the request finishes

        Returns:
            AsyncGenerator[AsyncSession, object]: 
                The yielded SQLAlchemy AsyncSession bound to the request's lifecycle
        """
        async with session_factory() as session:
            yield session


def register_provider(dispatcher: Dispatcher) -> None:
    """
    Registers Dishka providers and integrates them with aiogram.

    Steps performed:
        1. Creates an async dependency container with:
            - DatabaseSessionProvider (DB sessions per request)
            - AiogramProvider (provides aiogram context objects for DI)
        2. Sets up Dishka to auto-inject dependencies into handlers and filters
        3. Registers container cleanup on dispatcher shutdown

    Args:
        dispatcher (Dispatcher): 
            The aiogram Dispatcher instance to register the container with.
    """
    container = make_async_container(
        DatabaseSessionProvider(),
        AiogramProvider()
    )
    setup_dishka(
        container=container,
        router=dispatcher,
        auto_inject=True
    )
    dispatcher.shutdown.register(container.close)
