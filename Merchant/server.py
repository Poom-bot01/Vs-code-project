"""HTTP transport for the website and future mobile/API clients."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
from urllib.parse import urlparse

from lamoon.catalog import MENU
from lamoon.orders import OrderError, OrderNotFound, OrderService
from lamoon.repository import JsonOrderRepository
from lamoon.reset_scheduler import DataResetScheduler

ROOT = Path(__file__).resolve().parent
ORDERS = OrderService(JsonOrderRepository(ROOT / "orders.json"))
RESET_SCHEDULER = DataResetScheduler(ORDERS, ROOT / "data_reset_schedule.json")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        if urlparse(self.path).path.startswith("/api/"):
            # Enables future browser-based app clients; native apps can call the same JSON API.
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def send_json(self, status, data):
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def body_json(self):
        size = int(self.headers.get("Content-Length", "0"))
        if size < 0 or size > 100_000:
            raise ValueError("ข้อมูลมีขนาดใหญ่เกินไป")
        return json.loads(self.rfile.read(size) or b"{}")

    def api_path(self):
        path = urlparse(self.path).path
        return path if path.startswith("/api/v1/") else None

    def do_OPTIONS(self):
        if self.api_path():
            self.send_response(204)
            self.end_headers()
        else:
            self.send_error(404)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/v1/menu":
            return self.send_json(200, MENU)
        if path == "/api/v1/orders":
            return self.send_json(200, ORDERS.list_orders())
        if path.startswith("/api/v1/orders/"):
            try:
                order_id = int(path.rsplit("/", 1)[1])
                return self.send_json(200, ORDERS.get_order(order_id))
            except ValueError:
                return self.send_json(400, {"error": "หมายเลขออเดอร์ไม่ถูกต้อง"})
            except OrderNotFound as error:
                return self.send_json(404, {"error": str(error)})
        if path == "/api/v1/health":
            return self.send_json(200, {"status": "ok", "apiVersion": 1})
        if path == "/":
            self.path = "/order_food.html"
        elif path == "/admin":
            self.path = "/admin.html"
        return super().do_GET()

    def do_POST(self):
        if self.api_path() != "/api/v1/orders":
            return self.send_json(404, {"error": "ไม่พบ API นี้"})
        try:
            order = ORDERS.create_order(self.body_json())
        except OrderError as error:
            return self.send_json(400, {"error": str(error)})
        except (ValueError, json.JSONDecodeError):
            return self.send_json(400, {"error": "ข้อมูลที่ส่งมาไม่ถูกต้อง"})
        return self.send_json(201, order)

    def do_PATCH(self):
        path = self.api_path()
        try:
            if not path or not path.startswith("/api/v1/orders/"):
                return self.send_json(404, {"error": "ไม่พบ API นี้"})
            order_id = int(path.rsplit("/", 1)[1])
            payload = self.body_json()
            if not isinstance(payload, dict):
                return self.send_json(400, {"error": "ข้อมูลสถานะไม่ถูกต้อง"})
            if payload.get("status") != "ready":
                return self.send_json(400, {"error": "สถานะไม่ถูกต้อง"})
            return self.send_json(200, ORDERS.complete_order(order_id))
        except (ValueError, json.JSONDecodeError):
            return self.send_json(400, {"error": "คำขอไม่ถูกต้อง"})
        except OrderNotFound as error:
            return self.send_json(404, {"error": str(error)})

    def do_DELETE(self):
        path = self.api_path()
        try:
            if not path or not path.startswith("/api/v1/orders/"):
                return self.send_json(404, {"error": "ไม่พบ API นี้"})
            order_id = int(path.rsplit("/", 1)[1])
            ORDERS.delete_order(order_id)
            return self.send_json(200, {"ok": True})
        except ValueError:
            return self.send_json(400, {"error": "หมายเลขออเดอร์ไม่ถูกต้อง"})
        except OrderNotFound as error:
            return self.send_json(404, {"error": str(error)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    RESET_SCHEDULER.start()
    print(f"Website: http://localhost:{port}/order_food.html")
    print(f"Admin:   http://localhost:{port}/admin.html")
    print(f"API:     http://localhost:{port}/api/v1")
    try:
        ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        RESET_SCHEDULER.stop()
