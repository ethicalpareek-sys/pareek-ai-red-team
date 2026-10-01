from __future__ import annotations

from typing import Any

from app.services.discovery_service import DiscoveryService


class DiscoveryScanner:
    name = "discovery_scanner"

    def __init__(self):
        self.service = DiscoveryService()

    async def run(self, target: dict[str, Any], scope: dict[str, Any], **kwargs) -> list[dict[str, Any]]:
        allowed_domains = scope.get("allowed_domains", [])
        allowed_ports = scope.get("allowed_ports", [])
        excluded_hosts = scope.get("excluded_targets", [])
        return self.service.discover_assets(
            target.get("target") or target.get("hostname") or "example.com",
            allowed_domains=allowed_domains,
            allowed_ports=allowed_ports,
            excluded_hosts=excluded_hosts,
        )

    def validate_scope(self, host: str, port: int | None = None, ip: str | None = None, scope: dict[str, Any]) -> bool:
        allowed_domains = scope.get("allowed_domains", [])
        if not allowed_domains:
            return False
        return any(host == domain or host.endswith(f".{domain}") for domain in allowed_domains)

    def sanitize_output(self, item: dict[str, Any]) -> dict[str, Any]:
        return item


def build_discovery_results(target: str, **kwargs) -> list[dict[str, Any]]:
    return DiscoveryService().discover_assets(target, **kwargs)
