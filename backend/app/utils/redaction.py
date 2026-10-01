from __future__ import annotations
from typing import Any, Dict, List


class RedactionEngine:
    def redact(self, value: str) -> str:
        sensitive_patterns = [
            "api_key",
            "password",
            "session_token",
            "private_key",
            "access_token",
        ]
        lowered = value.lower()
        for token in sensitive_patterns:
            if token in lowered:
                return "[REDACTED]"
        return value

    def redact_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        redacted = {}
        for key, value in data.items():
            if isinstance(value, dict):
                redacted[key] = self.redact_dict(value)
            elif isinstance(value, list):
                redacted[key] = [self.redact_dict(v) if isinstance(v, dict) else self.redact(v) for v in value]
            else:
                redacted[key] = self.redact(str(value)) if isinstance(value, str) else value
        return redacted
