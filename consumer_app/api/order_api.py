from fastapi import APIRouter
from consumer_app.services.kafka_consumer import received_orders_log

router = APIRouter()

# ... existing /order-details endpoint ...

@router.get("/getAllOrderIdsFromTopic")
async def get_all_orders_from_topic(topic: str):
    # In a real app, you'd filter by topic if you subscribed to multiple.
    # Since we only have one topic here, we return the log.
    return {"topic": topic, "received_orders": received_orders_log}