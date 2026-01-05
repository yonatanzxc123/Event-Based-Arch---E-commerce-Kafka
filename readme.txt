Student Name: Yehonatan Segev
ID:

*)Producer URL : http://localhost:8000/create-order  - Creates a new order (HTTP POST request) and publish it to RabbitMQ
also the user needs a body with order ID and item count
EX:
{
  "orderId": "Order-123",
  "itemCount": 5
}


- API Endpoints:
    1. POST /create-order
        Payload: { "orderId": "Order-123", "itemCount": 5 }
        Description: Validates input, generates a full order object, and publishes a "Creation" event to Kafka.
     2. POST /update-order
        Payload: { "orderId": "Order-123", "status": "shipped" }
        Description: Updates the order status and publishes an "Update" event to Kafka to notify consumers.



*)Consumer URL: http://localhost:8001/order-details?orderId=Order-123   (you can replace the Order-123 with the relevant order ID)
this returns the stored order +computed shipping cost (GET HTTP request)

- API Endpoints:

     1. GET /order-details?orderId=Order-123
        Description: Returns the stored order details (including calculated shipping cost) from the in-memory store.
     2. GET /getAllOrderIdsFromTopic?topic=order_events
        Description: Returns a list of all order IDs processed from the specified Kafka topic.



*)bash start commands :
docker compose -f producer.yml up
docker compose -f consumer.yml up



*) Kafka Topics & Purpose :

Topic Name: order_events

Purpose:
I used a single topic named 'order_events' to handle the entire lifecycle of an order.
Both "Order Created" events (containing the full order data) and "Order Updated" events
(containing just the new status) are published to this same topic.
The Consumer distinguishes between them based on the payload structure (checking if 'items' exists)
and processes them sequentially to maintain the correct state.


*) Message keys:

Key Used: orderId

Why did I choose this key?
Kafka guarantees strict ordering of messages only within a specific partition.
By setting the message key to the 'orderId', I ensure that all events related to a
specific order (e.g., "Order-123") are hashed to the exact same partition.

This is critical for data consistency. It guarantees that the Consumer will always
read the "Create" event before the "Update" event for that order. If I had used a
random key (or null), the events might have landed on different partitions and could
have been processed out of order, causing the update to fail.


*)Rergarding the binding key -

I usedd the order status (e.g., "new") as the binding key.
 This key is used to bind the consumer's queue to the topic exchange, which ensures all messages with that specific status are delivered to the queue.



*)Error handling & Strategies

1. Connection Resilience (Consumer Startup):
   - Problem: The Consumer service might start up faster than the Kafka container, causing a crash.
   - Solution: I wrapped the connection logic in a 'while True' loop with a 'try-except' block specifically catching 'NoBrokersAvailable'.
   - Why: This allows the Consumer to wait and retry automatically until Kafka is ready, making the 'docker-compose' startup sequence reliable without manual intervention.

2. API & Publishing Reliability (Producer):
   - Problem: Kafka might be temporarily unavailable when a user tries to create an order.
   - Solution: The API endpoints utilize 'try-except' blocks around the 'publish_order_event' call. If publishing fails, I catch the exception and return a specific HTTP 500 error to the client with a descriptive message.
   - Why: This ensures the API fails gracefully and informs the client of the issue, rather than crashing the Producer application internally.

3. Message Processing Safety (Consumer Loop):
   - Problem: A single malformed message could crash the Consumer, stopping it from processing valid messages.
   - Solution: Inside the main consumption loop ('process_message'), I wrapped the logic in a 'try-except' block.
   - Why: If a bad message arrives, the error is printed to the logs, but the loop continues. This ensures high availability for the service.





