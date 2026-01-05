from pydantic import BaseModel


class OrderItem(BaseModel):
    itemId: str
    quantity: int
    price: float
