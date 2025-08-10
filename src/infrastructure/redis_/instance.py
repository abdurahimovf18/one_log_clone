from redis.asyncio import Redis

from src.config.settings import env


def create_instance(
    host: str = env.REDIS_HOST,
    port: int = env.REDIS_PORT,
    db: int = env.REDIS_DB,
    password: str | None = env.REDIS_PASSWORD,
) -> Redis:
    return Redis(
        host=host,
        port=port,
        password=password,
        db=db
    )
