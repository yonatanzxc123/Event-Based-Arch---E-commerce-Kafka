from typing import Dict, Optional
from consumer_app.models.stored_order import StoredOrder


class OrderStore:
    def __init__(self) -> None:
        self._store: Dict[str, StoredOrder] = {}

    def save(self, stored: StoredOrder) -> None:
        self._store[stored.order.orderId] = stored

    def get(self, order_id: str) -> Optional[StoredOrder]:
        return self._store.get(order_id)


# Single global instance
order_store = OrderStore()
