from aiogram import Dispatcher
from dishka import Provider, make_async_container
from dishka.integrations.aiogram import setup_dishka

from .current_user_provider import CurrentUserProvider
from .database_session_provider import DatabaseSessionProvider

providers: list[Provider] = [  # type: ignore
    CurrentUserProvider(),
    DatabaseSessionProvider(),
]


def register_providers(dispatcher: Dispatcher) -> None:
    """
    A function which registers providers counted at global providers.
    """

    # Creating container based on providers
    container = make_async_container(*providers)

    # Setting up dishka
    setup_dishka(container=container, router=dispatcher, auto_inject=True)
    
    # Registering container close at dispatcher shutdown
    dispatcher.shutdown.register(container.close)
