"""Order rules independent of HTTP, so web and future app clients share them."""

from datetime import datetime, timezone
from threading import RLock
from .catalog import MENU_BY_ID


class OrderError(ValueError):
    pass


class OrderNotFound(LookupError):
    pass


class OrderService:
    def __init__(self, repository):
        self.repository = repository
        self._lock = RLock()

    def list_orders(self):
        with self._lock:
            return self.repository.list()

    def get_order(self, order_id):
        with self._lock:
            for order in self.repository.list():
                if order["id"] == order_id:
                    return order
        raise OrderNotFound("ไม่พบออเดอร์นี้")

    def create_order(self, payload):
        if not isinstance(payload, dict):
            raise OrderError("ข้อมูลคำสั่งซื้อต้องเป็น JSON object")
        name = str(payload.get("name", "")).strip()[:50]
        requested = payload.get("items", [])
        if not name or not isinstance(requested, list) or not requested:
            raise OrderError("กรุณาระบุชื่อและรายการอาหาร")
        if len(requested) > 50:
            raise OrderError("หนึ่งออเดอร์เลือกอาหารได้ไม่เกิน 50 รายการ")
        items = []
        for requested_item in requested:
            if not isinstance(requested_item, dict):
                raise OrderError("พบรายการอาหารที่ไม่ถูกต้อง")
            menu_id = requested_item.get("menuId")
            qty = requested_item.get("qty")
            if type(menu_id) is not int or type(qty) is not int:
                raise OrderError("รหัสเมนูและจำนวนต้องเป็นจำนวนเต็ม")
            food = MENU_BY_ID.get(menu_id)
            if food is None:
                raise OrderError("ไม่พบเมนูอาหารที่เลือก")
            if qty < 1 or qty > 99:
                raise OrderError("จำนวนอาหารต้องอยู่ระหว่าง 1 ถึง 99")
            items.append({"name": food["name"], "qty": qty, "price": food["price"]})
        with self._lock:
            orders = self.repository.list()
            order_id = max((int(order["id"]) for order in orders), default=0) + 1
            order = {
                "id": order_id,
                "name": name,
                "items": items,
                "total": sum(item["qty"] * item["price"] for item in items),
                "createdAt": datetime.now(timezone.utc).isoformat(),
                # New orders are accepted by the kitchen automatically.
                "status": "preparing",
            }
            orders.insert(0, order)
            self.repository.save(orders)
        return order

    def complete_order(self, order_id):
        with self._lock:
            orders = self.repository.list()
            for order in orders:
                if order["id"] == order_id:
                    order["status"] = "ready"
                    self.repository.save(orders)
                    return order
        raise OrderNotFound("ไม่พบออเดอร์")

    def delete_order(self, order_id):
        with self._lock:
            orders = self.repository.list()
            remaining = [order for order in orders if order["id"] != order_id]
            if len(remaining) == len(orders):
                raise OrderNotFound("ไม่พบออเดอร์")
            self.repository.save(remaining)

    def reset_orders(self):
        """Clear all stored orders as one locked repository operation."""
        with self._lock:
            orders = self.repository.list()
            self.repository.save([])
            return len(orders)
