import json
import pika
from pika import BlockingConnection, URLParameters, BasicProperties

from producer_app.core.config import RABBITMQ_URL, EXCHANGE_NAME, EXCHANGE_TYPE, QUEUE_NAME
from producer_app.models.order import Order


def publish_order(order: Order) -> None:
    """
    Serialize the Order as JSON and publish it to the RabbitMQ exchange.
    """

    params = URLParameters(RABBITMQ_URL)
    connection: BlockingConnection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Idempotent: if the exchange already exists with same type, this is safe.
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        durable=True,
    )

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    routing_key = order.status
    channel.queue_bind(
        queue=QUEUE_NAME,
        exchange=EXCHANGE_NAME,
        routing_key=routing_key
    )



    body_bytes = order.model_dump_json().encode("utf-8")


    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=body_bytes,
        properties=BasicProperties(
            content_type="application/json",
            delivery_mode=2,  # persistent
            headers={"event_type": "order.created"},
        ),
    )

    connection.close()
