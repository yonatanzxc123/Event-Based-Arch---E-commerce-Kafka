from fastapi import APIRouter, HTTPException, Query
from consumer_app.services.order_store import order_store
from consumer_app.services.kafka_consumer import received_orders_log

router = APIRouter()

# --- Endpoint 1: Get Order Details (from memory) ---
@router.get("/order-details")
async def get_order_details(orderId: str = Query(..., min_length=1)):
    stored = order_store.get(orderId)
    if not stored:
        # Return 404 if not found in memory
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order": stored.order,
        "shippingCost": stored.shippingCost,
    }

# --- Endpoint 2: Get Topic Log (from Kafka consumer log) ---
@router.get("/getAllOrderIdsFromTopic")
async def get_all_orders_from_topic(topic: str):
    return {"topic": topic, "received_orders": received_orders_log}