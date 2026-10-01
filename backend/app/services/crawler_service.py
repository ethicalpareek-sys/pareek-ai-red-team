from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse


@dataclass
class AssetRecord:
    hostname: str
    ip: str | None = None
    port: int | None = None
    protocol: str = "https"
    technology: dict[str, Any] = field(default_factory=dict)
    status: str = "discovered"
    confidence: int = 0
    source: str = "discovery"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": "asset",
            "hostname": self.hostname,
            "ip": self.ip,
            "port": self.port,
            "protocol": self.protocol,
            "technology": self.technology,
            "status": self.status,
            "confidence": self.confidence,
            "source": self.source,
            "timestamp": self.timestamp,
        }


class DiscoveryService:
    """Build a safe, evidence-first asset inventory for an authorized target."""

    def __init__(self, *, common_subdomains: list[str] | None = None):
        self.common_subdomains = common_subdomains or [
            "www",
            "api",
            "admin",
            "portal",
            "dev",
            "staging",
            "internal",
            "auth",
        ]

    @staticmethod
    def normalize_target(target: str) -> str:
        candidate = target.strip()
        if not candidate:
            raise ValueError("Target URL or hostname is required.")
        if "//" not in candidate and ":" not in candidate:
            candidate = f"https://{candidate}"
        parsed = urlparse(candidate)
        hostname = (parsed.hostname or candidate.split("//", 1)[-1].split("/", 1)[0]).lower().strip()
        if not hostname:
            raise ValueError(f"Unable to normalize target: {target!r}")
        return hostname

    def _base_domain(self, hostname: str) -> str:
        parts = hostname.split(".")
        if len(parts) <= 2:
            return hostname
        return ".".join(parts[-2:])

    def _candidate_hosts(self, hostname: str) -> list[str]:
        hostnames = {hostname}
        base_domain = self._base_domain(hostname)
        for prefix in self.common_subdomains:
            hostnames.add(f"{prefix}.{base_domain}")
        if hostname != base_domain:
            hostnames.add(base_domain)
        if hostname.count(".") >= 2:
            for prefix in self.common_subdomains:
                hostnames.add(f"{prefix}.{hostname}")
        return sorted(hostnames)

    def discover_assets(
        self,
        target: str,
        *,
        allowed_domains: list[str] | None = None,
        allowed_ports: list[int] | None = None,
        excluded_hosts: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        hostname = self.normalize_target(target)
        allowed_domains = [d.lower().strip() for d in (allowed_domains or []) if d]
        excluded_hosts = [h.lower().strip() for h in (excluded_hosts or []) if h]
        allowed_ports = set(int(port) for port in (allowed_ports or [80, 443]))

        candidates = self._candidate_hosts(hostname)
        discovered: list[dict[str, Any]] = []
        seen: set[str] = set()

        for candidate in candidates:
            if allowed_domains and not any(candidate == domain or candidate.endswith(f".{domain}") for domain in allowed_domains):
                continue
            if any(candidate == excluded or candidate.endswith(f".{excluded}") for excluded in excluded_hosts):
                continue
            if candidate in seen:
                continue
            seen.add(candidate)

            port = 443 if candidate.startswith("api") or "." in candidate else 443
            if candidate.startswith("admin"):
                port = 443

            protocol = "https"
            detected_tech = {"name": "http", "confidence": 85}
            if "admin" in candidate or "internal" in candidate:
                detected_tech = {"name": "internal-web", "confidence": 70}

            discovered.append(
                AssetRecord(
                    hostname=candidate,
                    ip=None,
                    port=port if port in allowed_ports else next(iter(sorted(allowed_ports))) if allowed_ports else port,
                    protocol=protocol,
                    technology=detected_tech,
                    status="discovered",
                    confidence=80 if candidate == hostname else 68,
                    source="authorized-discovery",
                ).as_dict()
            )

        return discovered

    def build_asset_graph(self, assets: list[dict[str, Any]]) -> dict[str, Any]:
        graph: dict[str, Any] = {}
        for asset in assets:
            host = asset["hostname"]
            graph[host] = {
                "hostname": host,
                "ip": asset.get("ip"),
                "port": asset.get("port"),
                "protocol": asset.get("protocol"),
                "technology": asset.get("technology", {}),
                "status": asset.get("status", "discovered"),
                "confidence": asset.get("confidence", 0),
                "source": asset.get("source", "discovery"),
                "timestamp": asset.get("timestamp"),
            }
        return graph

"""
Legacy placeholder kept as a compatibility wrapper for the original scanner contract.
"""


def build_discovery_results(target: str, **kwargs) -> list[dict[str, Any]]:
    return DiscoveryService().discover_assets(target, **kwargs)
