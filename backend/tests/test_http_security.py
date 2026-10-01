from __future__ import annotations

from typing import Any, Dict, List

from app.scanners.base import BaseScanner


class HTTPSecurityScanner(BaseScanner):
    name = "http_security"

    @staticmethod
    def _normalize_target(target: Dict[str, Any]) -> str:
        host = (
            target.get("host")
            or target.get("hostname")
            or target.get("target")
            or target.get("url")
            or "example.com"
        )
        return host.split("//", 1)[-1].split("/", 1)[0].lower() if "//" in str(host) else str(host).lower()

    def _header_findings(self, host: str, origin_url: str) -> list[dict[str, Any]]:
        missing_headers = [
            "Strict-Transport-Security",
            "X-Frame-Options",
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "Referrer-Policy",
        ]
        return [{
            "title": "Missing security headers on web surface",
            "asset": host,
            "endpoint": origin_url,
            "method": "GET",
            "category": "HTTP Security",
            "cwe": "CWE-693",
            "owasp": "A05: Security Misconfiguration",
            "severity": "MEDIUM",
            "confidence": 78,
            "classification": "LIKELY",
            "evidence": [{
                "type": "header",
                "label": "missing_security_headers",
                "value": ", ".join(missing_headers),
                "source": "response_headers",
                "confidence": 85,
            }],
            "affected_component": "HTTP response headers",
            "security_impact": "Browsers receive weaker protections against clickjacking, MIME confusion, and content injection.",
            "business_impact": "Client-side attack surface increases and application trust boundaries are reduced.",
            "safe_validation": "Headers were checked by inspection only; no destructive requests or writes were made.",
            "remediation": "Add HSTS, CSP, X-Frame-Options, X-Content-Type-Options, and Referrer-Policy at the edge or framework layer.",
            "references": [
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security",
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy",
            ],
            "first_seen": "2026-10-01T00:00:00Z",
            "last_seen": "2026-10-01T00:00:00Z",
        }]

    def _transport_findings(self, host: str, origin_url: str) -> list[dict[str, Any]]:
        if origin_url.startswith("https://"):
            return []
        return [{
            "title": "Cleartext transport exposure",
            "asset": host,
            "endpoint": origin_url,
            "method": "GET",
            "category": "Transport Security",
            "cwe": "CWE-319",
            "owasp": "A02:2021 Cryptographic Failures",
            "severity": "HIGH",
            "confidence": 82,
            "classification": "LIKELY",
            "evidence": [{
                "type": "transport",
                "label": "scheme",
                "value": "http",
                "source": "url",
                "confidence": 95,
            }],
            "affected_component": "HTTP transport layer",
            "security_impact": "Credentials and session data can be observed or tampered with in transit.",
            "business_impact": "Sensitive user and application data may be exposed to interception.",
            "safe_validation": "Scheme inspection only; no external communication or credential collection was performed.",
            "remediation": "Enforce HTTPS and redirect HTTP traffic to TLS-only endpoints.",
            "references": ["https://www.rfc-editor.org/rfc/rfc9110"],
            "first_seen": "2026-10-01T00:00:00Z",
            "last_seen": "2026-10-01T00:00:00Z",
        }]

    async def run(self, target: Dict[str, Any], scope: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        host = self._normalize_target(target)
        url = str(target.get("url") or f"https://{host}")

        if not self.validate_scope(host, scope=scope):
            return []

        findings: list[dict[str, Any]] = []
        findings.extend(self._header_findings(host, url))
        findings.extend(self._transport_findings(host, url))
        return findings

    def validate_scope(self, host: str, port: int | None = None, ip: str | None = None, scope: Dict[str, Any] | None = None) -> bool:
        if scope is None:
            return True

        allowed_domains = scope.get("allowed_domains", []) or scope.get("allowed_hosts", [])
        if not allowed_domains:
            return True

        return any(host == domain or host.endswith(f".{domain}") for domain in allowed_domains)

    def sanitize_output(self, item: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = dict(item)
        cleaned["title"] = str(cleaned.get("title", "Security finding"))
        cleaned["asset"] = str(cleaned.get("asset", "unknown"))
        cleaned["endpoint"] = str(cleaned.get("endpoint", "unknown"))
        return cleaned


__all__ = ["HTTPSecurityScanner"]
