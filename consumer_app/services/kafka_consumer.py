import json
import os
import threading
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from consumer_app.services.order_store import order_store
from consumer_app.models.order import Order
from consumer_app.models.stored_order import StoredOrder

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = "order_events"

# To track received IDs for the /getAllOrderIdsFromTopic requirement
received_orders_log = []


def process_message(message_value):
    """
    Handle the logic: calculate shipping, save to store.
    """
    try:
        data = message_value
        order_id = data.get("orderId")

        # Log it for the requirement
        received_orders_log.append(order_id)

        # Logic from Ex1
        # If it's a "create" (full order) vs "update" (partial info)
        # You might need logic here to check if order exists in store.

        # Simplified:
        if data.get("items"):
            # It's likely a full order
            order = Order(**data)
            shipping_cost = round(order.totalAmount * 0.02, 2)
            stored = StoredOrder(order=order, shippingCost=shipping_cost)
            order_store.save(stored)
            print(f"Processed Create/Full Order: {order_id}")
        else:
            # It's an update
            existing = order_store.get(order_id)
            if existing:
                existing.order.status = data.get("status")
                order_store.save(existing)
                print(f"Processed Update Order: {order_id} to {data.get('status')}")

    except Exception as e:
        print(f"Error processing message: {e}")


def start_consumer():
    while True:
        try:
            print("Attempting to connect to Kafka...")
            consumer = KafkaConsumer(
                TOPIC_NAME,

                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            print("Connected to Kafka!")

            for message in consumer:
                process_message(message.value)

        except NoBrokersAvailable:
            print("Kafka not available yet, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Consumer error: {e}")
            time.sleep(5)


def start_consumer_in_background():
    t = threading.Thread(target=start_consumer, daemon=True)
    t.start()