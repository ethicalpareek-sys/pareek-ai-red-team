from __future__ import annotations
from typing import Any, Dict, List


class AttackPathEngine:
    def build_paths(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        paths: List[Dict[str, Any]] = []
        for finding in findings:
            if "graphql" in finding.get("endpoint", "").lower() and finding.get("category") == "API Security":
                paths.append({
                    "entry_point": "Public GraphQL endpoint",
                    "precondition": "Unauthorized or weakly authorized access to schema metadata",
                    "observed_weakness": "Schema exposure likely reveals internal object structure",
                    "affected_asset": finding.get("asset", ""),
                    "potential_impact": "Reconnaissance leading to privilege abuse or business logic abuse",
                    "evidence": finding.get("evidence", []),
                    "confidence": finding.get("confidence", 0),
                    "remediation": "Disable introspection in production and enforce authentication and authorization",
                })
        return paths
