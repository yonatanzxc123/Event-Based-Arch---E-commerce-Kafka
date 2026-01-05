import os

# In dev, we'll talk to RabbitMQ on localhost.
# In Docker, we'll override this with an environment variable (host "rabbitmq").
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

# Exchange for order events
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "orders.events")
EXCHANGE_TYPE = "topic"  # broadcast to all bound queues

BINDING_KEY = os.getenv("BINDING_KEY", "new")
QUEUE_NAME = os.getenv("QUEUE_NAME", "order-service.new")
