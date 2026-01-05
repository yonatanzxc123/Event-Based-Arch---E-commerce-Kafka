

*)Producer URL : http://localhost:8000/create-order  - Creates a new order (HTTP POST request) and publish it to RabbitMQ
also the user needs a body with order ID and item count
EX:
{
  "orderId": "Order-123",
  "itemCount": 5
}

*)Consumer URL: http://localhost:8001/order-details?orderId=Order-123   (you can replace the Order-123 with the relevant order ID)
this returns the stored order +computed shipping cost (GET HTTP request)



*)bash start commands :
docker compose -f producer.yml up
docker compose -f consumer.yml up


*)Exchange type and why I used it : 

the exchange type I chose is - topic

why ?  the topic exchange provides a flexible and scalable routing mechanism.
While in the task at hand we are requried to broadcast every message to our current consumers, a topic exchange allows us to use specific routing keys (such as order status, "new").
And this ensures every consumer receives all relevant order events as requried by the task, but also provides flexibility for future microservices to only subscribe to some events (e.g., "shipped" status and such). 
This models a scalable event-driven architecture pattern. (like we were tought in class)


*)Rergarding the binding key -

I usedd the order status (e.g., "new") as the binding key.
 This key is used to bind the consumer's queue to the topic exchange, which ensures all messages with that specific status are delivered to the queue.



*)The service that delclated the exchange  - Both the Producer and the Consumer declare the exchange and the queue

The producer ensures the exchange exists before any message is published, whcih guarantees no message failure.
And the consumer defines its own queue and binding logic.
I chose this approach because it ensures that everyone gets the messages as the declaration operations are idempotent!.
This means running the declaration from both sides is safe and cannot hurt the system configuration.
Its simply ensures the infrastructure exists regardless of which service starts first, making the system I built highly resilient and robust.








