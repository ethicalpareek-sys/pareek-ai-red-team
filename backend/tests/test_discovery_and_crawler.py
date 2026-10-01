from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.services.crawler_service import CrawlerService
from app.services.discovery_service import DiscoveryService


@dataclass
class OrchestratorContext:
    target_id: str
    mode: str = "SAFE"
    target_url: str | None = None
    assets: list[dict[str, Any]] = field(default_factory=list)
    endpoints: list[dict[str, Any]] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)


class SecurityOrchestrator:
    def __init__(self):
        self.discovery = DiscoveryService()
        self.crawler = CrawlerService()
        self.agents = {
            "recon": "recon_agent",
            "crawler": "crawler_agent",
            "web_security": "web_security_agent",
            "api_security": "api_security_agent",
            "authorization": "authorization_agent",
            "client_side": "client_side_agent",
            "config": "config_agent",
            "dependency": "dependency_agent",
            "correlation": "correlation_agent",
            "validation": "validation_agent",
            "risk": "risk_agent",
            "reporting": "reporting_agent",
        }

    def run_scan(self, target_id: str, mode: str, target_url: str | None = None) -> OrchestratorContext:
        context = OrchestratorContext(target_id=target_id, mode=mode.upper(), target_url=target_url or "https://example.com")

        context.assets = self.discovery.discover_assets(
            context.target_url,
            allowed_domains=["example.com"],
        )
        context.endpoints = self.crawler.collect_endpoints(context.target_url)
        context.findings = [
            {
                "title": "Discovery and crawler foundation initialized",
                "asset": context.target_url,
                "endpoint": context.target_url,
                "category": "Reconnaissance",
                "severity": "INFO",
                "classification": "OBSERVATION",
                "evidence": [{"type": "inventory", "label": "assets", "value": len(context.assets)}],
            }
        ]
        return context

    def deduplicate_findings(self, findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
        deduped: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        for finding in findings:
            key = (
                str(finding.get("title", "")),
                str(finding.get("asset", "")),
                str(finding.get("endpoint", "")),
                str(finding.get("category", "")),
            )
            deduped.setdefault(key, finding)
        return list(deduped.values())
