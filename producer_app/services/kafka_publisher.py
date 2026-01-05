import json
import os
from typing import Union, Dict, Any
from kafka import KafkaProducer
from kafka.errors import KafkaError
from producer_app.models.order import Order

# Get Kafka URL from env
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


def publish_order_event(order_data: Union[Order, Dict[str, Any]], event_type: str = "order_created"):
    prod = get_producer()

    # 1. Determine the Order ID (Key)
    if isinstance(order_data, Order):
        key_id = order_data.orderId
        value_payload = order_data.model_dump()
    else:
        # It's a dictionary (for updates)
        key_id = order_data.get("orderId")
        value_payload = order_data

    # 2. Publish
    # We use the orderId as the KEY to guarantee partition ordering.
    prod.send(
        topic=TOPIC_NAME,
        key=key_id,
        value=value_payload
    )
    prod.flush()