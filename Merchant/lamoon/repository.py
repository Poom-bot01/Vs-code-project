"""Persistence layer; replace this JSON implementation with a database later."""

import json
from pathlib import Path


class JsonOrderRepository:
    def __init__(self, path):
        self.path = Path(path)

    def list(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self, orders):
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(orders, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(self.path)
