import json
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
from producer_app.models.order import Order

# Get Kafka URL from env (default to localhost for local dev, kafka:29092 for docker)
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = "order_events"

# Initialize Producer (Global variable)
producer = None


def get_producer():
    global producer
    if producer is None:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
        except KafkaError as e:
            print(f"Error connecting to Kafka: {e}")
            raise e
    return producer


def publish_order_event(order: Order, event_type: str = "order_created"):
    prod = get_producer()

    # We use the orderId as the KEY.
    # This guarantees that all updates for "Order-123" land in the same partition
    # and are processed in order by the consumer.
    prod.send(
        topic=TOPIC_NAME,
        key=order.orderId,
        value=order.model_dump()
    )
    prod.flush()