from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class AuditService:
    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def log(self, event_type: str, message: str, *, target_id: str | None = None, operator_id: str | None = None, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        entry = {
            "id": f"event_{len(self.events) + 1}",
            "event_type": event_type,
            "message": message,
            "target_id": target_id,
            "operator_id": operator_id,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.events.append(entry)
        return entry

