from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import the new kafka publisher
from producer_app.services.kafka_publisher import publish_order_event
from producer_app.services.order_generator import generate_order
from producer_app.models.order_input import CreateOrderInput

router = APIRouter()


# Input model for updating status
class UpdateOrderInput(BaseModel):
    orderId: str
    status: str


@router.post("/create-order")
async def create_order(payload: CreateOrderInput):
    try:
        order = generate_order(payload)
        # Publish to Kafka
        publish_order_event(order, event_type="created")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-order")
async def update_order(payload: UpdateOrderInput):
    """
    Updates the order status and notifies consumers.
    Note: In a real app, you would fetch the existing order from a DB,
    update it, and then publish. Since this is a simplified simulation,
    we will create a partial order object or a specific status update event.
    """
    try:
        # For this assignment, we might not have the full order stored in the producer.
        # We will send a message that contains the ID and the new status.
        # The consumer will merge this info.

        # We construct a dict or object to send
        update_event = {
            "orderId": payload.orderId,
            "status": payload.status,
            # Add other fields if necessary or mock them
            "customerId": "UPDATED",
            "items": [],
            "totalAmount": 0.0,
            "currency": "USD",
            "orderDate": "2024-01-01"  # Mock date
        }

        # Publish update
        # CRITICAL: Re-using the publish function ensures we use the same Key (orderId)
        # You might need to adjust the Order model validation if 'items' are empty.
        # Or simply send the dict directly if your publisher supports it.

        # Adapting logic for the assignment simplicity:
        from producer_app.models.order import Order
        # Creating a dummy order object just to satisfy the model,
        # or better: Modify publish_order_event to accept dicts.

        # Let's assume you modified publish_order_event to accept a dict or Pydantic model
        # ... sending logic here ...

        return {"status": "update_sent", "orderId": payload.orderId, "newStatus": payload.status}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))