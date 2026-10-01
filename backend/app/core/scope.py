from __future__ import annotations
from dataclasses import dataclass, field
from ipaddress import ip_address, ip_network
from urllib.parse import urlparse
from typing import Optional, List


@dataclass
class ScopeRule:
    domain: Optional[str] = None
    ip_networks: List[str] = field(default_factory=list)
    ports: List[int] = field(default_factory=list)
    protocol: str = "https"
    allow_redirects: bool = False
    allow_subdomains: bool = False
    reason: str = ""

    def is_host_allowed(self, host: str, ip: Optional[str] = None, port: Optional[int] = None) -> bool:
        parsed = urlparse(f"//{host}") if "://" not in host else urlparse(host)
        host_name = parsed.hostname or host.lower()

        if self.domain and host_name == self.domain.lower():
            return True

        if self.domain and self.allow_subdomains and host_name.endswith("." + self.domain.lower()):
            return True

        if ip:
            try:
                ip_obj = ip_address(ip)
                for cidr in self.ip_networks:
                    if ip_obj in ip_network(cidr, strict=False):
                        return True
            except ValueError:
                pass

        if port is not None and self.ports and port not in self.ports:
            return False

        return False


@dataclass
class AuthorizationContext:
    target_name: str
    authorized: bool
    scope_rules: List[ScopeRule]
    excluded_targets: List[str] = field(default_factory=list)
    safe_mode: bool = True
    rate_limit_per_minute: int = 10
    request_budget: int = 2500
    time_limit_minutes: int = 240
    prohibited_actions: List[str] = field(default_factory=list)

    def can_scan(self, host: str, ip: Optional[str] = None, port: Optional[int] = None) -> bool:
        if not self.authorized:
            return False

        lowered_host = host.lower()
        if any(lowered_host == ex.lower() for ex in self.excluded_targets):
            return False
        if any(lowered_host.endswith("." + ex.lower()) for ex in self.excluded_targets):
            return False

        if not self.scope_rules:
            return False

        for rule in self.scope_rules:
            if rule.is_host_allowed(lowered_host, ip=ip, port=port):
                return True
        return False

    def is_prohibited(self, action: str) -> bool:
        return action.lower() in {x.lower() for x in self.prohibited_actions}
