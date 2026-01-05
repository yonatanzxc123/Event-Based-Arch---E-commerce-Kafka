from typing import List
from pydantic import BaseModel

from consumer_app.models.order_item import OrderItem


class Order(BaseModel):
    orderId: str
    customerId: str
    orderDate: str
    items: List[OrderItem]
    totalAmount: float
    currency: str
    status: str
