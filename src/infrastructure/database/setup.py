from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from src.config.settings import DATABASE_URL

engine = create_async_engine(
    url=DATABASE_URL,
    pool_class=NullPool,  # PgBouncer manages pools
)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, autoflush=False, 
    autocommit=False, expire_on_commit=False
)

metadata = MetaData()


class Base(DeclarativeBase): 
    metadata = metadata
