from __future__ import annotations
from datetime import datetime, timezone
import json
from typing import Any, Dict


class AuditLogger:
    def __init__(self):
        self.entries: list[Dict[str, Any]] = []

    def log(self, event_type: str, message: str, metadata: Dict[str, Any] | None = None, target_id: str | None = None, actor_user_id: str | None = None) -> Dict[str, Any]:
        entry = {
            "id": f"evt-{len(self.entries) + 1}",
            "target_id": target_id,
            "actor_user_id": actor_user_id,
            "event_type": event_type,
            "message": message,
            "metadata": metadata or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.entries.append(entry)
        return entry

    def export(self) -> list[Dict[str, Any]]:
        return self.entries
