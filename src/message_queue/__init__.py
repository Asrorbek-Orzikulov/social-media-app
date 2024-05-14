import pika

from src.config import settings

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=settings.rabbit_host,
        port=settings.rabbit_port,
        credentials=pika.PlainCredentials(
            username=settings.rabbit_username,
            password=settings.rabbit_password,
            erase_on_connect=True,
        ),
    )
)
channel = connection.channel()
