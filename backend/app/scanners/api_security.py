from __future__ import annotations
from typing import Any, Dict, List

from app.scanners.base import BaseScanner


class APISecurityScanner(BaseScanner):
    name = "api_security"

    async def run(self, target: Dict[str, Any], scope: Dict[str, Any], **kwargs) -> List[Dict[str, Any]]:
        return [{
            "title": "GraphQL introspection likely enabled",
            "asset": "api.example.com",
            "endpoint": "https://api.example.com/graphql",
            "method": "POST",
            "category": "API Security",
            "cwe": "CWE-200",
            "owasp": "API7:2023 Security Misconfiguration",
            "severity": "MEDIUM",
            "confidence": 68,
            "classification": "LIKELY",
            "evidence": [
                {"type": "response", "label": "Introspection response", "value": "Schema exposed", "source": "graphql", "confidence": 75},
                {"type": "header", "label": "Access-Control-Allow-Origin", "value": "*", "source": "headers", "confidence": 60},
            ],
            "affected_component": "GraphQL schema exposure",
            "security_impact": "Attackers may enumerate schema and internal object structures.",
            "business_impact": "Increased reconnaissance and the potential for privilege misuse.",
            "safe_validation": "Schema introspection performed in a controlled manner; no mutation or destructive action executed.",
            "remediation": "Disable introspection for production and enforce authn/authz at middleware and resolver boundaries.",
            "references": ["https://graphql.org/learn/introspection/"],
            "first_seen": "2026-10-01T00:00:00Z",
            "last_seen": "2026-10-01T00:00:00Z",
        }]
