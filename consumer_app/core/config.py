import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "orders.events")
EXCHANGE_TYPE = "topic"
# The queue used by this consumer
QUEUE_NAME = os.getenv("QUEUE_NAME", "order-service.new")

# Binding key for this consumer – status "new"
BINDING_KEY = os.getenv("BINDING_KEY", "new")