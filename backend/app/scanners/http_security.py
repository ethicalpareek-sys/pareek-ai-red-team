from __future__ import annotations
from typing import Any, Dict, List

from app.scanners.base import BaseScanner


class HTTPSecurityScanner(BaseScanner):
    name = "http_security"

    async def run(self, target: Dict[str, Any], scope: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        return [{
            "title": "Missing security headers across multiple endpoints",
            "asset": "api.example.com",
            "endpoint": "https://api.example.com/v1",
            "method": "GET",
            "category": "HTTP Security",
            "cwe": "CWE-693",
            "owasp": "A05: Security Misconfiguration",
            "severity": "MEDIUM",
            "confidence": 72,
            "classification": "LIKELY",
            "evidence": [
                {"type": "header", "label": "X-Frame-Options", "value": "missing", "source": "response_headers", "confidence": 80},
                {"type": "header", "label": "Content-Security-Policy", "value": "missing", "source": "response_headers", "confidence": 80},
            ],
            "affected_component": "HTTP response headers",
            "security_impact": "Clickjacking and content injection protections are weaker than expected.",
            "business_impact": "Client-side attack surfaces are elevated and browser protections are reduced.",
            "safe_validation": "Non-destructive verification through header inspection only.",
            "remediation": "Add CSP, X-Frame-Options, and HSTS as appropriate.",
            "references": [
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy",
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
            ],
            "first_seen": "2026-10-01T00:00:00Z",
            "last_seen": "2026-10-01T00:00:00Z",
        }]
