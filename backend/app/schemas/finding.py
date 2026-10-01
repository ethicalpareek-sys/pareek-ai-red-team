from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Severity = Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
Classification = Literal["INFORMATIONAL", "POSSIBLE", "LIKELY", "CONFIRMED"]


class EvidenceItem(BaseModel):
    type: str
    label: str
    value: str
    source: str
    confidence: int = 0


class TargetCreate(BaseModel):
    name: str
    owner_user_id: str | None = None
    authorized: bool = False
    allowed_domains: List[str] = Field(default_factory=list)
    allowed_ips: List[str] = Field(default_factory=list)
    excluded_targets: List[str] = Field(default_factory=list)
    allowed_ports: List[int] = Field(default_factory=list)
    safe_mode: bool = True
    rate_limit_per_minute: int = 10
    request_budget: int = 2500
    time_limit_minutes: int = 240


class Finding(BaseModel):
    id: str = ""
    title: str
    asset: str = ""
    endpoint: str = ""
    method: str = "GET"
    category: str = ""
    cwe: str = ""
    owasp: str = ""
    severity: Severity = "LOW"
    confidence: int = Field(ge=0, le=100, default=0)
    classification: Classification = "POSSIBLE"
    evidence: List[EvidenceItem] = Field(default_factory=list)
    affected_component: str = ""
    security_impact: str = ""
    business_impact: str = ""
    safe_validation: str = ""
    remediation: str = ""
    references: List[str] = Field(default_factory=list)
    first_seen: str = ""
    last_seen: str = ""
