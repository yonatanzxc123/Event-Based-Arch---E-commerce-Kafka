from fastapi import APIRouter, HTTPException

from producer_app.models.order_input import CreateOrderInput
from producer_app.services.order_generator import generate_order
from producer_app.services.rabbitmq_publisher import publish_order

router = APIRouter()


@router.post("/create-order")
async def create_order(payload: CreateOrderInput):
    """
    1. Validate input (orderId, itemCount)
    2. Generate full Order object
    3. Publish Order to RabbitMQ as a JSON event
    4. Return the Order in the HTTP response
    """
    try:
        order = generate_order(payload)
    except ValueError as ve:
        # Business validation error
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal error while creating order")

    # Publish to RabbitMQ
    try:
        publish_order(order)
    except Exception as e:
        # If publishing fails, we report 500 (per assignment: handle errors with non-200 codes)
        raise HTTPException(status_code=500, detail=f"Failed to publish order event: {e}")

    return order
