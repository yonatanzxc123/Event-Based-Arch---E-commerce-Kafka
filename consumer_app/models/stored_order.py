from pydantic import BaseModel
from consumer_app.models.order import Order


class StoredOrder(BaseModel):
    order: Order
    shippingCost: float
