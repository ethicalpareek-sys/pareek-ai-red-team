from __future__ import annotations
from typing import Any, Dict, List


class BaseScanner:
    name: str = "base_scanner"

    async def run(self, target: Dict[str, Any], scope: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        return []

    def validate_scope(self, host: str, port: int | None = None, ip: str | None = None, scope: Dict[str, Any]) -> bool:
        return True

    def sanitize_output(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return item
