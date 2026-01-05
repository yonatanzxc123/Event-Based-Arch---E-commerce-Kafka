import random
import string
from datetime import datetime, timezone
from typing import List

from producer_app.models.order_input import CreateOrderInput
from producer_app.models.order import Order
from producer_app.models.order_item import OrderItem


def _random_customer_id(prefix: str = "CUST", length: int = 6) -> str:
    chars = string.ascii_uppercase + string.digits
    return f"{prefix}-" + "".join(random.choices(chars, k=length))


def generate_order(data: CreateOrderInput) -> Order:
    items: List[OrderItem] = []

    # We guarantee uniqueness per order by using the index in the ID
    for i in range(1, data.itemCount + 1):
        item_id = f"ITEM-{i:04d}"  # ITEM-0001, ITEM-0002, ...

        quantity = random.randint(1, 5)          # random quantity > 0
        price = round(random.uniform(5.0, 120.0), 2)  # random price

        items.append(
            OrderItem(
                itemId=item_id,
                quantity=quantity,
                price=price,
            )
        )

    total = round(sum(it.quantity * it.price for it in items), 2)

    order = Order(
        orderId=data.orderId,
        customerId=_random_customer_id(),
        orderDate=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        items=items,
        totalAmount=total,
        currency="USD",
        status="new",
    )

    return order
