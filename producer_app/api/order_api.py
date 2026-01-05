from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Import the kafka publisher
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
        # Publish to Kafka (Full Order Object)
        publish_order_event(order, event_type="created")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-order")
async def update_order(payload: UpdateOrderInput):
    """
    Updates the order status and notifies consumers.
    """
    try:
        # We construct a dict for the update event.
        # This structure ensures the Consumer treats it as an 'update' (because items is empty).
        update_event = {
            "orderId": payload.orderId,
            "status": payload.status,
            "customerId": "UPDATED",
            "items": [],  # Empty list -> Consumer sees this as False and triggers 'Update' logic
            "totalAmount": 0.0,
            "currency": "USD",
            "orderDate": "2026-01-01"
        }

        # Publish update
        # CRITICAL: This now passes a dictionary.
        # Your updated kafka_publisher.py must handle 'isinstance(order_data, Order)' checks.
        publish_order_event(update_event, event_type="updated")

        return {"status": "update_sent", "orderId": payload.orderId, "newStatus": payload.status}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish update: {str(e)}")