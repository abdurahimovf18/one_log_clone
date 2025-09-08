from redis.asyncio import Redis


def create_instance(
    host: str,
    port: int,
    db: int,
    password: str | None = None,
) -> Redis:
    return Redis(
        host=host,
        port=port,
        password=password,
        db=db
    )
