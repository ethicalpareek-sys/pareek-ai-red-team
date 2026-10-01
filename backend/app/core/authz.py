from __future__ import annotations
from typing import Dict

from .scope import AuthorizationContext


class AuthorizationEngine:
    def __init__(self):
        self._policies: Dict[str, AuthorizationContext] = {}

    def register_target(self, target_id: str, auth_context: AuthorizationContext) -> None:
        self._policies[target_id] = auth_context

    def validate_request(self, target_id: str, host: str, ip: str | None = None, port: int | None = None) -> bool:
        ctx = self._policies.get(target_id)
        if ctx is None:
            return False
        return ctx.can_scan(host, ip=ip, port=port)

    def ensure_safe_mode(self, target_id: str) -> bool:
        ctx = self._policies.get(target_id)
        return bool(ctx and ctx.safe_mode)

    def check_forbidden_actions(self, target_id: str, action: str) -> bool:
        ctx = self._policies.get(target_id)
        if ctx is None:
            return True
        return ctx.is_prohibited(action)
