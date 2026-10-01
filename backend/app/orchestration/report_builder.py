from __future__ import annotations
from typing import Any, Dict, List


class ReportBuilder:
    def build_summary(self, target: Dict[str, Any], findings: List[Dict[str, Any]], attack_paths: List[Dict[str, Any]]) -> Dict[str, Any]:
        summary = {
            "target": target.get("name"),
            "scope": target.get("allowed_domains", []),
            "scan_mode": "SAFE",
            "assets_discovered": 0,
            "endpoints_discovered": 0,
            "technologies": [],
            "findings": {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
            "top_attack_paths": len(attack_paths),
            "confirmed_findings": 0,
            "likely_findings": 0,
            "possible_findings": 0,
            "recommended_remediation": [
                "Enforce authorization boundaries",
                "Reduce endpoint exposure",
                "Harden HTTP headers",
            ],
            "next_safe_tests": [
                "Re-test authenticated flows with explicit scope",
                "Validate secure header policy",
                "Assess GraphQL authorization",
            ],
        }

        for finding in findings:
            sev = finding.get("severity", "INFORMATIONAL").lower()
            if sev == "critical":
                summary["findings"]["critical"] += 1
            elif sev == "high":
                summary["findings"]["high"] += 1
            elif sev == "medium":
                summary["findings"]["medium"] += 1
            elif sev == "low":
                summary["findings"]["low"] += 1
            else:
                summary["findings"]["info"] += 1

        return summary
