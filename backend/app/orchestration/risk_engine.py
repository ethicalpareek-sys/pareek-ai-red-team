from __future__ import annotations
from typing import Any, Dict, List


class RiskEngine:
    def score_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        severity_weights = {
            "INFORMATIONAL": 1,
            "LOW": 2,
            "MEDIUM": 4,
            "HIGH": 7,
            "CRITICAL": 10,
        }

        severity = finding.get("severity", "INFORMATIONAL")
        confidence = finding.get("confidence", 0)
        evidence_count = len(finding.get("evidence", []))

        score = (severity_weights.get(severity, 1) * 10) + confidence + min(evidence_count * 2, 10)

        return {
            "score": score,
            "explanation": "This is a contextual estimate based on severity, confidence, and evidence density; it is not an absolute truth.",
        }
