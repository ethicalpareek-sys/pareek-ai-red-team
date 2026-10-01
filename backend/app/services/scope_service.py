from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.core.authz import AuthorizationEngine
from app.services.scope_service import ScopeService


@dataclass
class TargetRecord:
    id: str
    name: str
    description: str = ""
    authorized_domains: list[str] = field(default_factory=list)
    authorized_ips: list[str] = field(default_factory=list)
    authorized_ports: list[int] = field(default_factory=list)
    excluded_hosts: list[str] = field(default_factory=list)
    excluded_paths: list[str] = field(default_factory=list)
    testing_mode: str = "SAFE"
    rate_limit: int = 10
    request_budget: int = 2500
    authorization_status: str = "PENDING"
    created_at: str | None = None
    updated_at: str | None = None


class TargetService:
    def __init__(self, auth_engine: AuthorizationEngine | None = None, scope_service: ScopeService | None = None):
        self.auth_engine = auth_engine or AuthorizationEngine()
        self.scope_service = scope_service or ScopeService()

    def register_target(self, payload: dict[str, Any]) -> TargetRecord:
        target = TargetRecord(
            id=payload.get("id") or "target-demo-id",
            name=payload["name"],
            description=payload.get("description", ""),
            authorized_domains=payload.get("authorized_domains", []),
            authorized_ips=payload.get("authorized_ips", []),
            authorized_ports=payload.get("authorized_ports", []),
            excluded_hosts=payload.get("excluded_hosts", []),
            excluded_paths=payload.get("excluded_paths", []),
            testing_mode=payload.get("testing_mode", "SAFE").upper(),
            rate_limit=int(payload.get("rate_limit", 10)),
            request_budget=int(payload.get("request_budget", 2500)),
            authorization_status=payload.get("authorization_status", "PENDING"),
        )

        self.scope_service.register_target(
            target.id,
            domains=target.authorized_domains,
            ips=target.authorized_ips,
            ports=target.authorized_ports,
            excluded_hosts=target.excluded_hosts,
            excluded_paths=target.excluded_paths,
            mode=target.testing_mode,
            rate_limit=target.rate_limit,
            request_budget=target.request_budget,
        )

        return target

    def validate_target_request(self, target_id: str, url: str, *, port: int | None = None) -> dict[str, Any]:
        return self.scope_service.validate_request(target_id, url, port=port)
