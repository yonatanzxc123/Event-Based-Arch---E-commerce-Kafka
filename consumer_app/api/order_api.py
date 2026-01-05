from fastapi import APIRouter, HTTPException, Query

from consumer_app.services.order_store import order_store

router = APIRouter()


@router.get("/order-details")
async def get_order_details(orderId: str = Query(..., min_length=1)):
    stored = order_store.get(orderId)
    if not stored:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order": stored.order,
        "shippingCost": stored.shippingCost,
    }
