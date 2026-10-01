from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class TargetScope:
    target_id: str
    domains: list[str] = field(default_factory=list)
    ips: list[str] = field(default_factory=list)
    ports: list[int] = field(default_factory=list)
    excluded_hosts: list[str] = field(default_factory=list)
    excluded_paths: list[str] = field(default_factory=list)
    mode: str = "SAFE"
    rate_limit: int = 10
    request_budget: int = 2500
    authorized: bool = False


class ScopeService:
    def __init__(self):
        self.scopes: dict[str, TargetScope] = {}

    def register_target(
        self,
        target_id: str,
        *,
        domains: list[str] | None = None,
        ips: list[str] | None = None,
        ports: list[int] | None = None,
        excluded_hosts: list[str] | None = None,
        excluded_paths: list[str] | None = None,
        mode: str = "SAFE",
        rate_limit: int = 10,
        request_budget: int = 2500,
        authorized: bool = True,
    ) -> TargetScope:
        scope = TargetScope(
            target_id=target_id,
            domains=[d.lower().strip() for d in (domains or []) if d],
            ips=[i.strip() for i in (ips or []) if i],
            ports=[int(p) for p in (ports or []) if p is not None],
            excluded_hosts=[h.lower().strip() for h in (excluded_hosts or []) if h],
            excluded_paths=[p.strip() for p in (excluded_paths or []) if p],
            mode=mode.upper(),
            rate_limit=int(rate_limit),
            request_budget=int(request_budget),
            authorized=bool(authorized),
        )
        self.scopes[target_id] = scope
        return scope

    def validate_request(self, target_id: str, url: str, *, port: int | None = None) -> dict[str, object]:
        scope = self.scopes.get(target_id)
        if scope is None:
            return {"allowed": False, "reason": "Target is not registered in the scope engine."}

        if not scope.authorized:
            return {"allowed": False, "reason": "Target must be explicitly authorized before active scanning."}

        parsed = urlparse(url)
        host = (parsed.hostname or "").lower().strip()
        if not host:
            return {"allowed": False, "reason": "Could not resolve a valid hostname from the target URL."}

        if any(host == excluded or host.endswith(f".{excluded}") for excluded in scope.excluded_hosts):
            return {"allowed": False, "reason": "Host is explicitly excluded from the configured scope."}

        allowed = False
        for domain in scope.domains:
            if host == domain or host.endswith(f".{domain}"):
                allowed = True
                break

        if not allowed:
            return {"allowed": False, "reason": "Requested host is outside the authorized domain scope."}

        if scope.ports and port is not None and port not in scope.ports:
            return {"allowed": False, "reason": "Requested port is outside the configured permitted port list."}

        return {
            "allowed": True,
            "target_id": target_id,
            "host": host,
            "port": port,
            "mode": scope.mode,
            "rate_limit": scope.rate_limit,
            "request_budget": scope.request_budget,
        }

    def is_authorized_scan_mode(self, target_id: str) -> bool:
        scope = self.scopes.get(target_id)
        if scope is None:
            return False
        return scope.authorized and scope.mode in {"SAFE", "STANDARD", "DEEP", "API", "AUTHENTICATED", "FULL_ASSESSMENT"}
