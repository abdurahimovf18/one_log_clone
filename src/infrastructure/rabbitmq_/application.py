from faststream import FastStream
from faststream.rabbit import RabbitBroker


def create_application(
    user: str,
    password: str,
    host: str,
    port: int,
) -> FastStream:
    url = f"amqp://{user}:{password}@{host}:{port}"
    broker = RabbitBroker(url=url)    

    return FastStream(
        broker=broker
    )



